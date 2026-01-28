# Automated GitHub Actions CI/CD with azd & OIDC

## Overview
Set up a fully automated, idempotent CI/CD pipeline using GitHub Actions reusable workflows with OIDC authentication. This enables secure deployments to Azure without storing long-lived credentials, with automated validation on pull requests and controlled deployments to development and production environments.

## Phase 1: Setup Script Implementation
Create an idempotent automation script to configure Azure OIDC federation and GitHub secrets.

- [ ] **Task 1.1**: Create setup script structure
  - File: `scripts/setup-cicd.sh`
  - Add prerequisite checks for required tools: `az`, `gh`, `azd`, `jq`
  - Implement idempotency by checking for existing resources before creation
  - Accept environment parameter (`dev` or `prod`)

- [ ] **Task 1.2**: Implement Service Principal management
  - Create or identify existing SP with naming convention `sp-inventory-app-cicd-<env>`
  - Assign `Contributor` role to the SP
  - Store SP credentials for OIDC configuration

- [ ] **Task 1.3**: Configure Azure OIDC federation
  - Detect or add federated credentials for GitHub OIDC
  - Set subject format: `repo:<org>/<repo>:environment:<env>`
  - Enable OIDC authentication for GitHub Actions

- [ ] **Task 1.4**: Create GitHub environment and secrets
  - Use `gh api` to create GitHub environment if it doesn't exist
  - Store required secrets in GitHub environment:
    - `AZURE_CLIENT_ID`
    - `AZURE_TENANT_ID`
    - `AZURE_SUBSCRIPTION_ID`

- [ ] **Task 1.5**: Initialize azd environment
  - Create or select azd environment: `azd env new <env>` or `azd env select <env>`
  - Configure environment variables: `AZURE_ENV_NAME`, `AZURE_LOCATION`
  - Set pipeline provider: `AZD_PIPELINE_PROVIDER=github`

## Phase 2: Reusable Deployment Workflow
Create a standardized deployment workflow that can be called for any environment.

- [ ] **Task 2.1**: Create reusable workflow file
  - File: `.github/workflows/deploy.yml`
  - Define `workflow_call` trigger
  - Add inputs: `environment` (GitHub Environment), `azure_env_name` (azd Environment)

- [ ] **Task 2.2**: Implement checkout step
  - Use `actions/checkout@v4`
  - Fetch full git history for proper versioning

- [ ] **Task 2.3**: Configure Azure authentication
  - Use `azure/login@v2` with OIDC
  - Reference environment secrets: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`

- [ ] **Task 2.4**: Set up azd tooling
  - Install azd using `Azure/setup-azd` action
  - Select target environment: `azd env select ${{ inputs.azure_env_name }}`

- [ ] **Task 2.5**: Configure container image tags
  - Set environment variables for image tags using commit SHA
  - `SERVICE_BACKEND_IMAGE_NAME` with tag from `github.sha`
  - `SERVICE_FRONTEND_IMAGE_NAME` with tag from `github.sha`

- [ ] **Task 2.6**: Execute deployment
  - Run `azd provision --no-prompt` to create/update infrastructure
  - Run `azd deploy --no-prompt` to deploy application code
  - Ensure proper error handling and output logging

## Phase 3: CI Workflow
Create a workflow to validate pull requests before merging.

- [ ] **Task 3.1**: Create CI workflow file
  - File: `.github/workflows/ci.yml`
  - Trigger on pull requests to `main` branch
  - Configure parallel job execution

- [ ] **Task 3.2**: Implement backend validation job
  - Install `uv` for Python dependency management
  - Run `uv sync` to install backend dependencies
  - Execute tests: `STORAGE_MODE=memory uv run pytest`
  - Use in-memory storage mode to avoid Azure dependencies

- [ ] **Task 3.3**: Implement frontend validation job
  - Run `npm ci` to install frontend dependencies
  - Execute linting: `npm run lint`
  - Run frontend build to catch compilation errors

- [ ] **Task 3.4**: Implement infrastructure validation job
  - Validate Bicep templates: `az bicep build --file infra/main.bicep`
  - Ensure IaC is syntactically correct before merge

## Phase 4: Development Deployment
Create an automated deployment workflow for the development environment.

- [ ] **Task 4.1**: Create dev deployment workflow file
  - File: `.github/workflows/deploy-dev.yml`
  - Trigger on push to `main` branch
  - Configure concurrency group by environment to queue deployments

- [ ] **Task 4.2**: Configure workflow to call reusable deployment
  - Call `.github/workflows/deploy.yml`
  - Pass parameters: `environment: dev`, `azure_env_name: dev`
  - Ensure proper secret and permission inheritance

## Phase 5: Production Deployment
Create a controlled, manual deployment workflow for production.

- [ ] **Task 5.1**: Create prod deployment workflow file
  - File: `.github/workflows/deploy-prod.yml`
  - Trigger: `workflow_dispatch` (manual only)
  - Add required input: `confirm_production_deployment` (boolean)
  - Configure concurrency group by environment to prevent parallel deployments

- [ ] **Task 5.2**: Implement deployment confirmation
  - Validate that `confirm_production_deployment` is `true`
  - Add conditional job step to block deployment if not confirmed
  - Provide clear error message if confirmation is missing

- [ ] **Task 5.3**: Configure workflow to call reusable deployment
  - Call `.github/workflows/deploy.yml`
  - Pass parameters: `environment: prod`, `azure_env_name: prod`
  - Ensure proper secret and permission inheritance

## Verification
Confirm the CI/CD pipeline is fully functional and secure.

- [ ] **Verification 1**: Run setup script for dev environment
  - Execute `./scripts/setup-cicd.sh dev`
  - Verify Azure Service Principal is created or identified
  - Confirm GitHub environment and secrets are configured
  - Check azd environment is initialized

- [ ] **Verification 2**: Run setup script for prod environment
  - Execute `./scripts/setup-cicd.sh prod`
  - Verify separate Service Principal for production
  - Confirm production GitHub environment is isolated

- [ ] **Verification 3**: Test CI workflow on pull request
  - Create a test PR to `main` branch
  - Verify all three jobs run in parallel (backend, frontend, IaC)
  - Confirm tests pass without requiring Azure credentials

- [ ] **Verification 4**: Test dev deployment workflow
  - Push a commit to `main` branch
  - Verify `deploy-dev.yml` triggers automatically
  - Confirm deployment completes successfully
  - Validate application is running in dev environment

- [ ] **Verification 5**: Test prod deployment workflow
  - Trigger workflow manually from GitHub Actions UI
  - Verify confirmation input is required
  - Confirm deployment only proceeds when confirmation is `true`
  - Validate application is running in production environment

- [ ] **Verification 6**: Verify OIDC authentication
  - Check workflow logs to confirm OIDC token is used (no static credentials)
  - Verify Service Principal authentication succeeds
  - Confirm no secrets are exposed in logs

- [ ] **Verification 7**: Test idempotency
  - Re-run setup script for both environments
  - Verify script detects existing resources and doesn't duplicate
  - Confirm no errors occur on subsequent runs
