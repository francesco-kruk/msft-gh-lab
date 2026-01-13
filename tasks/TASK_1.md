# TASK 1 — Implement Test Mode Backend

## Purpose
In the course of the session, we will implement self-contained end-to-end (E2E) testing using Playwright. To achieve this, we first need to decouple our backend from the live Azure Cosmos DB service. This task focuses on implementing a "Test Mode" that uses an in-memory repository instead of the real database. This allows tests to run locally and reliably without network dependencies or cloud costs.

**Note:** This task is strictly about setting up the application to run with the test storage. We will implement the actual Playwright tests in a later task.

## Objective & Desired Outcome
You need to modify the backend to support a "test mode". When this mode is active:
1. The application should use an **In-Memory Repository** implementation for data storage instead of connecting to Cosmos DB.
2. The application should be startable locally in this mode without Azure credentials.
3. The existing Cosmos DB implementation should remain intact for production use.

Specifically, this involves:
- Creating an interface/abstraction for your data access layer.
- Moving the current Cosmos DB logic into a concrete implementation of that interface.
- Creating a new In-Memory implementation (e.g., using a Python dictionary or list).
- Using an environment variable (e.g., `TEST_MODE=true` or `REPOSITORY_TYPE=memory`) to switch implementations at runtime.

## Ways to Complete This Task
You are free to use any method you prefer to reach the goal, depending on your comfort level:

- **Pro-Code**: Use your preferred coding style. You can manually refactor the code, abstract the repository pattern, and implement the in-memory store. Use Copilot Inline Suggestions (`Ctrl+I` / `Cmd+I`) to generate the boilerplate for the new classes.
- **Assisted**: Use Copilot Chat (`Ctrl+Alt+I` / `Cmd+Alt+I`) to ask for a plan ("How do I refactor this FastAPI app to use the Repository pattern?") or specific code snippets.
- **Autonomous (Agent Mode)**: Use Copilot's Agent Mode to plan and implement the changes across multiple files automatically.

## Follow-Along Instructions
If you have less coding experience or want to see the Agent in action, use the following steps:

1. Open **Copilot Chat** (Agent Mode).
2. In the model picker, select **Claude Sonnet 4.5**.
3. Input the following prompt exactly:

    > I want to implement self-contained end-to-end testing using Playwright. For that, implement a “test mode” backend storage option (in-memory repository) so tests don’t depend on Cosmos and start the app locally. Ignore the actual e2e testing for now.

4. **Review**: The Agent will analyze your workspace (`backend/src/`) and propose a plan. It will likely suggest creating a `Repository` abstract base class and two subclasses (`CosmosRepository`, `InMemoryRepository`).
5. **Approve**: Click to apply the edits.
6. **Verify**: Once finished, the Agent should tell you how to run the app in test mode. Try starting the backend (e.g., `./run-backend-test-mode.sh` or `STORAGE_MODE=test uvicorn src.main:app --reload`) and check if it runs without errors.

## Expected Outcome

**Note:** Copilot's responses are non-deterministic and may vary between sessions. The exact files and structure might differ, but the core functionality should be similar.

### Core Implementation (Required)
The agent should create or modify these key files in `backend/src/repositories/`:

- **Abstract Base Class** (e.g., `base.py` or `repository.py`) - Defines the repository interface with methods like `list_devices()`, `get_device()`, `create_device()`, `update_device()`, `delete_device()`
- **Cosmos DB Implementation** (e.g., `cosmos_repo.py` or `cosmos_repository.py`) - Preserves existing Cosmos DB logic, moved from `__init__.py`
- **In-Memory Implementation** (e.g., `memory.py`, `inmemory_repo.py`, or `test_repository.py`) - New implementation using Python dictionaries for storage
- **Factory or Selection Logic** (e.g., `factory.py` or integrated in `__init__.py`) - Switches between implementations based on environment variables
- **Updated `__init__.py`** - Modified to use the factory pattern and delegate to the selected implementation
- **Updated `main.py`** - Modified to conditionally initialize Cosmos DB only when not in test mode

### Environment Variable
The implementation should use an environment variable to control the mode, such as:
- `STORAGE_MODE=test` or `STORAGE_MODE=memory` for in-memory storage
- `STORAGE_MODE=cosmos` or unset for Cosmos DB (default/production)

Alternative variable names the agent might use: `TEST_MODE`, `REPOSITORY_TYPE`, `DB_MODE`, etc.

### Additional Files (Optional but Likely)
The agent may also generate supporting files such as:
- **Shell scripts** (e.g., `run-backend-test-mode.sh`) - Convenience script to start the backend in test mode
- **Python test/validation scripts** (e.g., `test-backend-testmode.py`) - Script to verify the implementation works
- **Docker Compose configuration** (e.g., `docker-compose.test.yml`) - For running both frontend and backend in test mode
- **Documentation files** - Such as `TEST_MODE_README.md`, `QUICKSTART.md`, architecture diagrams, implementation summaries, Playwright setup examples, etc.

### Verification Steps
To verify the implementation works:

1. **Check files exist**: Verify the core repository files were created in `backend/src/repositories/`
2. **Start in test mode**: Run the provided startup command (check agent's output for exact command)
3. **Check logs**: Confirm you see messages like "Running in test mode" or "Using in-memory storage"
4. **Test health endpoint**: `curl http://localhost:8000/health` should return `{"status":"healthy"}`
5. **Test CRUD operations**: Use the validation script if provided, or manually test creating/reading/deleting devices
6. **Verify isolation**: Data should not persist between restarts (restart the backend and confirm devices are gone)

The app should start locally without Azure credentials and function identically to the Cosmos DB version, but using in-memory storage.
