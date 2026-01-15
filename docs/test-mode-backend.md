# Backend Test Mode

The backend can run in a self-contained test mode that uses an in-memory repository instead of Azure Cosmos DB. This is useful for local testing and automation.

## Run in Test Mode

From the backend directory:

- Set the storage mode to memory and start the server:
  - STORAGE_MODE=memory uv run uvicorn src.main:app --reload

## Behavior

- STORAGE_MODE=memory uses an in-memory store.
- No Cosmos environment variables are required in test mode.
- Data is not persisted between restarts.

## Default Mode

If STORAGE_MODE is unset or set to cosmos, the backend uses Cosmos DB and requires the Cosmos environment variables.