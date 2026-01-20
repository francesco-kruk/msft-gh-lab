targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the environment that can be used as part of naming resource convention')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

@description('Whether to enable Cosmos DB Free Tier (only one per subscription)')
param cosmosFreeTierEnabled bool = false

@description('Backend container image name')
param backendImageName string = ''

@description('Frontend container image name')
param frontendImageName string = ''

@description('Allowed CORS origins for backend API (comma-separated)')
param allowedOrigins string = '*'

// Tags that should be applied to all resources
var tags = {
  'azd-env-name': environmentName
}

// Generate a unique token for resource naming
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))

// Computed resource names
var cosmosAccountName = 'cosmos-${resourceToken}'
var cosmosDatabaseName = 'inventory'
var cosmosDevicesContainerName = 'devices'

// Organize resources in a resource group
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: 'rg-gh-lab-${environmentName}'
  location: location
  tags: tags
}

// Container Apps Environment
module containerAppsEnvironment 'core/host/container-apps-environment.bicep' = {
  name: 'container-apps-environment'
  scope: rg
  params: {
    name: 'cae-${resourceToken}'
    location: location
    tags: tags
  }
}

// Container Registry
module containerRegistry 'core/host/container-registry.bicep' = {
  name: 'container-registry'
  scope: rg
  params: {
    name: 'cr${resourceToken}'
    location: location
    tags: tags
  }
}

// Cosmos DB account, database, and containers
module cosmos 'core/data/cosmos.bicep' = {
  name: 'cosmos'
  scope: rg
  params: {
    accountName: cosmosAccountName
    location: location
    tags: tags
    enableFreeTier: cosmosFreeTierEnabled
    databaseName: cosmosDatabaseName
    devicesContainerName: cosmosDevicesContainerName
    enableServerless: true
  }
}

// Frontend Container App (deployed first so backend can reference its URL)
module frontend 'core/host/container-app.bicep' = {
  name: 'frontend'
  scope: rg
  params: {
    name: 'ca-frontend-${resourceToken}'
    location: location
    tags: tags
    serviceName: 'frontend'
    containerAppsEnvironmentName: containerAppsEnvironment.outputs.name
    containerRegistryName: containerRegistry.outputs.name
    containerName: 'frontend'
    containerImage: !empty(frontendImageName) ? frontendImageName : 'nginx:latest'
    targetPort: 80
    minReplicas: 1
    env: [
      {
        name: 'BACKEND_URL'
        value: 'http://localhost'
      }
    ]  // Backend URL will be set accurately after backend is created
  }
}

// Backend Container App (uses system-assigned managed identity for Cosmos DB access)
module backend 'core/host/container-app.bicep' = {
  name: 'backend'
  scope: rg
  params: {
    name: 'ca-backend-${resourceToken}'
    location: location
    tags: tags
    serviceName: 'backend'
    containerAppsEnvironmentName: containerAppsEnvironment.outputs.name
    containerRegistryName: containerRegistry.outputs.name
    containerName: 'backend'
    containerImage: !empty(backendImageName) ? backendImageName : 'nginx:latest'
    targetPort: 8000
    minReplicas: 1
    enableProbes: true  // Enable health probes for reliability
    enableManagedIdentity: true  // Use system-assigned managed identity
    external: false  // Internal: only accessible within Container Apps Environment
    allowInsecure: true  // Allow HTTP for internal container-to-container communication
    env: [
      {
        name: 'COSMOS_ENDPOINT'
        value: cosmos.outputs.endpoint
      }
      {
        name: 'COSMOS_DB_NAME'
        value: cosmosDatabaseName
      }
      {
        name: 'COSMOS_DEVICES_CONTAINER'
        value: cosmosDevicesContainerName
      }
      {
        name: 'ALLOWED_ORIGINS'
        // Automatically allow the frontend URL + custom origins parameter
        value: !empty(allowedOrigins) && allowedOrigins != '*' ? '${frontend.outputs.uri},${allowedOrigins}' : frontend.outputs.uri
      }
    ]
  }
  dependsOn: [
    frontend
  ]
}

// Cosmos DB RBAC role assignment for backend managed identity
// This must be deployed after both cosmos and backend to get the principal ID
module cosmosRbac 'core/data/cosmos-rbac.bicep' = {
  name: 'cosmos-rbac'
  scope: rg
  params: {
    accountName: cosmosAccountName
    principalId: backend.outputs.identityPrincipalId
  }
}

// Update frontend with backend URL (requires second deployment after backend exists)
module frontendUpdate 'core/host/container-app.bicep' = {
  name: 'frontend-update'
  scope: rg
  params: {
    name: 'ca-frontend-${resourceToken}'
    location: location
    tags: tags
    serviceName: 'frontend'
    containerAppsEnvironmentName: containerAppsEnvironment.outputs.name
    containerRegistryName: containerRegistry.outputs.name
    containerName: 'frontend'
    containerImage: !empty(frontendImageName) ? frontendImageName : 'nginx:latest'
    targetPort: 80
    minReplicas: 1
    env: [
      {
        name: 'BACKEND_URL'
        value: 'http://${backend.outputs.name}.internal.${containerAppsEnvironment.outputs.defaultDomain}'  // Internal DNS name for container-to-container communication
      }
    ]
  }
  dependsOn: [
    backend
  ]
}

// Outputs
output AZURE_LOCATION string = location
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerRegistry.outputs.loginServer
output AZURE_CONTAINER_REGISTRY_NAME string = containerRegistry.outputs.name
output BACKEND_URI string = backend.outputs.uri
output FRONTEND_URI string = frontendUpdate.outputs.uri
output COSMOS_ENDPOINT string = cosmos.outputs.endpoint
output COSMOS_DB_NAME string = cosmosDatabaseName
output AZURE_RESOURCE_GROUP string = rg.name
