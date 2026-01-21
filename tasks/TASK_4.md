# TASK 4 — Implement Dark and Light Mode

## Purpose
Move the system from a basic development deployment to a **production-ready** state. To achieve this, we will implement a polished Dark/Light mode toggle, enhancing user experience and demonstrating application maturity. This task leverages **GitHub Copilot Agents**—specifically the **Coding Agent** and **Code Review Agent**—to handle feature implementation and code quality checks autonomously, ensuring the code meets production standards.

## Objective & Desired Outcome
Add a UI toggle component to the frontend application that switches the theme.
1. Create a toggle button positioned in the **top right corner** of the header or navigation bar.
2. Configure the button to display a **sun icon** ☀️ when in light mode and a **half-moon icon** 🌙 when in dark mode.
3. Implement logic to handle theme switching (light/dark).
4. Ensure the preference is applied to the UI elements.

**Note:** The outcome of this task is a fully functional theme switcher implemented via an autonomous agent workflow starting from a GitHub Issue.

## Ways to Engage with Copilot
In this task, we focus purely on the **Agentic** workflow within GitHub functionality:
- **Issue Creation**: Using Copilot to draft a structured feature request.
- **Coding Agent**: Assigning the task to Copilot to write the code.
- **Code Review Agent**: Utilizing automated reviews for the generated Pull Request.

## Follow-Along Instructions

### Step 1: Create the Feature Request using Copilot
1. Open [GitHub Copilot](https://github.com/copilot) and select the right repository.
2. Click on **"Create issue"** or type `/create-issue` in the chat interface.
3. Add an appropriate prompt to describe the feature:
   > "Implement a dark and light mode toggle for the frontend application. It should be positioned in the top right corner. The button should show a sun icon when in light mode and a half-moon icon when in dark mode. It should update the background and text colors appropriate for each mode. The new feature should be implemented followign the current structure, frameworks, and style of the project."
4. Review the generated issue description and click **Create issue**.

### Step 2: Delegate Implementation to Copilot
1. Open the issue you just created in the repository.
2. **Assign the issue to Copilot**.
   - This triggers the **Coding Agent** to analyze your codebase, plan the implementation, and automatically create a Pull Request with the necessary changes.

### Step 3: Review with Code Review Agent
1. Navigate to the Pull Request created by the Coding Agent.
2. Observe the **Code Review Agent** (or Copilot's review summary) providing feedback or approval on the generated code.
3. Once the checks pass and you are satisfied with the implementation, merge the Pull Request.
4. Verify the toggle works in the deployed or local application.

## Expected Outcome
-   **Theme Toggle Component**: A new React component (e.g., `ThemeToggle.tsx`) integrated into the header or navigation.
-   **Iconography**: The button correctly displays a Sun icon in light mode and a Moon icon in dark mode.
-   **State Persistence**: The user's theme preference is saved (e.g., in `localStorage`) and persists across page reloads.
-   **Styling**: The application applies appropriate background and text colors for both modes.
-   **Agent Workflow**: The feature is implemented via the GitHub Copilot Agent workflow (Issue -> PR).

**Note:** The outcome of this task can be found in the remote branch named `task-4`.