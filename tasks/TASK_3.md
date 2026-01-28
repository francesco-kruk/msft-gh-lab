# TASK 3 — Implement CI/CD Pipelines with GitHub Actions

## Purpose
Now that we have established a testing strategy in Task 2 and a robust development mode in Task 1, the final step is to automate the delivery of our application. This task focuses on implementing Continuous Integration and Continuous Deployment (CI/CD) pipelines using **GitHub Actions**, ensuring that every change is tested and deployed efficiently.

## Objective & Desired Outcome
Create a dual-environment CI/CD pipeline (Development and Production) that enforces quality gates.

The outcome should be:
1.  **Two Environments**: Setup for `dev` and `prod` environments using **Reusable Workflows**.
2.  **Automated Pipeline**:
    -   **Pull Request**: Triggers CI (Tests, Linting) without deployment (`ci.yml`).
    -   **Merge to Main**: Automatically deploys to the **Dev** environment (`deploy-dev.yml`).
    -   **Manual Trigger**: Deploys to the **Prod** environment with confirmation (`deploy-prod.yml`).
3.  **Application of Prior Skills**: Utilize the prompting strategies, Agents, and instruction files learned in previous tasks.

## Reminder: Copilot Best Practices
As you execute this task, remember to leverage:
-   **Copilot Instructions**: Use custom markdown files to guide the agent.
-   **Agent Mode**: Use Agents for complex, multi-step planning and generation.
-   **MCP Servers**: Use the GitHub MCP server to interact with your repository resources.

## Follow-Along Instructions

### 1) Preparation - Instructions & Best Practices
-   **Download Instruction File**:
    -   Visit the [awesome-copilot](https://github.com/github/awesome-copilot) repository.
    -   Download the file [github-actions-ci-cd-best-practices.instructions.md](https://github.com/github/awesome-copilot/blob/b1fac0d0a1a30f0137eef2c8cbdc75a14616d24a/instructions/github-actions-ci-cd-best-practices.instructions.md).
    -   Add this file to your `.github/instructions/` folders (e.g., `.github/instructions/github-actions-ci-cd-best-practices.instructions.md`).
-   **Load Context**: Ensure this new instruction file is referenced or active in your Copilot context.

### 2) Update Copilot Instructions
Add the following text to your `.github/copilot-instructions.md` file (in the `## ☁️ Infrastructure & Deployment` section) to ensure Copilot follows the CI/CD best practices.

```markdown
- **Guidance**: When working on GitHub Actions workflows, STRICTLY follow the instructions in `.github/instructions/github-actions-ci-cd-best-practices.instructions.md`.
```

### 3) Install Agents & Tools
-   **GitHub Copilot for Azure**: Install the **GitHub Copilot for Azure** extension. This adds the `@azure` agent, which is an expert in `azd` configuration and Azure resources.
-   **GitHub MCP Server**: Open the Extensions view (`Ctrl+Shift+X`) and search for the **GitHub MCP Server**. Install it to enable deeper integration with GitHub Actions.
-   **Configure**: Ensure these tools are enabled in the Copilot Chat "Attachments" or "Tools" menu.

### 4) Plan Mode - Design CI/CD Strategy
Switch to **Plan Mode** in Copilot Chat to design the pipeline before generating code.

**Prompt:**
> I want to set up a **fully automated** CI/CD pipeline for this Azure project using GitHub Actions and `azd`, where the user only needs to run a single setup script followed by `azd up`.
>
> **Goal:**
> Create a comprehensive plan to set up a modular workflow using **Reusable Workflows**.
>
> **Requirements:**
> 1. **Reusable Deployment Workflow (`.github/workflows/deploy.yml`)**:
>    - Accepts `environment` (e.g., 'dev', 'prod') and `azure_env_name` as inputs.
>    - Handles OIDC login, `azd env select`, `azd provision`, and `azd deploy`.
>
> 2. **Continuous Integration (`.github/workflows/ci.yml`)**:
>    - Trigger: On Pull Requests to `main`.
>    - Steps: Run Unit Tests and Bicep build validation. **DO NOT DEPLOY**.
>
> 3. **Dev Deployment (`.github/workflows/deploy-dev.yml`)**:
>    - Trigger: On push to `main` (Continuous Deployment).
>    - Logic: Calls `deploy.yml` targeting the `dev` environment.
>
> 4. **Prod Deployment (`.github/workflows/deploy-prod.yml`)**:
>    - Trigger: Manual (`workflow_dispatch`) with a required confirmation input.
>    - Logic: Calls `deploy.yml` targeting the `prod` environment.
>
> 5. **Automated Setup Script (`scripts/setup-cicd.sh`)**:
>    - Must detect existing `azd` App Registrations (Backend & Frontend) and store their Client IDs as GitHub Secrets (`BACKEND_API_CLIENT_ID`, `FRONTEND_SPA_CLIENT_ID`).
>    - Creates a Service Principal for GitHub OIDC.
>    - **Crucial**: Must assign the Service Principal as an **Owner** of the App Registrations (or grant `Application.ReadWrite.OwnedBy`) to allow the pipeline to update Redirect URIs.
>
> 6. **Local Development & CI Reliability**:
>    - Include a `postprovision` hook in `azure.yaml` that runs a script (`infra/hooks/postprovision.sh`).
>    - This script must grant the "Cosmos DB Built-in Data Contributor" role to the current principal (user or CI SPN) to prevent RBAC errors during `azd up`.

Review the plan to ensure it covers the GitHub Actions workflow file, the OIDC setup, and the GitHub setup script. Keep refining the plan is needed by interacting with Copilot in Plan Mode.

### 5) Create a Skill for Writing Implementation Plans
Before saving the plan, create a reusable skill that defines how to write structured implementation plans.

-   **Create Directory**: Create `.github/skills/write-structured-implementation-plans/`
-   **Create Skill File**: Create a `SKILL.md` file in this directory.
-   **Frontmatter**: Add frontmatter with `name: write-structured-implementation-plans` (matching the folder name) and `description: ...`
-   **Content**: Define the structure, format, and best practices for writing implementation plans (phases, checkboxes, file locations, etc.).

This skill will be reusable across future tasks and can guide Copilot in creating consistent, well-structured plans.

### 6) Agent Mode (same session) - Save the Plan
Once the plan is created, switch to **Agent Mode** (stay in the same session) to save it.

**Prompt:**
> Write the approved plan from Plan Mode.

Confirm that the agent uses the newly created skill and writes the new plan according to the guidelines.

### 7) Agent Mode (new session) - Implement CI/CD Workflow
Start a **new Copilot session**, switch to **Agent Mode**, and execute the plan by adding it as context.

**Prompt:**
> Implement the steps in `plan/cicd-setup.md` exactly, one step at a time. Create the GitHub Actions workflow files for both dev and prod environments.

### 8) Configure GitHub Actions Secrets
After your infrastructure is provisioned with `azd up`, you need to configure GitHub Actions to authenticate with Azure. To do so, run the setup script generated in the previous step.

Ensure the script is executable (run from the repo root):
```bash
chmod +x ./scripts/setup-cicd.sh
```

**Run the setup script (pass the environment name and Azure location):**
```bash
./scripts/setup-cicd.sh dev swedencentral
```

This script will:
-   Verify your azd environment is configured
-   Create a service principal with federated credentials for OIDC authentication
-   Create the GitHub Environment (if missing) and configure **Environment secrets** (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`) scoped to that environment
-   Set up environment-specific configurations

**Note:** You'll need to run this script once for each environment (dev, prod).
Example:
```bash
./scripts/setup-cicd.sh prod swedencentral
```

### 9) Verification
-   **Check GitHub**: Go to **Settings → Environments**. You should see `dev` and `prod` environments. Click on one to verify that `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, and `AZURE_SUBSCRIPTION_ID` are set as **Environment secrets**.
-   **Test Pipeline**: Create a Pull Request. The `ci` workflow should run tests successfully but NOT deploy.
    -   Merge the PR to `main` → triggers deployment to **dev** environment.
    -   Manually trigger the **prod** deployment workflow → deploys to **prod** environment.
-   **Monitor**: Check the "Actions" tab in your GitHub repository to see the workflow runs.

### 10) Rename Resource Groups (post-migration)
Since this repo previously used a single environment, update the resource group naming to match the new multi-environment convention:
- Update the resource group name in [infra/main.bicep](infra/main.bicep#L37-L42) to `rg-gh-lab-<env>`.
- Re-run `azd provision` (or `azd up`) for each environment to create or migrate the resource group names.

### 11) Agent Mode (new session) - Update Documentation with CI/CD details
Start a **new Copilot session** (Agent Mode) to ensure the documentation reflects the new capabilities.

**Prompt:**
> I have successfully implemented the CI/CD pipelines. Now update the documentation to reflect these changes.
>
> 1.  **Update `README.md`**:
>     -   Add a new section `## CI/CD Pipeline`.
>     -   Describe the workflow: Pull Requests trigger CI (tests), merge to `main` deploys to **Dev**, and **Prod** requires manual approval.
>     -   Explain how to set up the pipeline using `./scripts/setup-cicd.sh <env> <location>`.
>
> 2.  **Update `.github/copilot-instructions.md`**:
>     -   Under `## ☁️ Infrastructure & Deployment`, add a bullet point about the CI/CD pipeline.
>     -   Mention that deployments should primarily happen via GitHub Actions for consistent environments.
>     -   Mention the existence of `dev` and `prod` environments in GitHub.


## Expected Outcome
-   A `.github/workflows/` directory containing your CI/CD workflow definition(s).
-   A `scripts/setup-cicd.sh` script for configuring GitHub Actions secrets.
-   **GitHub Environment secrets** configured (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`) for both `dev` and `prod` environments (not repository secrets).
-   Successful pipeline runs visible in the "Actions" tab of your GitHub repository.
-   Validation that code changes automatically propagate to the correct Azure environment:
    -   Main branch pushes deploy to **dev**
    -   **Prod** deploys only when manually triggered with confirmation

**Note:** The outcome of this task can be checked against the remote branch named `task-3`.
