# Device Management Application - Test Plan

## Overview

This test plan covers comprehensive end-to-end testing of the Device Management application using Playwright with Python. The tests validate both UI functionality and API endpoints.

## Application Exploration Summary

### Core Features Identified

Based on exploration of the application (http://localhost:3000), the following key functionalities were identified:

#### 1. **Device Listing**
- **Location**: Main list section on the right side
- **UI Elements**: 
  - Device cards with name, assignment status, Edit and Delete buttons
  - Empty state message when no devices exist
- **Expected Behavior**: 
  - Displays all devices fetched from the API
  - Shows "No devices found. Add your first device!" when empty

#### 2. **Add Device**
- **Location**: Form section on the left side
- **UI Elements**:
  - "Device Name" input field (required)
  - "Assigned To" input field (optional)
  - "Add Device" submit button
- **Expected Behavior**:
  - Creates new device via POST /api/devices
  - Clears form after successful submission
  - Device appears in the list immediately

#### 3. **Edit Device**
- **Location**: Same form section, triggered by Edit button
- **UI Elements**:
  - Pre-filled form with existing device data
  - "Update Device" button instead of "Add Device"
  - "Cancel" button to exit edit mode
  - Form header changes to "Edit Device"
- **Expected Behavior**:
  - Populates form with device data when Edit is clicked
  - Updates device via PUT /api/devices/:id
  - Returns to add mode after successful update or cancel

#### 4. **Delete Device**
- **Location**: Delete button in each device card
- **UI Elements**: Delete button with confirmation dialog
- **Expected Behavior**:
  - Shows browser confirmation dialog
  - Deletes device via DELETE /api/devices/:id
  - Removes device from list immediately

#### 5. **Error Handling**
- **UI Elements**: Error state display (if applicable)
- **Expected Behavior**:
  - Gracefully handles API failures
  - Displays error messages to users

### API Endpoints

#### Health Check
- **Endpoint**: `GET /health`
- **Response**: `{"status": "healthy"}`
- **Purpose**: Container health probe

#### List Devices
- **Endpoint**: `GET /devices`
- **Query Params**: `skip` (default: 0), `limit` (default: 100)
- **Response**: Array of device objects

#### Get Device
- **Endpoint**: `GET /devices/:id`
- **Response**: Single device object or 404

#### Create Device
- **Endpoint**: `POST /devices`
- **Body**: `{"name": string, "assigned_to": string | null}`
- **Response**: Created device with id, timestamps

#### Update Device
- **Endpoint**: `PUT /devices/:id`
- **Body**: `{"name": string, "assigned_to": string | null}`
- **Response**: Updated device object

#### Delete Device
- **Endpoint**: `DELETE /devices/:id`
- **Response**: Success message or 404

### User Flows Tested

#### Flow 1: Create Device with Assignment
1. User opens application
2. Fills in device name: "MacBook Pro M3"
3. Fills in assigned to: "Alice Smith"
4. Clicks "Add Device"
5. Device appears in list with correct information
6. Form is cleared for next entry

#### Flow 2: Create Device without Assignment
1. User opens application
2. Fills in device name: "iPhone 15 Pro"
3. Leaves "Assigned To" empty
4. Clicks "Add Device"
5. Device appears with "Not assigned" status

#### Flow 3: Edit Existing Device
1. User clicks Edit on a device
2. Form switches to edit mode
3. Fields are pre-populated
4. User modifies name/assignment
5. Clicks "Update Device"
6. Changes are reflected in the list
7. Form returns to add mode

#### Flow 4: Cancel Edit Operation
1. User clicks Edit on a device
2. Form switches to edit mode
3. User clicks Cancel
4. Form returns to add mode without saving
5. Original device data remains unchanged

#### Flow 5: Delete Device
1. User clicks Delete on a device
2. Confirmation dialog appears
3. User confirms deletion
4. Device is removed from list
5. List updates (or shows empty state)

## Test Coverage

### UI Tests (14 tests)
- ✅ Page loads successfully
- ✅ Empty state display
- ✅ Add device with assignment
- ✅ Add device without assignment
- ✅ Edit device
- ✅ Cancel edit operation
- ✅ Delete device
- ✅ Form validation (empty name)
- ✅ Multiple devices display
- ✅ Loading state handling
- ✅ Error handling

### API Tests (6 tests)
- ✅ Health check endpoint
- ✅ List devices endpoint
- ✅ Create device endpoint
- ✅ Get device endpoint (via update test)
- ✅ Update device endpoint
- ✅ Delete device endpoint

## Test Environment

### Prerequisites
1. Frontend server running on http://localhost:3000
2. Backend server running on http://localhost:8000
3. Backend in `STORAGE_MODE=memory` for test isolation

### Installation

```bash
# Install Python dependencies
cd tests
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test class
pytest test_device_management.py::TestDeviceManagement

# Run specific test
pytest test_device_management.py::TestDeviceManagement::test_add_device_with_assignment

# Run with detailed output
pytest -v -s

# Run in headed mode (show browser)
pytest --headed

# Run with specific browser
pytest --browser firefox
```

### Starting Application for Testing

```bash
# Terminal 1 - Start backend
cd backend
STORAGE_MODE=memory uv run uvicorn src.main:app --reload

# Terminal 2 - Start frontend
cd frontend
npm run dev

# Terminal 3 - Run tests
cd tests
pytest
```

## Test Locators Reference

### Key UI Locators
- **Page Header**: `h1` with text "Device Management"
- **Form Header**: `h2` (changes between "Add New Device" / "Edit Device")
- **Device Name Input**: `input[id="name"]`
- **Assigned To Input**: `input[id="assignedTo"]`
- **Submit Button**: `button:has-text("Add Device")` or `button:has-text("Update Device")`
- **Cancel Button**: `button.btn-secondary` with text "Cancel"
- **Device Cards**: `.device-item`
- **Edit Button**: `button.btn-edit`
- **Delete Button**: `button.btn-delete`
- **Empty State**: `.empty-state`
- **Main Content**: `.app-main`

## Known Limitations

1. **Browser Confirmation Dialogs**: Tests handle JavaScript `confirm()` dialogs, but actual behavior may vary by browser
2. **State Isolation**: Tests share the in-memory database state when run sequentially - consider database reset between tests for true isolation
3. **Network Delays**: Tests assume local deployment with minimal latency
4. **Visual Regression**: No visual regression testing implemented yet

## Future Test Enhancements

1. **Performance Testing**: Measure load times, API response times
2. **Accessibility Testing**: WCAG compliance, keyboard navigation, screen reader support
3. **Mobile Testing**: Responsive design validation
4. **Cross-browser Testing**: Run on Chrome, Firefox, Safari, Edge
5. **Integration Testing**: Test with actual Cosmos DB backend
6. **Load Testing**: Stress test with many devices
7. **Security Testing**: XSS, CSRF, input validation
8. **CI/CD Integration**: Automated testing in GitHub Actions

## Test Maintenance

- Update locators if UI structure changes
- Add tests for new features
- Review and update API tests when endpoints change
- Keep Playwright and pytest versions updated
- Monitor test flakiness and add appropriate waits/retries

## Contact & Support

For questions about tests or to report issues:
- Review the test output for detailed error messages
- Check that both frontend and backend are running
- Verify Playwright browsers are installed
- Ensure pytest-playwright plugin is installed

