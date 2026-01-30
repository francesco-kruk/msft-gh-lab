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

## Open in Codespaces

Use the devcontainer for a ready-to-deploy environment with Azure tooling preinstalled.

- Quickstart and troubleshooting: [.devcontainer/README.md](.devcontainer/README.md)
- Golden path: `azd auth login` → `azd env new` → `azd env set AZURE_LOCATION <region>` → `azd up`

## Local Development

### Backend
```bash
cd backend
uv sync
uv run uvicorn src.main:app --reload
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

## Environment Variables

The deployment sets and uses the following:
- `BACKEND_URL`: Backend API endpoint for the frontend
- `COSMOS_ENDPOINT`: Cosmos DB account endpoint
- `COSMOS_DB_NAME`: Database name (default: `inventory`)
- `COSMOS_DEVICES_CONTAINER`: Container name (default: `devices`)

## Architecture

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Frontend   │─────>│   Backend    │─────>│  Cosmos DB   │
│ (React App)  │      │  (FastAPI)   │      │   (NoSQL)    │
└──────────────┘      └──────────────┘      └──────────────┘
  Container App         Container App         Serverless
```
