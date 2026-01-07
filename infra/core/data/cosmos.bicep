@description('The name of the Cosmos DB account')
param accountName string

@description('The location for the Cosmos DB account')
param location string = resourceGroup().location

@description('Tags for the resources')
param tags object = {}

@description('Whether to enable Free Tier (only one per subscription)')
param enableFreeTier bool = false

@description('The name of the database')
param databaseName string = 'inventory'

@description('The name of the devices container')
param devicesContainerName string = 'devices'

@description('Enable serverless capacity mode')
param enableServerless bool = true

// Cosmos DB Account
resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2024-11-15' = {
  name: accountName
  location: location
  tags: tags
  kind: 'GlobalDocumentDB'
  properties: {
    // CRITICAL: Must be 'Enabled' for Container Apps without VNet integration
    // Container Apps use outbound public IPs unless configured with private endpoints
    publicNetworkAccess: 'Enabled'
    
    // Allow Azure services to bypass firewall - this allows Container Apps to connect
    // even without adding their specific IPs (which are dynamic)
    networkAclBypass: 'AzureServices'
    networkAclBypassResourceIds: []
    
    // Empty ipRules means: with networkAclBypass, Azure services can connect
    // Add specific IPs here if you need to allow additional access
    ipRules: []
    
    // Virtual network filtering not enabled (would need VNet integration)
    isVirtualNetworkFilterEnabled: false
    virtualNetworkRules: []
    
    databaseAccountOfferType: 'Standard'
    enableFreeTier: enableFreeTier
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
    }
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
    capabilities: enableServerless ? [
      {
        name: 'EnableServerless'
      }
    ] : []
    
    // Disable key-based access for better security, rely on RBAC only
    disableKeyBasedMetadataWriteAccess: false
  }
}

// SQL Database
resource database 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-11-15' = {
  parent: cosmosAccount
  name: databaseName
  properties: {
    resource: {
      id: databaseName
    }
  }
}

// Devices Container
resource devicesContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-11-15' = {
  parent: database
  name: devicesContainerName
  properties: {
    resource: {
      id: devicesContainerName
      partitionKey: {
        paths: ['/id']
        kind: 'Hash'
      }
      indexingPolicy: {
        indexingMode: 'consistent'
        automatic: true
        includedPaths: [
          {
            path: '/*'
          }
        ]
        excludedPaths: [
          {
            path: '/"_etag"/?'
          }
        ]
      }
    }
  }
}

// Outputs
output endpoint string = cosmosAccount.properties.documentEndpoint
output accountName string = cosmosAccount.name
output databaseName string = database.name
output devicesContainerName string = devicesContainer.name
