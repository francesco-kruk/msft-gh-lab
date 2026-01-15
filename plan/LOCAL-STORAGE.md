# Plan: Test-Mode Backend (In-Memory Repository)

1. Review current backend flow to confirm repository usage and app lifecycle in backend/src/main.py, db/cosmos.py, repositories/, and schemas.py.
2. Define a repository interface and factory for selecting the implementation (Cosmos vs in-memory) under backend/src/repositories/.
3. Move existing Cosmos logic into a concrete Cosmos repository implementation without behavior changes.
4. Add an in-memory repository implementation using a simple in-process store (dict/list) that mirrors CRUD behavior.
5. Wire the factory into the API so route handlers call the selected repository.
6. Make Cosmos initialization conditional on storage mode; skip Cosmos client setup in test mode.
7. Document environment variable behavior:
   - STORAGE_MODE=memory uses in-memory repo and does not require Cosmos env vars.
   - STORAGE_MODE=cosmos or unset uses Cosmos repo and keeps current Cosmos env requirements.
8. Update task documentation or README to describe how to run the backend in test mode.