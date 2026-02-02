# TASK 0 — Initial Application Deployment

## Purpose
Before we start modifying code or refactoring, we must verify that the base application works as expected in the target environment. This task focuses on deploying the initial state of the Inventory Management App to Azure using the Azure Developer CLI (`azd`). This ensures your Azure subscription, resource quotas, and local tools are correctly configured.

**Note:** This task is about validating the infrastructure-as-code and deployment pipeline.

## Objective & Desired Outcome
Deploy the current application to Azure.
1. Authenticate with Azure.
2. Provision all required resources (Resource Group, Cosmos DB, Container Registry, Container Apps Environment, Container Apps).
3. Build and deploy the Docker containers for Frontend and Backend.
4. Verify the running application in the browser.

**Desired Outcome:** A fully functional app running on Azure with a public URL.

## Ways to Engage with Copilot
Use these engagement styles during the task:

### Guided / Chat
- **Ask Mode**: "What does `azd up` do?" or "How do I login to Azure with azd?"
- **Terminal Integration**: If a command fails, use the sparkle icon (Explain) in the terminal to have Copilot diagnose the error.

### Hands-Off / Autonomous
- **Agent Mode**: Ask Copilot to "Deploy this app to Azure" (though for this specific task, running the command yourself is often faster for learning).

## Reminder: Modes From Most “Pro‑Code” to Most “Hands‑Off”
1. **Ghost text** — Inline, token-level suggestions while you type.
2. **Next Edit Suggestion** — Navigates to the next suggested edit for refactors.
3. **Comment-driven autocomplete** — Generate code from a natural-language comment.
4. **Inline Chat (Ctrl+I / Cmd+I)** — Localized edits in the current file.
5. **Ask Mode** — Advice only, no edits applied.
6. **Edit Mode** — Generates edits, you review and apply.
7. **Plan Mode** — Produces a plan before any edits.
8. **Agent Mode** — Autonomous multi-file changes with minimal manual effort.

## Follow-Along Instructions

### 1. Fork the Repository
1. Navigate to the original repository on GitHub.
2. Click the **Fork** button in the top-right corner.
3. Select your GitHub account as the destination for the fork.

### 2. Open the Repository

Choose one of the following options:

#### Option A: Open in GitHub Codespaces (Recommended)
1. Go to your forked repository on GitHub.
2. Click the green **Code** button.
3. Select the **Codespaces** tab.
4. Click **Create codespace on main**.
5. Wait for the Codespace to initialize (this may take a few minutes).

#### Option B: Clone Locally
1. Go to your forked repository on GitHub.
2. Click the green **Code** button and copy the repository URL.
3. Open a terminal and run:

```bash
git clone <your-forked-repo-url>
cd <repo-name>
```

4. Open the cloned folder in VS Code:

```bash
code .
```

### 3. Authenticate with Azure
If you haven't already, log in to your Azure account.

```bash
azd auth login
```

### 4. Initialize and Deploy
Run the single command that provisions resources and deploys the code.

```bash
azd up
```

- You will be asked to select an **Environment Name**. Choose something unique (recommended: `dev-<your-alias>`).
- You will be asked to select an **Azure Subscription**. Choose the one you set up in the prerequisites.
- You will be asked to select an **Azure Location**. Choose a region close to you (recommended: `swedencentral`).

**Note:** This process may take 5–10 minutes as it creates Cosmos DB and other resources.

### 5. Verify Deployment
Once `azd up` completes, it will print a URL (e.g., `https://ca-web-...containerapps.io`).
- Click the URL to open the application.
- Verify that you can see the inventory list (it might be empty initially).
- Try adding a test item to ensure the database connection works.

### Troubleshooting with Copilot
If you encounter an error during deployment (e.g., "Subscription not found" or "Quota exceeded"):
1. **Select the error message** in the terminal.
2. Right-click and choose **Copilot > Explain This**.
3. Or type `@terminal` in the Chat view and paste the error.
