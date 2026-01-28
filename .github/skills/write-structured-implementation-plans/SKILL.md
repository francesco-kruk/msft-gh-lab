---
name: write-structured-implementation-plans
description: Defines how to write and structure implementation plans with consistent location, naming, and format using phases and checkboxes
---

# Writing Structured Implementation Plans

This skill defines how to write and structure implementation plans for development tasks. Plans should be saved in a consistent location with descriptive names and follow a clear, actionable format.

## When to Use
Use this skill when asked to:
- Create a plan for implementing a feature
- Document a step-by-step approach for a task
- Write an implementation strategy
- Generate a development roadmap

## Instructions

### File Location and Naming
1. **Directory**: Always save plan files in the `plan/` directory at the workspace root
2. **Naming Convention**: Use kebab-case filenames that clearly describe the plan's purpose
   - Format: `<purpose-description>.md`
   - Examples:
     - `local-storage.md` for local storage implementation plan
     - `e2e-testing.md` for end-to-end testing plan
     - `auth-integration.md` for authentication integration plan
     - `database-migration.md` for database migration plan

### Plan Structure
Each plan should follow this hierarchical structure:

```markdown
# [Plan Title]

## Overview
Brief description of what this plan accomplishes and why.

## Phase 1: [Phase Name]
Brief description of this phase's goal.

- [ ] **Task 1.1**: [Task description]
  - Details, files affected, or approach
  - Any prerequisites or dependencies

- [ ] **Task 1.2**: [Task description]
  - Details, files affected, or approach

## Phase 2: [Phase Name]
Brief description of this phase's goal.

- [ ] **Task 2.1**: [Task description]
  - Details, files affected, or approach

- [ ] **Task 2.2**: [Task description]
  - Details, files affected, or approach

## Verification
Steps to verify the implementation is complete and working correctly.

- [ ] **Verification 1**: [What to verify]
- [ ] **Verification 2**: [What to verify]
```

### Format Requirements

#### Checkboxes
- Every task MUST start with `- [ ]` for tracking completion
- Use checkboxes for both implementation tasks and verification steps

#### Phases
- Group related tasks into logical phases
- Each phase should have a clear objective
- Phases should be numbered sequentially (Phase 1, Phase 2, etc.)
- Adapt the number of phases to the complexity of the plan

#### Tasks
- Number tasks hierarchically (1.1, 1.2, 2.1, 2.2, etc.)
- Use **bold** for task titles to improve readability
- Include relevant details below each task (indented):
  - Files that will be created or modified
  - Key implementation approaches
  - Dependencies on other tasks
  - Environment variables or configuration changes

#### Content Guidelines
- Keep task descriptions concise but actionable
- Focus on what needs to be done, not how to do it in detail
- Include file paths using relative paths from workspace root
- Mention key technologies, patterns, or frameworks involved
- Ensure tasks are ordered logically based on dependencies

### Adaptability
While maintaining the core structure (phases → tasks with checkboxes):
- Adjust the number of phases based on plan complexity
- Tailor phase names to the specific domain (e.g., "Backend Changes", "Frontend Updates", "Infrastructure")
- Include additional sections if needed (e.g., "Prerequisites", "Rollback Plan", "Testing Strategy")
- Adapt the level of detail to match the plan's scope

## Example Output

```markdown
# Test Mode Backend Implementation Plan

## Overview
Implement a test mode for the backend that uses in-memory storage instead of Cosmos DB, enabling local development and testing without Azure dependencies.

## Phase 1: Repository Abstraction
Create a repository interface to decouple storage implementation from business logic.

- [ ] **Task 1.1**: Create abstract base class
  - File: `backend/src/repositories/base.py`
  - Define interface with methods: list_devices, get_device, create_device, update_device, delete_device

- [ ] **Task 1.2**: Move Cosmos DB logic to concrete implementation
  - File: `backend/src/repositories/cosmos_repository.py`
  - Migrate existing code from `backend/src/db/cosmos.py`
  - Implement base class interface

## Phase 2: In-Memory Implementation
Create a test-friendly storage implementation using Python data structures.

- [ ] **Task 2.1**: Create in-memory repository class
  - File: `backend/src/repositories/memory_repository.py`
  - Use Python dictionary for storage
  - Implement all base class methods

- [ ] **Task 2.2**: Add repository factory
  - File: `backend/src/repositories/factory.py`
  - Create factory function that returns repository based on STORAGE_MODE environment variable
  - Default to Cosmos DB if not specified

## Phase 3: Application Integration
Update the FastAPI application to use the repository abstraction.

- [ ] **Task 3.1**: Update main.py
  - File: `backend/src/main.py`
  - Use factory to get repository instance
  - Skip Cosmos DB initialization when STORAGE_MODE=memory

- [ ] **Task 3.2**: Update repository module exports
  - File: `backend/src/repositories/__init__.py`
  - Export factory function and base class

## Verification
Confirm the implementation works correctly in both modes.

- [ ] **Verification 1**: Start backend with STORAGE_MODE=memory and verify it runs without Azure credentials
- [ ] **Verification 2**: Test CRUD operations work correctly in memory mode
- [ ] **Verification 3**: Verify production mode still works with Cosmos DB
- [ ] **Verification 4**: Confirm data doesn't persist between restarts in memory mode
```

## Notes
- Plans are living documents - they can be updated as implementation progresses
- The checkbox format (`- [ ]`) enables easy progress tracking
- Clear phase separation helps break down complex tasks
- Include verification steps to ensure quality
