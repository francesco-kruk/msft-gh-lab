# TASK 1 — Implement Test Mode Backend

## Purpose
In the course of the session, we will implement self-contained end-to-end (E2E) testing using Playwright. To achieve this, we first need to decouple our backend from the live Azure Cosmos DB service. This task focuses on implementing a "Test Mode" that uses an in-memory repository instead of the real database. This allows tests to run locally and reliably without network dependencies or cloud costs.

**Note:** This task is strictly about setting up the application to run with the test storage. We will implement the actual Playwright tests in a later task.

## Objective & Desired Outcome
Modify the backend to support a “test mode”. When this mode is active:
1. The application uses an **In-Memory Repository** instead of Cosmos DB.
2. The app starts locally without Azure credentials.
3. The Cosmos DB implementation remains intact for production.

**Note:** The outcome of this task can be found in the remote branch named `task-1`.

Specifically, you will:
- Create an interface/abstraction for data access.
- Move existing Cosmos DB logic into a concrete implementation of that interface.
- Create a new In-Memory implementation (e.g., using a Python dictionary or list).
- Use an environment variable (e.g., `STORAGE_MODE=memory`) to select the implementation at runtime.

## Ways to Engage with Copilot
Use these engagement styles during the task:

### Pro-Code / Inline
- **Ghost text**: Accept or reject line-level suggestions as you type.
- **Next Edit Suggestion**: Jump to Copilot’s next suggested change (good for repetitive refactors).
- **Comment-driven autocomplete**: Write a brief comment describing a function/class and let Copilot expand it.
- **Inline Chat (Ctrl+I / Cmd+I)**: Ask for small, local edits in a single file.

### Guided / Chat
- **Ask Mode**: Ask Copilot for guidance without applying edits.
- **Edit Mode**: Request edits with a focused instruction (still mostly manual control).
- **Plan Mode**: Ask Copilot to outline a step-by-step plan before changes.

### Hands-Off / Autonomous
- **Agent Mode**: Let Copilot analyze the workspace and make multi-file changes on your behalf.

## Reminder: Modes From Most “Pro‑Code” to Most “Hands‑Off”
1. **Ghost text** — Inline, token-level suggestions while you type.
2. **Next Edit Suggestion** — Navigates to the next suggested edit for refactors.
3. **Comment-driven autocomplete** — Generate code from a natural-language comment.
4. **Inline Chat (Ctrl+I / Cmd+I)** — Localized edits in the current file.
5. **Ask Mode** — Advice only, no edits applied.
6. **Edit Mode** — Generates edits, you review and apply.
7. **Plan Mode** — Produces a plan before any edits.
8. **Agent Mode** — Autonomous multi-file changes with minimal manual effort.

## Follow-Along Instructions (Multi-Mode Sequence)
Use this exact sequence to practice the modes in one continuous session.

### 1) Plan Mode
Open Copilot Chat → switch to **Plan Mode** and use this prompt:

> Create a step-by-step plan to add a test-mode backend with an in-memory repository to this FastAPI app. Include file touch points and environment variable behavior.

Review the plan and ensure it covers repository abstraction, Cosmos implementation, in-memory implementation, and runtime selection.

### 2) Agent Mode (same session) → Write the plan to plan/LOCAL-STORAGE.md
Without refreshing the context, switch to **Agent Mode** and use this prompt:

> Write the approved plan from Plan Mode into plan/LOCAL-STORAGE.md. Keep it concise, ordered, and actionable.

Confirm that plan/LOCAL-STORAGE.md was created and accurately reflects the plan.

### 3) Agent Mode (new session) → Implement the plan step-by-step
Start a **new Copilot session** (fresh context), then switch to **Agent Mode** and use this prompt:

> Implement the steps in plan/LOCAL-STORAGE.md exactly, one step at a time. Make minimal, clear edits and keep Cosmos support intact. Add an in-memory repository and runtime selection via an environment variable. Finish by summarizing how to run the backend in test mode.

## Expected Outcome
**Note:** Copilot’s responses are non-deterministic and may vary between sessions. The exact files and structure might differ, but the core functionality should be similar.

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
