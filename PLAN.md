# Devcontainer Implementation Plan

## Overview

Add a `.devcontainer/` configuration to enable GitHub Codespaces support with a seamless "open and deploy" experience. The default workflow will be `azd up` to provision Azure resources and deploy the application, with Cosmos DB remaining Azure-only (no local emulator) and configuration managed via `azd env`.

## Architecture Decisions

### Single Container Approach
- Use a single devcontainer (no docker-compose) with multi-language support
- Base image with Python 3.11 + Node.js 20
- Install Azure tooling via devcontainer Features
- Enable Docker-outside-of-Docker for `azd up` image building

### Default Workflow: Deploy-First
- Primary path: `azd auth login` → `azd env new` → `azd up`
- Cosmos DB is Azure-only with RBAC (no local emulator)
- Environment configuration via `azd env set` commands
- Deployed entrypoint is the frontend Container App URL

### Optional Local Development
- Backend: `uv run uvicorn src.main:app --reload` (port 8000)
- Frontend: `npm run dev` (port 3000, proxies to backend)
- Note: Local backend requires Cosmos RBAC roles assigned to dev user

## File Structure

```
.devcontainer/
├── devcontainer.json          # Main devcontainer configuration
├── post-create.sh             # Run once after container creation
├── post-start.sh              # Run on every container start
├── scripts/
│   └── azd-up.sh             # Helper wrapper for azd up workflow
└── README.md                  # Codespaces-specific quickstart
```

## Implementation Details

### 1. `.devcontainer/devcontainer.json`

**Purpose**: Define the Codespaces environment with all required tools and settings.

**Key Configuration**:
- **Base Image**: `mcr.microsoft.com/devcontainers/python:3.11`
- **Features to Install**:
  - `ghcr.io/azure/azure-dev/azd:latest` - Azure Developer CLI
  - `ghcr.io/devcontainers/features/azure-cli:1` - Azure CLI
  - `ghcr.io/devcontainers/features/docker-outside-of-docker:1` - Docker access
  - `ghcr.io/devcontainers/features/node:1` with version "20"
  - `ghcr.io/devcontainers/features/github-cli:1` - GitHub CLI (optional)

- **Port Forwarding**:
  - 3000: Frontend Vite dev server
  - 8000: Backend FastAPI dev server
  - Label ports clearly for developer UX

- **VS Code Extensions**:
  - `ms-azuretools.azure-dev` - Azure Developer CLI extension
  - `ms-azuretools.vscode-bicep` - Bicep language support
  - `ms-python.python` - Python language support
  - `dbaeumer.vscode-eslint` - ESLint
  - `esbenp.prettier-vscode` - Prettier
  - `GitHub.copilot` - GitHub Copilot (optional)
  - `redhat.vscode-yaml` - YAML support

- **Lifecycle Hooks**:
  - `postCreateCommand`: `.devcontainer/post-create.sh`
  - `postStartCommand`: `.devcontainer/post-start.sh`

- **Settings**:
  - Set Python default interpreter path
  - Configure terminal to use bash
  - Set reasonable defaults for formatters

### 2. `.devcontainer/post-create.sh`

**Purpose**: One-time setup after container creation. Print clear next steps without auto-provisioning.

**Tasks**:
1. Verify required tools are installed (`azd`, `az`, `docker`, `node`, `python`, `uv`)
2. Optionally install `uv` if not present (backend package manager)
3. Optionally run `cd backend && uv sync` to pre-install backend dependencies
4. Optionally run `cd frontend && npm ci` to pre-install frontend dependencies
5. Print welcome message with golden path instructions:
   ```
   🚀 Codespaces Ready!
   
   To deploy to Azure:
   1. azd auth login
   2. azd env new <environment-name>
   3. azd env set AZURE_LOCATION <region>  # e.g., eastus
   4. azd up
   
   After deployment, find your app URL:
   azd env get-values | grep FRONTEND_URI
   
   For local development:
   - Backend: cd backend && uv run uvicorn src.main:app --reload
   - Frontend: cd frontend && npm run dev
   
   Note: Local backend requires Cosmos RBAC roles for your Azure user.
   ```

### 3. `.devcontainer/post-start.sh`

**Purpose**: Lightweight reminder on every container start.

**Tasks**:
1. Check if `azd env` is configured (`azd env list`)
2. Check if Azure auth is valid (`az account show`)
3. Print context-aware reminder:
   - If no env: show `azd env new` command
   - If env exists but not deployed: show `azd up` command
   - If deployed: show `azd env get-values` to find URLs

### 4. `.devcontainer/scripts/azd-up.sh`

**Purpose**: Helper script that validates prerequisites and runs `azd up`.

**Logic**:
1. Check for Azure auth: `az account show` or `azd auth login` status
2. Check for active azd environment: `azd env list`
3. Verify required env vars are set (or prompt user to set them):
   - `AZURE_LOCATION` (required for initial deployment)
   - Optional: `AZURE_SUBSCRIPTION_ID`
4. Run `azd up` with appropriate flags
5. On success, display the frontend URL and how to access it

**Usage**:
```bash
./.devcontainer/scripts/azd-up.sh
```

### 5. `.devcontainer/README.md`

**Purpose**: Codespaces-specific quickstart and troubleshooting guide.

**Sections**:

#### Quick Start
1. Open in Codespaces (automatic devcontainer build)
2. Wait for post-create script to complete
3. Authenticate: `azd auth login`
4. Create environment: `azd env new <name>`
5. Set location: `azd env set AZURE_LOCATION eastus`
6. Deploy: `azd up`

#### Authentication
- Recommended: `azd auth login` (device code flow works in Codespaces)
- If `preprovision.sh` complains: also run `az login`
- Set subscription if needed: `az account set --subscription <id>`

#### Cosmos DB Configuration
- Cosmos is **Azure-only** with RBAC authentication (no local auth, no emulator)
- Deployed backend uses System-Assigned Managed Identity (automatic)
- For local backend development: assign your Azure user "Cosmos DB Built-in Data Contributor" role on the Cosmos account

#### Environment Variables
- Configuration via `azd env set`:
  - `AZURE_LOCATION`: Azure region (required, e.g., "eastus")
  - `AZURE_SUBSCRIPTION_ID`: Target subscription (optional if default is correct)
  - `cosmosFreeTierEnabled`: true/false (optional, default: true)

#### Local Development (Optional)
- Backend: `cd backend && uv run uvicorn src.main:app --reload` (port 8000)
- Frontend: `cd frontend && npm run dev` (port 3000)
- Frontend proxies `/api` to `http://localhost:8000` in dev mode
- Requires Cosmos RBAC for your user

#### Troubleshooting
- **azd command not found**: Reload window or check Feature installation
- **Docker daemon not accessible**: Restart Codespace
- **Cosmos access denied locally**: Assign your user Cosmos data contributor role
- **preprovision.sh fails**: Ensure both `azd auth login` and `az login` are completed

#### Recommended Codespaces Secrets
- `AZURE_SUBSCRIPTION_ID`: Your Azure subscription ID
- `AZURE_LOCATION`: Preferred deployment region
- `AZURE_TENANT_ID`: Microsoft Entra tenant (if using specific tenant)

These can be set at the repo or org level in GitHub Codespaces settings.

## Workflow After Implementation

### First-Time Codespaces User Flow

1. Click "Open in GitHub Codespaces" (or create from repo)
2. Wait 2-3 minutes for devcontainer build + post-create script
3. See welcome message with next steps
4. Run: `azd auth login` (opens device code flow)
5. Run: `azd env new codespaces-demo` (or custom name)
6. Run: `azd env set AZURE_LOCATION eastus`
7. Run: `azd up` (provisions Azure resources and deploys)
8. Open the `FRONTEND_URI` from output
9. Done! App is running in Azure

### Returning User Flow

1. Open existing Codespace
2. See post-start reminder with context
3. If already deployed: `azd env get-values` to find URLs
4. If need to redeploy: `azd up`
5. If need to update: make code changes → `azd deploy`

## Prerequisites to Verify/Fix

### 1. Bicep Parameters Alignment
**Issue**: `infra/main.parameters.json` contains `principalId`, `principalType`, `principalName` but `infra/main.bicep` may not declare these parameters.

**Action**: Review and align:
- Option A: Remove unused parameters from `main.parameters.json`
- Option B: Add matching parameter declarations to `main.bicep` if they're intended to be used

### 2. preprovision.sh Auth Check
**Current**: `infra/hooks/preprovision.sh` checks `az account show`

**Consideration**: Decide if this should also accept `azd auth login` only, or keep requiring Azure CLI auth.

## Additional Enhancements (Future)

### Prebuilds
Enable GitHub Codespaces prebuilds to speed up container creation:
- Prebuild steps: tool installation, `npm ci`, `uv sync`
- Skip: `azd up` (requires auth + creates billable resources)

### Task Integration
Add `.vscode/tasks.json` entries for common commands:
- "Deploy to Azure" → runs `azd up`
- "Start Backend Locally" → runs backend dev server
- "Start Frontend Locally" → runs frontend dev server
- "View Azure Resources" → runs `azd show`

### Environment Name Convention
Suggest standardized naming for Codespaces environments:
- Pattern: `codespace-${GITHUB_USER}-${GITHUB_CODESPACE_NAME}`
- Add helper to post-create.sh to generate this automatically

### Testing Script
Add `.devcontainer/scripts/test-setup.sh` to validate:
- All required tools are installed and correct versions
- Azure connectivity works
- Docker daemon is accessible
- Ports are forwarded correctly

## Success Criteria

✅ A new Codespace can run `azd up` successfully after minimal setup (auth + env)  
✅ All required Azure tools (azd, az, bicep, docker) are pre-installed  
✅ Clear documentation guides users through the golden path  
✅ Port forwarding enables optional local development  
✅ No auto-provisioning (respects user control over Azure resources)  
✅ Cosmos remains Azure-only with RBAC authentication  
✅ Environment configuration managed via `azd env`  

## Implementation Order

1. Create `.devcontainer/devcontainer.json` with base config
2. Create `.devcontainer/post-create.sh` with setup and welcome message
3. Create `.devcontainer/post-start.sh` with context-aware reminders
4. Create `.devcontainer/scripts/azd-up.sh` helper script
5. Create `.devcontainer/README.md` with comprehensive guide
6. Fix any Bicep parameter mismatches in infra files
7. Update main `README.md` with "Open in Codespaces" section
8. Test in an actual Codespace
9. Iterate based on UX feedback

## Reference

Based on: https://github.com/Azure-Samples/az-ai-devcontainer/tree/main/.devcontainer

Key differences from reference:
- This repo has both frontend + backend (Python + Node)
- Uses `uv` instead of pip/poetry for Python deps
- Default workflow is deploy-first (`azd up`) vs local-first
- No AI model dependencies (simpler setup)
