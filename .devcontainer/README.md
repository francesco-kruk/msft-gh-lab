# Codespaces Quickstart

## Quick Start
1. Open this repo in GitHub Codespaces.
2. Wait for the devcontainer to finish building.
3. Authenticate: `azd auth login`
4. Create environment: `azd env new <name>`
5. Set location: `azd env set AZURE_LOCATION eastus`
6. Deploy: `azd up`

Optional helper:
- `bash .devcontainer/scripts/azd-up.sh`

## Authentication
- Recommended: `azd auth login`
- If `preprovision.sh` fails, also run `az login`
- Set subscription if needed: `az account set --subscription <id>`

## Cosmos DB Configuration
- Cosmos is Azure-only with RBAC (no local emulator)
- Deployed backend uses System-Assigned Managed Identity
- For local backend development: assign your Azure user the “Cosmos DB Built-in Data Contributor” role on the Cosmos account

## Environment Variables
Use `azd env set`:
- `AZURE_LOCATION`: Azure region (required, e.g., eastus)
- `AZURE_SUBSCRIPTION_ID`: Target subscription (optional)
- `cosmosFreeTierEnabled`: true/false (optional, default: true)

## Local Development (Optional)
- Backend: `cd backend && uv run uvicorn src.main:app --reload` (port 8000)
- Frontend: `cd frontend && npm run dev` (port 3000)
- Frontend proxies `/api` to `http://localhost:8000` in dev mode
- Requires Cosmos RBAC for your user

## Troubleshooting
- azd command not found: rebuild the devcontainer
- Docker daemon not accessible: restart Codespace
- Cosmos access denied locally: assign Cosmos data contributor role
- preprovision.sh fails: ensure both `azd auth login` and `az login` are completed

## Recommended Codespaces Secrets
- `AZURE_SUBSCRIPTION_ID`
- `AZURE_LOCATION`
- `AZURE_TENANT_ID`
