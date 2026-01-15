# TASK 2 — Implement End-to-End Testing with Playwright

## Purpose
Now that we have successfully decoupled the backend and implemented a "Test Mode" (Task 1), we can proceed to implement rigorous End-to-End (E2E) testing. This task focuses on using **Playwright** to simulate user interactions and verify that the application works correctly from the user's perspective.

In this task, we will also explore advanced ways to customize and guide Copilot to generate better code and tests, leveraging instruction files and custom prompts.

## Objective & Desired Outcome
Set up a robust E2E testing framework using Playwright (Python or Node.js versions are both acceptable, but we'll focus on Python to match the backend language).

The outcome should be:
1.  **Playwright Installed & Configured**: A usable Playwright setup in the repo.
2.  **E2E Test Suite**: At least one complete test scenario verifying the core functionality:
    -   Create a device.
    -   List devices and verify the new device is present.
    -   Delete the device and verify it is gone.
3.  **Instruction & Prompt Usage**: You will use Copilot Instructions and Custom Prompts to generate this code efficiently.

## Ways to Engage with Copilot
This task emphasizes **Customization & Advanced Context**. The main ways to engage with Copilot highlighted in this task are:

-   **Copilot Instructions**: Refining the `.github/copilot-instructions.md` file to include testing preferences.
-   **Custom Prompts**: Creating reusable prompts for generating tests.
-   **Custom Agents**: Using specific agents (like `@azure` if needed, though standard `@workspace` is primary here).
-   **MCP Servers**: Understanding how Copilot connects to external tools (like the file system or database, implicitly).
-   **External Resources**: Visit [awesome-copilot](https://github.com/github/awesome-copilot) to find useful instruction files, prompts, and configuration patterns to import into this repository.

## Follow-Along Instructions (Multi-Mode Sequence)

### 1) Preparation - Awesome Copilot
Visit [https://github.com/github/awesome-copilot](https://github.com/github/awesome-copilot).
-   Look for "Instructions" or "Prompts" related to testing, Python, or Playwright.
-   *Optional*: Copy relevant patterns into your `.github/copilot-instructions.md` to teach Copilot how you like your tests structured (e.g., "Always use `pytest` fixtures," "Use Page Object Model").

### 2) Plan Mode
Open Copilot Chat → switch to **Plan Mode** and use this prompt:

> Plan the setup of Playwright for Python in this workspace. We want to test the full E2E flow (create, list, delete device) against the locally running app (frontend+backend in test mode). Include necessary `pip` installs and folder structure.

Review the plan. It should include installing `playwright` and `pytest-playwright`, running `playwright install`, and creating a `tests/e2e/` directory.

### 3) Agent Mode - Setup & Implementation
Switch to **Agent Mode** and use a prompt similar to this:

> Execute the plan to set up Playwright. Then, write a robust E2E test file in `tests/e2e/test_devices.py`. It should verify that a user can open the frontend, add a new device, see it in the list, and delete it. Assume the app is running on localhost:5173.

### 4) Verification / Running
Ask Copilot how to run the tests.
> How do I run these tests against my local stack?

(You will likely need to start the backend in one terminal with `STORAGE_MODE=memory` and the frontend in another, then run `pytest` in a third).

## Expected Outcome
-   **New Directory**: `tests/e2e/` (or similar) containing the tests.
-   **Dependencies**: `playwright` added to a requirements file (or `pyproject.toml`) or just installed.
-   **Test File**: A Python file (e.g., `test_devices.py`) using `playwright.sync_api` or `async_api`.
-   **Working Test**: The test passes when the app is running locally.

**Note:** The outcome of this task can be found in the remote branch named `task-2`.
