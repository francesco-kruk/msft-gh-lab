# Plan: Automated GitHub Actions CI/CD with azd & OIDC

This plan outlines the steps to set up a fully automated, idempotent CI/CD pipeline using GitHub Actions reusable workflows with OIDC authentication.

## 1. Idempotent Setup Script (`scripts/setup-cicd.sh`)

Create a script to automate the initialization of GitHub Secrets and Azure OIDC federation.
*   **Idempotency checks**: Verify prerequisites (`az`, `gh`, `azd`, `jq`) and existing resources before creation.
*   **Service Principal**: Identify or create an SP with `Contributor` role (`sp-inventory-app-cicd-<env>`).
*   **OIDC**: Detect or add federated credentials for subject `repo:<org>/<repo>:environment:<env>`.
*   **GitHub Environment**: Create environment via `gh api` and store secrets:
    *   `AZURE_CLIENT_ID`
    *   `AZURE_TENANT_ID`
    *   `AZURE_SUBSCRIPTION_ID`
*   **azd Initialization**: Create/select environment (`azd env new`), set `AZURE_ENV_NAME`, `AZURE_LOCATION`, and `AZD_PIPELINE_PROVIDER=github`.

## 2. Reusable Deployment Workflow (`.github/workflows/deploy.yml`)

Create a workflow to standardize deployment across environments.
*   **Inputs**: `environment` (GitHub Env), `azure_env_name` (azd Env).
*   **Steps**:
    1.  Checkout code (full history).
    2.  Authenticate with `azure/login@v2` (OIDC).
    3.  Install azd (`Azure/setup-azd`).
    4.  Select environment (`azd env select`).
    5.  Set image tags using commit SHA (`SERVICE_BACKEND_IMAGE_NAME`, `SERVICE_FRONTEND_IMAGE_NAME`).
    6.  Run `azd provision --no-prompt`.
    7.  Run `azd deploy --no-prompt`.

## 3. CI Workflow (`.github/workflows/ci.yml`)

Create a workflow for Pull Request validation.
*   **Trigger**: PRs to `main`.
*   **Parallel Jobs**:
    *   **Backend**: `uv` install, backend sync, `STORAGE_MODE=memory uv run pytest`.
    *   **Frontend**: `npm ci`, `npm run lint`.
    *   **IaC**: `az bicep build --file infra/main.bicep`.

## 4. Dev Deployment Workflow (`.github/workflows/deploy-dev.yml`)

Create a CD workflow for the development environment.
*   **Trigger**: Push to `main`.
*   **Concurrency**: Group by environment to queue deployments.
*   **Job**: Call `deploy.yml` with `environment: dev`, `azure_env_name: dev`.

## 5. Prod Deployment Workflow (`.github/workflows/deploy-prod.yml`)

Create a workflow for controlled production releases.
*   **Trigger**: `workflow_dispatch` with required boolean `confirm_production_deployment`.
*   **Concurrency**: Group by environment to queue deployments.
*   **Job**:
    *   Validate confirmation input.
    *   Call `deploy.yml` with `environment: prod`, `azure_env_name: prod`.
