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

## Workshop Checkpoints

This repository includes checkpoint branches for each task. If you need to catch up or start fresh from a specific point, use the commands below.

### Load a Checkpoint (discard local changes)

```bash
git stash && git switch task-1   # After completing Task 1
git stash && git switch task-2   # After completing Task 2
git stash && git switch task-3   # After completing Task 3
git stash && git switch task-4   # After completing Task 4
```

### Load a Checkpoint (keep local changes)

If you want to preserve your current work before switching:

```bash
git add -A && git stash save "my work on task X"
git switch task-1
```

To recover your stashed work later: `git stash pop`

### Reset to a Clean Checkpoint

If you want to completely discard all local changes and reset to a checkpoint:

```bash
git checkout -- . && git clean -fd && git switch task-1
```

### Available Checkpoints

| Branch   | Description                          |
|----------|--------------------------------------|
| `main`   | Starting point                       |
| `task-1` | Completed Task 1                     |
| `task-2` | Completed Task 2                     |
| `task-3` | Completed Task 3                     |
| `task-4` | Completed Task 4 (final solution)    |
