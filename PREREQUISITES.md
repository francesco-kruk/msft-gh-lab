# Prerequisites (Walkthrough)

This page walks you through setting up everything you need before starting the labs.

## Quick checklist

You’re ready when you can check all of these:

- [ ] I have an **external tenant** and an **Azure subscription** set up (per the request process)
- [ ] My **GitHub account** is linked to (or can authenticate with) my **Microsoft account**
- [ ] I have an **Azure subscription** and can create resources (at least **Contributor** access)

Optional, only needed if not using Codespaces:

- [ ] I have **GitHub Copilot** enabled and the **VS Code extension** installed
- [ ] I have **GitHub Copilot Chat** enabled and the **VS Code extension** installed
- [ ] I have **VS Code**, **Git**, and **Docker** installed locally
- [ ] I have **Node.js** installed (18+, recommended 20 LTS)
- [ ] I have `uv` installed (and can provision **Python 3.11+**)

---

## 1) External tenant + Azure subscription (request)

For this lab, you should use an **external tenant** and an **Azure subscription** created via the official request process.

### Follow the request instructions

- Request your Azure subscription here (follow the steps in the page):
	- https://microsoft.sharepoint.com/teams/Security-EndpointProtection/SitePages/Request-your-Azure-Subscription.aspx?web=1

This SharePoint page already includes screenshots, so they are not duplicated here.

### Verify

- You can sign in to https://portal.azure.com with the account used in the request.
- Under **Subscriptions**, you can see the newly created/assigned subscription.
- You can create a **Resource group** in that subscription.

---

## 2) GitHub account linked to a Microsoft account

This lab expects you to authenticate and access GitHub resources using an identity linked to Microsoft.

### Setup steps (high level)

1. Ensure you can sign in to GitHub at https://github.com using your intended account.
2. Confirm the email on your GitHub account matches (or can be associated with) your Microsoft identity.
3. If your organization uses Microsoft Entra ID SSO:
	- Join the GitHub organization when invited.
	- Complete SSO authorization when prompted.

### Verify

- You can access the lab’s GitHub organization and repositories.
- If SSO is required, you can successfully authorize SSO for the org.

---

## 3) Azure subscription

You need an Azure subscription you can deploy resources into.

### Setup steps

1. Sign in to the Azure portal: https://portal.azure.com
2. Confirm you have a subscription available under **Subscriptions**.
3. Confirm your role assignments:
	- You should have at least **Contributor** on the subscription (or on a target resource group).
	- If the lab provisions identity/RBAC, you may need **User Access Administrator** (lab-specific).
4. (Recommended) Install the Azure CLI for local verification: https://learn.microsoft.com/cli/azure/install-azure-cli
5. (Recommended) Sign in via CLI:
	- Run `az login`
	- Run `az account show` and confirm the subscription.

### Verify

- In the Azure portal, you can create a new **Resource group**.
- If using CLI, `az account show` returns the expected subscription.

---

## _Optional steps (needed if not using Codespaces):_

## 4) GitHub Copilot (VS Code extension)

You need a Copilot subscription assigned to your GitHub user, and the VS Code extension installed.

### Setup steps

1. Confirm Copilot is enabled for your GitHub account:
	- Open your GitHub settings and look for **Copilot** (availability depends on your plan/org).
2. Sign in to GitHub from VS Code:
	- In VS Code, run the command **“GitHub: Sign in”** (Command Palette).
3. Confirm Copilot is active:
	- Open a code file and type a few characters; you should see inline suggestions.

### Verify

- In VS Code, Copilot suggestions appear (or Copilot status shows “Ready”).

---

## 5) GitHub Copilot Chat (VS Code extension)

Copilot Chat requires the chat-capable extension and that your Copilot entitlement includes chat.

### Setup steps

1. Install the VS Code extension:
	- Install **GitHub Copilot Chat** from the VS Code Marketplace.
2. Make sure you’re signed in to GitHub in VS Code (same account as Copilot).
3. Open the Copilot Chat panel and send a test prompt.

### Verify

- Copilot Chat responds without entitlement/auth errors.

---

## 6) Local tooling

These labs involve building/running code locally.

### Setup steps

1. Install **VS Code** (latest stable): https://code.visualstudio.com/
2. Install **Git**: https://git-scm.com/downloads
3. Install **Docker** (Desktop on Windows/macOS, Engine on Linux): https://docs.docker.com/get-docker/
4. Install **Node.js** for the frontend:
	- Required: **Node.js 18+**
	- Recommended: **Node.js 20 LTS**
	- Install from: https://nodejs.org/
5. Install **uv** for Python environments and dependencies:
	- Install instructions: https://docs.astral.sh/uv/getting-started/installation/
6. Provision **Python 3.11+** using uv:
	- Example: `uv python install 3.11`

### Verify

- VS Code opens and reports a version: `code --version`
- Git is available: `git --version`
- Docker is available: `docker --version`
- Node and npm are available: `node --version` and `npm --version`
- uv is available: `uv --version`
- uv-managed Python meets the minimum: `uv run python --version`
