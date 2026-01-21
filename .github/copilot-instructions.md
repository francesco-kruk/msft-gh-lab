# Copilot Instructions for Inventory Management App

## 🏗 Project Architecture
This is a monorepo containing a full-stack application deployed to Azure Container Apps.
- **Frontend**: React + Vite + TypeScript (`/frontend`)
- **Backend**: Python FastAPI with `uv` (`/backend`)
- **Infrastructure**: Azure Bicep managed by `azd` (`/infra`, `azure.yaml`)
- **Database**: Azure Cosmos DB (NoSQL)

## 🔧 Backend Development (`/backend`)
- **Framework**: FastAPI with Pydantic models.
- **Dependency Management**: Uses `uv`. Always check `pyproject.toml`.
- **Repository Pattern**: 
  - **CRITICAL**: Never access DB directly in routes. Use `src.repositories` module methods.
  - **Interface**: Define new data operations in `src.repositories.base.DeviceRepository`.
  - **Dual Implementation**: You **MUST** implement both `CosmosDeviceRepository` (prod) and `InMemoryDeviceRepository` (test/dev) for any new data method.
  - **Factory**: `src.repositories.factory.py` switches implementations based on `STORAGE_MODE`.
- **Running Locally**:
  ```bash
  cd backend
  uv sync
  STORAGE_MODE=memory uv run uvicorn src.main:app --reload
  ```

## ⚛️ Frontend Development (`/frontend`)
- **Structure**: React/Vite + TypeScript.
- **API Communication**: 
  - API base URL is defined by `VITE_API_URL` or defaults to `/api`.
  - **Dev**: `vite.config.ts` proxies `/api` requests to `http://localhost:8000`.
  - **Prod**: Nginx (`nginx.conf.template`) rewrites `/api/*` to the backend container URL.
- **Running Locally**:
  ```bash
  cd frontend
  npm install
  npm run dev
  ```

## ☁️ Infrastructure & Deployment (`/infra`)
- **Tooling**: Uses Azure Developer CLI (`azd`). `azure.yaml` describes the service map.
- **Deployment**: `azd up` provisions resources and deploys code.
- **Environment**: Backend relies on System-Assigned Managed Identity to access Cosmos DB (RBAC).
- **Automation**: The user should be able to set up everything automatically by running `azd up` without the need to run additional scripts manually.
- **CI/CD**: Deployments should primarily happen via GitHub Actions for consistent environments. The project uses `dev` and `prod` environments in GitHub.
- **Guidance**: When working on GitHub Actions workflows, STRICTLY follow the instructions in `.github/instructions/github-actions-ci-cd-best-practices.instructions.md`.

## 📝 Coding Conventions
- **Pydantic**: Use `src.schemas.py` for all DTOs.
- **Async/Await**: The entire backend stack is async. Ensure all DB operations are awaited.
- **Logging**: Use standard Python `logging`.
- **Error Handling**: Raise `HTTPException` in routes, but allow Repositories to raise standard Python exceptions or return `None`.

## 📍 Key Files
- **Service definitions**: [`azure.yaml`](azure.yaml)
- **Repo Interface**: [`backend/src/repositories/base.py`](backend/src/repositories/base.py)
- **Data Schemas**: [`backend/src/schemas.py`](backend/src/schemas.py)
- **Frontend Proxy**: [`frontend/vite.config.ts`](frontend/vite.config.ts)

## 🧪 Testing
- **Framework**: Use Playwright with `pytest-playwright` for End-to-End tests.
- **Guidance**: When writing or updating tests, STRICTLY follow the instructions in `.github/instructions/playwright-python.instructions.md`.