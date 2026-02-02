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
-   **Custom Agents**: Using specific Playwright tester agents.
-   **MCP Servers**: Understanding how Copilot connects to external tools (like the Playwright MCP server).
-   **External Resources**: Visit [awesome-copilot](https://github.com/github/awesome-copilot) to find useful instruction files, prompts, and configuration patterns to import into this repository.

## Follow-Along Instructions (Multi-Mode Sequence)

### 1) Preparation - Copilot Instructions & Awesome Copilot
-   **Generate Instructions**: Click on the gear icon in the Copilot Chat panel and select **"Generate Chat Instructions"**. This will help bootstrap your `.github/copilot-instructions.md`.
-   **Awesome Copilot**: Visit [https://github.com/github/awesome-copilot](https://github.com/github/awesome-copilot).
    -   Download the following files and add them to your `.github` folder (create subfolders like `.github/instructions/`, `.github/prompts/` and `.github/agents/` for maintainability):
        -   [playwright-python.instructions.md](https://github.com/github/awesome-copilot/blob/0b9ad6eaaae33a9316c88ebff139bf5384eb1278/instructions/playwright-python.instructions.md)
        -   [playwright-explore-website.prompt.md](https://github.com/github/awesome-copilot/blob/0b9ad6eaaae33a9316c88ebff139bf5384eb1278/prompts/playwright-explore-website.prompt.md)
        -   [playwright-tester.agent.md](https://github.com/github/awesome-copilot/blob/0b9ad6eaaae33a9316c88ebff139bf5384eb1278/agents/playwright-tester.agent.md)

### 2) Configure Downloaded Files
Now that you've added the Playwright files from awesome-copilot, configure them for optimal performance:

-   **Update Model Selection**: In both `.github/agents/playwright-tester.agent.md` and `.github/prompts/playwright-explore-website.prompt.md`, change the model to `Claude Sonnet 4.5`, `GPT-5.2-Codex`, or a similarly powerful model.
-   **Scope Instructions Correctly**: In `.github/instructions/playwright-python.instructions.md`, update the `applyTo` pattern from `'**'` to `'{**/test_*.py,**/*_test.py,**/tests/**/*.py}'`. This ensures the Playwright Python instructions only apply to Python test files, not the entire repository (including your TypeScript frontend).
-   **Use Python for Tests**: In `.github/agents/playwright-tester.agent.md`, update the Test Generation responsibility to use **Python** instead of TypeScript. Change the line to: `"start writing well-structured and maintainable Playwright tests using Python based on what you have explored."`

### 3) Update Copilot Instructions
Add the following text to your `.github/copilot-instructions.md` file to ensure Copilot follows the Playwright best practices when writing tests. You can add it at the end of the file.

```markdown
## 🧪 Testing
- **Framework**: Use Playwright with `pytest-playwright` for End-to-End tests.
- **Guidance**: When writing or updating tests, STRICTLY follow the instructions in `.github/instructions/playwright-python.instructions.md`.
```

### 4) Install Playwright MCP
Add the Playwright MCP in VS Code through the UI by clicking on Extensions on the left side panel or by pressing `Ctrl+Shift+X` and then typing `@mcp Playwright` in the search bar. Find and install the Playwright server on top of the list (ensure it is the one issued by Microsoft).

After installation, ensure the MCP server is enabled by clicking on the wrench and screwdriver icon next to the model selection in the Copilot Chat UI and selecting the `microsoft/playwright-mcp` tool.

**Note:** Ensure you have a browser installed for Playwright to use. You may need to run `npx playwright install chromium`, `npx playwright install chrome` or similar in your terminal if you haven't already.

### 5) Explore with Prompt
Open Copilot Chat and switch to **Agent Mode**. Use the custom prompt you downloaded to explore the running application and generate a test plan:

> /playwright-explore-website Run this prompt against http://localhost:3000 to explore the app and propose a test plan.

**Note:** After running this prompt, confirm that Copilot is using `.github/copilot-instructions.md` and potentially `.github/instructions/playwright-python.instructions.md`. You can check this by looking at the context indicator in the Copilot Chat panel (the paperclip icon or "Used references" section) to ensure relevant instruction files are loaded as context.

Review the output. Copilot will use the Playwright MCP to click through your app and suggest a testing strategy.

### 6) Custom Agent - Test Review & Generation
Select the custom agent `Playwright Tester Mode` by clicking the chat participant dropdown in the Copilot Chat panel (or type `@playwright-tester` in the chat). Then, run the following prompt:

> Review the generated test plan and add any missing tests if necessary. If valid, set up the test environment and generate a robust E2E test file in `tests/e2e/test_devices.py` using **Python with pytest-playwright**. The tests should verify that a user can:
> 1. Open the frontend at localhost:3000
> 2. Add a new device with name, type, and optional assigned user
> 3. See the device appear in the list
> 4. Edit the device details
> 5. Delete the device with confirmation dialog
>
> Include proper fixtures for app navigation and clean state management. Use role-based locators (get_by_role, get_by_label) as per Playwright best practices.

Also generate a `tests/requirements.txt` file with the test dependencies (`pytest`, `pytest-playwright`, `playwright`).

### 7) Verification / Running
Ask Copilot how to run the tests.
> How do I run these tests against my local stack?

**Typical steps to run the generated tests:**

1.  **Install Python Dependencies**:
    ```bash
    pip install -r tests/requirements.txt
    ```

2.  **Install Playwright Browsers**:
    ```bash
    playwright install chromium
    ```

3.  **Start the Application**:
    -   **Backend** (Terminal 1):
        ```bash
        cd backend
        # Ensure your virtual environment is active if using one
        STORAGE_MODE=memory uv run uvicorn src.main:app --reload
        ```
    -   **Frontend** (Terminal 2):
        ```bash
        cd frontend
        npm run dev
        ```

4.  **Run Tests** (Terminal 3):
    ```bash
    cd tests
    pytest
    ```

## Expected Outcome
-   **Test Directory**: A dedicated directory for tests (e.g., `tests/e2e/`) containing the test scenarios.
-   **Dependencies File**: A `requirements.txt` (or update to `pyproject.toml`) in the `tests/` folder listing `pytest` and `pytest-playwright`.
-   **Test Implementation**: A properly structured test file (likely `test_devices.py` or similar) that:
    -   Uses Playwright fixtures (`page`, `expect`).
    -   Implements tests for Creating, Reading, Updating, and Deleting (CRUD) devices.
    -   Handles browser interaction logic (clicking, typing, alerts).
-   **Successful Execution**: The tests run and pass against the local environment (`localhost:3000`).


**Note:** The outcome of this task can be found in the remote branch named `task-2`.
