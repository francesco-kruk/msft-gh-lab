# End-to-End Tests for Device Management

This directory contains comprehensive end-to-end (E2E) tests for the Device Management application using Playwright with Python.

## Test Suite Overview

The E2E tests in `test_devices.py` verify the complete user workflow:

1. **Opening the application** - User navigates to the frontend
2. **Adding a new device** - User fills in the form and creates a device
3. **Viewing devices** - User sees the device appear in the list
4. **Editing devices** - User modifies device information
5. **Deleting devices** - User removes devices with confirmation

## Test Classes

### `TestDeviceE2EWorkflow`
Complete end-to-end workflow tests that simulate real user interactions:

- **test_complete_device_lifecycle** - Full CRUD workflow (Create → View → Edit → Delete)
- **test_add_device_and_see_in_list** - Add device and verify it appears
- **test_add_device_without_assignment** - Create unassigned device
- **test_delete_device_with_confirmation** - Delete with dialog confirmation
- **test_cancel_delete_operation** - Cancel deletion via dialog
- **test_edit_and_cancel** - Edit mode with cancellation
- **test_multiple_devices_management** - Manage multiple devices simultaneously
- **test_form_validation** - Input validation and required fields

### `TestDeviceUIInteractions`
UI state and interaction tests:

- **test_page_loads_correctly** - Verify all page elements load
- **test_responsive_ui_updates** - Real-time UI updates without refresh

## Prerequisites

### 1. Application Running
The tests assume the application is running locally:

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000 (with `STORAGE_MODE=memory`)

### 2. Python Environment
Install Python dependencies:

```bash
# Using pip
cd tests
pip install -r requirements.txt

# Or using uv (recommended)
cd tests
uv pip install -r requirements.txt
```

### 3. Playwright Browsers
Install Playwright browsers:

```bash
playwright install chromium
```

## Running Tests

### Run All E2E Tests
```bash
cd tests
pytest e2e/test_devices.py -v
```

### Run Specific Test Class
```bash
pytest e2e/test_devices.py::TestDeviceE2EWorkflow -v
```

### Run Specific Test
```bash
pytest e2e/test_devices.py::TestDeviceE2EWorkflow::test_complete_device_lifecycle -v
```

### Run with Detailed Output
```bash
pytest e2e/test_devices.py -v -s
```

### Run in Headed Mode (Show Browser)
```bash
pytest e2e/test_devices.py --headed
```

### Run with Specific Browser
```bash
# Firefox
pytest e2e/test_devices.py --browser firefox

# WebKit (Safari)
pytest e2e/test_devices.py --browser webkit
```

## Test Execution Workflow

### Complete Test Run
1. **Terminal 1** - Start backend:
   ```bash
   cd backend
   STORAGE_MODE=memory uv run uvicorn src.main:app --reload
   ```

2. **Terminal 2** - Start frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Terminal 3** - Run tests:
   ```bash
   cd tests
   pytest e2e/test_devices.py -v
   ```

## Test Features

### Clean State Management
Each test uses the `clean_state` fixture which:
- Clears all devices before the test starts
- Ensures isolated test execution
- Prevents test interference
- Optionally cleans up after tests

### Dialog Handling
Tests automatically handle browser confirmation dialogs:
```python
page.on("dialog", lambda dialog: dialog.accept())  # Confirm
page.on("dialog", lambda dialog: dialog.dismiss())  # Cancel
```

### Robust Locators
Tests use reliable locators based on:
- **IDs**: `input[id="name"]`, `input[id="assignedTo"]`
- **Classes**: `.device-item`, `.btn-edit`, `.btn-delete`
- **Text content**: `button:has-text("Add Device")`
- **Filters**: `.device-item.filter(has_text="Device Name")`

## Key Locators Reference

| Element | Locator | Description |
|---------|---------|-------------|
| Page Header | `h1` | "Device Management" |
| Form Header | `h2` | "Add New Device" / "Edit Device" |
| Device Name Input | `input[id="name"]` | Required field |
| Assigned To Input | `input[id="assignedTo"]` | Optional field |
| Add/Update Button | `button:has-text("Add Device")` | Submit button |
| Cancel Button | `button.btn-secondary` | Cancel edit |
| Device Card | `.device-item` | Individual device |
| Edit Button | `button.btn-edit` | Edit device |
| Delete Button | `button.btn-delete` | Delete device |
| Empty State | `.empty-state` | No devices message |

## Test Data

Tests use descriptive device names to make debugging easier:
- "MacBook Pro 16-inch"
- "iPhone 15 Pro"
- "Dell Monitor 27-inch"
- "Surface Pro 9"

## Debugging Tips

### View Browser Actions
Run in headed mode to see what the test is doing:
```bash
pytest e2e/test_devices.py --headed -s
```

### Slow Down Execution
Add slowmo to see actions more clearly:
```bash
pytest e2e/test_devices.py --headed --slowmo 1000
```

### Screenshot on Failure
Screenshots are automatically captured on test failure and saved to `test-results/`

### Verbose Output
Use `-v` for verbose test names and `-s` to see print statements:
```bash
pytest e2e/test_devices.py -v -s
```

### Single Test Debugging
Run just one test to isolate issues:
```bash
pytest e2e/test_devices.py::TestDeviceE2EWorkflow::test_add_device_and_see_in_list -v -s --headed
```

## Common Issues

### "Connection Refused" Error
- **Cause**: Frontend or backend not running
- **Solution**: Start both servers before running tests

### "Element Not Found" Error
- **Cause**: UI timing or locator mismatch
- **Solution**: Check locators match the actual UI, add explicit waits if needed

### "Browser Not Installed" Error
- **Cause**: Playwright browsers not installed
- **Solution**: Run `playwright install chromium`

### Tests Fail Randomly
- **Cause**: Race conditions or timing issues
- **Solution**: Use Playwright's built-in waiting (`expect()` auto-waits)

## Best Practices

1. **Use the `clean_state` fixture** - Ensures test isolation
2. **Use `expect()` assertions** - Built-in auto-waiting for elements
3. **Filter locators for specificity** - `.filter(has_text="Device Name")`
4. **Handle dialogs explicitly** - Set up handlers before triggering actions
5. **Use descriptive test names** - Makes failures easier to understand
6. **One workflow per test** - Keep tests focused and maintainable

## Continuous Integration

To run these tests in CI/CD:

```yaml
# Example GitHub Actions workflow
- name: Install dependencies
  run: |
    pip install -r tests/requirements.txt
    playwright install chromium

- name: Start backend
  run: |
    cd backend
    STORAGE_MODE=memory uvicorn src.main:app &

- name: Start frontend
  run: |
    cd frontend
    npm install
    npm run dev &

- name: Run E2E tests
  run: |
    cd tests
    pytest e2e/test_devices.py -v
```

## Contributing

When adding new E2E tests:
1. Follow the existing test structure
2. Use the `clean_state` fixture for isolation
3. Add descriptive docstrings
4. Test both success and error cases
5. Update this README with new test descriptions

## Support

For issues or questions:
- Check the main [tests/README.md](../README.md)
- Review Playwright documentation: https://playwright.dev/python/
- Review pytest documentation: https://docs.pytest.org/
