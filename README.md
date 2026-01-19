# Inventory Management App

A simple inventory management application built with React and FastAPI, deployed to Azure Container Apps.

<img alt="image" src="https://github.com/user-attachments/assets/6ed5515b-8d31-436a-ac79-41aee1743d88" />



## Features

- Add new devices to inventory
- Edit device information (name, assigned to)
- View all devices
- Delete devices

## Tech Stack

- **Frontend**: React + Vite + TypeScript
- **Backend**: Python FastAPI with uv
- **Database**: Azure Cosmos DB (NoSQL)
- **Hosting**: Azure Container Apps

## Prerequisites

- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
- [Docker](https://www.docker.com/get-started)
- Azure subscription

## Local Development

### Backend
```bash
cd backend
uv sync
STORAGE_MODE=memory uv run uvicorn src.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Deploy to Azure

```bash
azd up
```

This single command will:
1. Provision all Azure resources (Container Apps, Cosmos DB, Container Registry)
2. Build and push Docker images
3. Deploy frontend and backend (backend uses System-Assigned Managed Identity)
4. Assign RBAC roles for the backend to access Cosmos DB

### Requirements for `azd up`

- Be logged in to Azure: 
  
  ```bash
  azd auth login
  ```

## CI/CD Pipeline

The project includes a comprehensive CI/CD pipeline using GitHub Actions.

### Workflow
1. **Pull Requests**: Triggers the CI pipeline which runs tests to validate changes.
2. **Merge to `main`**: Automatically deploys the changes to the **Dev** environment.
3. **Production Release**: Deploying to **Prod** requires manual approval in GitHub Actions.

### Setup
You can set up the required Azure resources and GitHub secrets for the pipeline using the provided script:

```bash
./scripts/setup-cicd.sh <env> <location>
```

For example:
```bash
./scripts/setup-cicd.sh dev eastus2
```

## Environment Variables

The deployment sets and uses the following:
- `BACKEND_URL`: Backend API endpoint for the frontend
- `COSMOS_ENDPOINT`: Cosmos DB account endpoint
- `COSMOS_DB_NAME`: Database name (default: `inventory`)
- `COSMOS_DEVICES_CONTAINER`: Container name (default: `devices`)
- `STORAGE_MODE`: Set to `memory` to use the in-memory repository (no Cosmos env vars required). Defaults to `cosmos`.

## Architecture

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Frontend   │─────>│   Backend    │─────>│  Cosmos DB   │
│ (React App)  │      │  (FastAPI)   │      │   (NoSQL)    │
└──────────────┘      └──────────────┘      └──────────────┘
  Container App         Container App         Serverless
```
