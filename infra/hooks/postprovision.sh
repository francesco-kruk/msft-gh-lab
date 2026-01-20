#!/usr/bin/env bash
set -euo pipefail

log() {
  echo "[postprovision] $*"
}

log "Assigning Cosmos DB data role to current principal if needed..."

if ! az account show > /dev/null 2>&1; then
  log "Not logged in to Azure CLI. Please run 'az login' first."
  exit 1
fi

AZURE_RESOURCE_GROUP=$(azd env get-values | sed -n 's/^AZURE_RESOURCE_GROUP=//p' | tr -d '"')
COSMOS_ENDPOINT=$(azd env get-values | sed -n 's/^COSMOS_ENDPOINT=//p' | tr -d '"')

if [[ -z "${AZURE_RESOURCE_GROUP}" ]]; then
  log "AZURE_RESOURCE_GROUP not found in azd environment values."
  exit 1
fi

if [[ -z "${COSMOS_ENDPOINT}" ]]; then
  log "COSMOS_ENDPOINT not found in azd environment values."
  exit 1
fi

ACCOUNT_NAME=$(echo "${COSMOS_ENDPOINT}" | sed -E 's#https?://([^./]+).*#\1#')

if [[ -z "${ACCOUNT_NAME}" ]]; then
  log "Failed to parse Cosmos DB account name from COSMOS_ENDPOINT=${COSMOS_ENDPOINT}."
  exit 1
fi

USER_TYPE=$(az account show --query user.type -o tsv)
USER_NAME=$(az account show --query user.name -o tsv)

PRINCIPAL_ID=""
if [[ "${USER_TYPE}" == "user" ]]; then
  PRINCIPAL_ID=$(az ad signed-in-user show --query id -o tsv)
else
  PRINCIPAL_ID=$(az ad sp show --id "${USER_NAME}" --query id -o tsv)
fi

if [[ -z "${PRINCIPAL_ID}" ]]; then
  log "Failed to resolve principal ID for current Azure CLI identity."
  exit 1
fi

ROLE_DEFINITION_ID=$(az cosmosdb sql role definition list \
  --account-name "${ACCOUNT_NAME}" \
  --resource-group "${AZURE_RESOURCE_GROUP}" \
  --query "[?roleName=='Cosmos DB Built-in Data Contributor'].id | [0]" -o tsv)

if [[ -z "${ROLE_DEFINITION_ID}" ]]; then
  log "Failed to resolve Cosmos DB Built-in Data Contributor role definition ID."
  exit 1
fi

EXISTING_ASSIGNMENT=$(az cosmosdb sql role assignment list \
  --account-name "${ACCOUNT_NAME}" \
  --resource-group "${AZURE_RESOURCE_GROUP}" \
  --query "[?principalId=='${PRINCIPAL_ID}'].id | [0]" -o tsv)

if [[ -n "${EXISTING_ASSIGNMENT}" ]]; then
  log "Role assignment already exists for principal ${PRINCIPAL_ID}."
  exit 0
fi

# Get subscription ID for constructing the scope
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
SCOPE="/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${AZURE_RESOURCE_GROUP}/providers/Microsoft.DocumentDB/databaseAccounts/${ACCOUNT_NAME}"

az cosmosdb sql role assignment create \
  --account-name "${ACCOUNT_NAME}" \
  --resource-group "${AZURE_RESOURCE_GROUP}" \
  --principal-id "${PRINCIPAL_ID}" \
  --role-definition-id "${ROLE_DEFINITION_ID}" \
  --scope "${SCOPE}" > /dev/null

log "Role assignment created for principal ${PRINCIPAL_ID}."
