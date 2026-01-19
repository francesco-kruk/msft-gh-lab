#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <environment> <azure-location> [subscription-id]" >&2
  exit 1
fi

ENV_NAME="$1"
AZURE_LOCATION="$2"
SUBSCRIPTION_ID="${3:-}"

for cmd in az gh azd jq; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing prerequisite: $cmd" >&2
    exit 1
  fi
done

if ! az account show >/dev/null 2>&1; then
  echo "Azure CLI not logged in. Run: az login" >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "GitHub CLI not authenticated. Run: gh auth login" >&2
  exit 1
fi

if [[ -z "$SUBSCRIPTION_ID" ]]; then
  SUBSCRIPTION_ID="$(az account show --query id -o tsv)"
fi

TENANT_ID="$(az account show --query tenantId -o tsv)"

REPO_FULL="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
REPO_OWNER="${REPO_FULL%%/*}"
REPO_NAME="${REPO_FULL#*/}"

SP_NAME="sp-inventory-app-cicd-${ENV_NAME}"
APP_ID="$(az ad sp list --display-name "$SP_NAME" --query "[0].appId" -o tsv)"

if [[ -z "$APP_ID" ]]; then
  APP_ID="$(az ad sp create-for-rbac \
    --name "$SP_NAME" \
    --role Contributor \
    --scopes "/subscriptions/$SUBSCRIPTION_ID" \
    --query appId -o tsv)"
fi

ROLE_ASSIGNMENT_ID="$(az role assignment list \
  --assignee "$APP_ID" \
  --scope "/subscriptions/$SUBSCRIPTION_ID" \
  --role Contributor \
  --query "[0].id" -o tsv)"

if [[ -z "$ROLE_ASSIGNMENT_ID" ]]; then
  az role assignment create \
    --assignee "$APP_ID" \
    --role Contributor \
    --scope "/subscriptions/$SUBSCRIPTION_ID" >/dev/null
fi

APP_OBJECT_ID="$(az ad app show --id "$APP_ID" --query id -o tsv)"
SUBJECT="repo:${REPO_FULL}:environment:${ENV_NAME}"
EXISTING_FED_CRED_COUNT="$(az ad app federated-credential list \
  --id "$APP_OBJECT_ID" \
  --query "[?subject=='$SUBJECT'] | length(@)" -o tsv)"

if [[ "$EXISTING_FED_CRED_COUNT" == "0" ]]; then
  az ad app federated-credential create \
    --id "$APP_OBJECT_ID" \
    --parameters "$(jq -n \
      --arg name "github-${ENV_NAME}" \
      --arg issuer "https://token.actions.githubusercontent.com" \
      --arg subject "$SUBJECT" \
      --arg audience "api://AzureADTokenExchange" \
      '{name:$name, issuer:$issuer, subject:$subject, audiences:[$audience]}')" \
    >/dev/null
fi

gh api -X PUT "repos/${REPO_OWNER}/${REPO_NAME}/environments/${ENV_NAME}" >/dev/null

gh secret set -e "$ENV_NAME" AZURE_CLIENT_ID -b "$APP_ID"
gh secret set -e "$ENV_NAME" AZURE_TENANT_ID -b "$TENANT_ID"
gh secret set -e "$ENV_NAME" AZURE_SUBSCRIPTION_ID -b "$SUBSCRIPTION_ID"

if ! azd env select "$ENV_NAME" >/dev/null 2>&1; then
  azd env new "$ENV_NAME"
fi

azd env set AZURE_ENV_NAME "$ENV_NAME"
azd env set AZURE_LOCATION "$AZURE_LOCATION"
azd env set AZD_PIPELINE_PROVIDER "github"

echo "CI/CD setup complete for environment: $ENV_NAME"
