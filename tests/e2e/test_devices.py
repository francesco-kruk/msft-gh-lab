"""
End-to-End Test Suite for Device Management Application

This test suite verifies the complete user workflow:
1. Opening the application
2. Adding a new device
3. Viewing the device in the list
4. Editing the device
5. Deleting the device

Tests are written using Playwright with Python to simulate real user interactions.
"""
import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="function")
def app(page: Page):
    """Navigate to the application and ensure it's loaded."""
    page.goto("http://localhost:3000")
    expect(page).to_have_title("Inventory Management")
    expect(page.get_by_role("heading", level=1)).to_contain_text("Device Management")
    return page


@pytest.fixture(scope="function")
def clean_state(app: Page):
    """
    Ensure a clean state before each test by clearing all devices.
    This fixture navigates to the app and deletes all existing devices.
    """
    # Set up dialog handler to auto-accept confirmations
    app.on("dialog", lambda dialog: dialog.accept())
    
    # Delete all existing devices
    delete_buttons = app.get_by_role("button", name="Delete")
    while delete_buttons.count() > 0:
        delete_buttons.first.click()
        app.wait_for_timeout(100)
        delete_buttons = app.get_by_role("button", name="Delete")
    
    # Verify clean state - empty message should be visible
    expect(app.get_by_text("No devices found")).to_be_visible()
    
    yield app
    
    # Cleanup after test
    app.on("dialog", lambda dialog: dialog.accept())
    delete_buttons = app.get_by_role("button", name="Delete")
    while delete_buttons.count() > 0:
        delete_buttons.first.click()
        app.wait_for_timeout(100)
        delete_buttons = app.get_by_role("button", name="Delete")


def test_page_loads_correctly(app: Page):
    """
    Test that the application loads with all expected elements.
    
    Verifies:
    - Page title
    - Main heading
    - Form section with correct heading
    - Device list section with correct heading
    - Input fields are present
    - Add button is present
    """
    # Verify page title and main heading
    expect(app).to_have_title("Inventory Management")
    expect(app.get_by_role("heading", level=1)).to_contain_text("Device Management")
    
    # Verify form section
    expect(app.get_by_role("heading", level=2).first).to_have_text("Add New Device")
    
    # Verify form fields
    expect(app.get_by_role("textbox", name="Device Name *")).to_be_visible()
    expect(app.get_by_role("textbox", name="Assigned To")).to_be_visible()
    expect(app.get_by_role("button", name="Add Device")).to_be_visible()
    
    # Verify devices section
    expect(app.get_by_role("heading", name="Devices")).to_be_visible()


def test_add_device_and_see_in_list(clean_state: Page):
    """
    Test adding a new device and verifying it appears in the list.
    
    This test simulates a user:
    1. Filling in the device form
    2. Clicking the Add Device button
    3. Verifying the device appears in the list with correct information
    4. Verifying the form is cleared after submission
    """
    page = clean_state
    
    # Fill in device information
    device_name = "MacBook Pro 16-inch"
    assigned_to = "John Doe"
    
    page.get_by_role("textbox", name="Device Name *").fill(device_name)
    page.get_by_role("textbox", name="Assigned To").fill(assigned_to)
    page.get_by_role("button", name="Add Device").click()
    
    # Verify device appears in the list
    expect(page.get_by_role("heading", level=3, name=device_name)).to_be_visible()
    expect(page.get_by_text(f"Assigned to: {assigned_to}")).to_be_visible()
    
    # Verify form was cleared
    expect(page.get_by_role("textbox", name="Device Name *")).to_have_value("")
    expect(page.get_by_role("textbox", name="Assigned To")).to_have_value("")
    
    # Verify action buttons are present
    expect(page.get_by_role("button", name="Edit")).to_be_visible()
    expect(page.get_by_role("button", name="Delete")).to_be_visible()


def test_add_device_without_assignment(clean_state: Page):
    """
    Test adding a device without assigning it to anyone.
    
    Verifies that:
    - A device can be created with only a name
    - The device shows "Not assigned" in the list
    """
    page = clean_state
    
    device_name = "Dell Monitor"
    
    page.get_by_role("textbox", name="Device Name *").fill(device_name)
    page.get_by_role("button", name="Add Device").click()
    
    # Verify device appears in the list
    expect(page.get_by_role("heading", level=3, name=device_name)).to_be_visible()
    expect(page.get_by_text("Not assigned")).to_be_visible()


def test_form_validation_empty_name(clean_state: Page):
    """
    Test that the form validates required fields.
    
    Verifies that submitting without a device name is prevented by HTML5 validation.
    """
    page = clean_state
    
    # Try to submit without filling device name
    page.get_by_role("button", name="Add Device").click()
    
    # The device name field should be focused (HTML5 validation)
    expect(page.get_by_role("textbox", name="Device Name *")).to_be_focused()
    
    # Verify no device was added
    expect(page.get_by_text("No devices found")).to_be_visible()


def test_delete_device_with_confirmation(clean_state: Page):
    """
    Test deleting a device with confirmation dialog.
    
    Workflow:
    1. Add a device
    2. Click delete button
    3. Confirm deletion in dialog
    4. Verify device is removed
    """
    page = clean_state
    
    # Add a device to delete
    device_name = "Old Printer"
    page.get_by_role("textbox", name="Device Name *").fill(device_name)
    page.get_by_role("button", name="Add Device").click()
    
    # Verify device exists
    expect(page.get_by_role("heading", level=3, name=device_name)).to_be_visible()
    
    # Set up dialog handler to confirm deletion
    page.on("dialog", lambda dialog: dialog.accept())
    
    # Click delete button
    page.get_by_role("button", name="Delete").click()
    
    # Verify device is removed
    expect(page.get_by_role("heading", level=3, name=device_name)).not_to_be_visible()
    expect(page.get_by_text("No devices found")).to_be_visible()


def test_cancel_delete_operation(app: Page):
    """
    Test canceling a delete operation via the confirmation dialog.
    
    Verifies that:
    - Clicking cancel in the delete dialog keeps the device
    - Device remains visible in the list
    
    Note: This test uses app fixture instead of clean_state to avoid
    dialog handler conflicts.
    """
    page = app
    
    # Add a device
    device_name = "Important Laptop"
    page.get_by_role("textbox", name="Device Name *").fill(device_name)
    page.get_by_role("button", name="Add Device").click()
    
    # Verify device exists
    expect(page.get_by_role("heading", level=3, name=device_name)).to_be_visible()
    
    # Set up dialog handler to cancel deletion
    page.on("dialog", lambda dialog: dialog.dismiss())
    
    # Click delete button
    page.get_by_role("button", name="Delete").click()
    
    # Verify device still exists
    expect(page.get_by_role("heading", level=3, name=device_name)).to_be_visible()
    expect(page.get_by_text("No devices found")).not_to_be_visible()
    
    # Cleanup: Accept dialog this time to delete the device
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Delete").click()


def test_edit_device(clean_state: Page):
    """
    Test editing a device's information.
    
    Workflow:
    1. Add a device
    2. Click edit button
    3. Verify form is populated with device data
    4. Update the information
    5. Submit the update
    6. Verify changes are reflected in the list
    """
    page = clean_state
    
    # Add a device
    device_name = "iPhone 15 Pro"
    assigned_to = "Jane Smith"
    
    page.get_by_role("textbox", name="Device Name *").fill(device_name)
    page.get_by_role("textbox", name="Assigned To").fill(assigned_to)
    page.get_by_role("button", name="Add Device").click()
    
    # Click edit button
    page.get_by_role("button", name="Edit").click()
    
    # Verify we're in edit mode
    expect(page.get_by_role("heading", level=2).first).to_have_text("Edit Device")
    
    # Verify form is populated
    expect(page.get_by_role("textbox", name="Device Name *")).to_have_value(device_name)
    expect(page.get_by_role("textbox", name="Assigned To")).to_have_value(assigned_to)
    
    # Update the device information
    updated_name = "iPhone 15 Pro Max"
    updated_assigned_to = "Jane Doe"
    
    page.get_by_role("textbox", name="Device Name *").fill(updated_name)
    page.get_by_role("textbox", name="Assigned To").fill(updated_assigned_to)
    page.get_by_role("button", name="Update Device").click()
    
    # Verify we're back in add mode
    expect(page.get_by_role("heading", level=2).first).to_have_text("Add New Device")
    
    # Verify the updates
    expect(page.get_by_role("heading", level=3, name=updated_name)).to_be_visible()
    expect(page.get_by_text(f"Assigned to: {updated_assigned_to}")).to_be_visible()
    
    # Verify only the updated device is present (old name fully replaced)
    expect(page.get_by_role("heading", level=3)).to_have_count(1)
    expect(page.get_by_role("heading", level=3)).to_have_text(updated_name)


def test_edit_and_cancel(clean_state: Page):
    """
    Test canceling an edit operation.
    
    Verifies that:
    - Clicking cancel returns to add mode
    - Original device data is unchanged
    - Form is cleared
    """
    page = clean_state
    
    # Add a device
    device_name = "Dell XPS 15"
    assigned_to = "Bob Wilson"
    
    page.get_by_role("textbox", name="Device Name *").fill(device_name)
    page.get_by_role("textbox", name="Assigned To").fill(assigned_to)
    page.get_by_role("button", name="Add Device").click()
    
    # Click edit button
    page.get_by_role("button", name="Edit").click()
    
    # Verify we're in edit mode
    expect(page.get_by_role("heading", level=2).first).to_have_text("Edit Device")
    
    # Make some changes but don't submit
    page.get_by_role("textbox", name="Device Name *").fill("Changed Name")
    page.get_by_role("textbox", name="Assigned To").fill("Changed Person")
    
    # Click cancel
    page.get_by_role("button", name="Cancel").click()
    
    # Verify we're back in add mode
    expect(page.get_by_role("heading", level=2).first).to_have_text("Add New Device")
    
    # Verify form is cleared
    expect(page.get_by_role("textbox", name="Device Name *")).to_have_value("")
    expect(page.get_by_role("textbox", name="Assigned To")).to_have_value("")
    
    # Verify original device data is unchanged
    expect(page.get_by_role("heading", level=3, name=device_name)).to_be_visible()
    expect(page.get_by_text(f"Assigned to: {assigned_to}")).to_be_visible()


def test_multiple_devices_management(clean_state: Page):
    """
    Test managing multiple devices simultaneously.
    
    Verifies that:
    - Multiple devices can be added
    - All devices are displayed in the list
    - Each device can be edited or deleted independently
    """
    page = clean_state
    
    # Add multiple devices
    devices = [
        ("MacBook Pro", "Alice"),
        ("iPhone 15", "Bob"),
        ("iPad Air", "Charlie"),
    ]
    
    for device_name, assigned_to in devices:
        page.get_by_role("textbox", name="Device Name *").fill(device_name)
        page.get_by_role("textbox", name="Assigned To").fill(assigned_to)
        page.get_by_role("button", name="Add Device").click()
    
    # Verify all devices are present
    expect(page.get_by_role("button", name="Edit")).to_have_count(3)
    expect(page.get_by_role("button", name="Delete")).to_have_count(3)
    
    for device_name, assigned_to in devices:
        expect(page.get_by_role("heading", level=3, name=device_name)).to_be_visible()
        expect(page.get_by_text(f"Assigned to: {assigned_to}")).to_be_visible()
    
    # Delete the middle device
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Delete").nth(1).click()
    
    # Verify count decreased
    expect(page.get_by_role("button", name="Edit")).to_have_count(2)
    expect(page.get_by_role("button", name="Delete")).to_have_count(2)
    
    # Verify the correct device was deleted
    expect(page.get_by_role("heading", level=3, name="iPhone 15")).not_to_be_visible()
    expect(page.get_by_role("heading", level=3, name="MacBook Pro")).to_be_visible()
    expect(page.get_by_role("heading", level=3, name="iPad Air")).to_be_visible()


def test_complete_device_lifecycle(clean_state: Page):
    """
    Test the complete device lifecycle: Create → View → Edit → Delete
    
    This comprehensive test simulates a user:
    1. Opening the application
    2. Adding a new device with assignment
    3. Verifying it appears in the list
    4. Editing the device information
    5. Deleting the device
    6. Verifying the device is removed
    """
    page = clean_state
    
    # Step 1: Verify application is ready
    expect(page.get_by_role("heading", level=1)).to_contain_text("Device Management")
    expect(page.get_by_text("No devices found")).to_be_visible()
    
    # Step 2: Add a new device
    device_name = "ThinkPad X1 Carbon"
    assigned_to = "Sarah Connor"
    
    page.get_by_role("textbox", name="Device Name *").fill(device_name)
    page.get_by_role("textbox", name="Assigned To").fill(assigned_to)
    page.get_by_role("button", name="Add Device").click()
    
    # Step 3: Verify the device appears in the list
    expect(page.get_by_role("heading", level=3, name=device_name)).to_be_visible()
    expect(page.get_by_text(f"Assigned to: {assigned_to}")).to_be_visible()
    expect(page.get_by_role("button", name="Edit")).to_be_visible()
    expect(page.get_by_role("button", name="Delete")).to_be_visible()
    
    # Verify form was cleared
    expect(page.get_by_role("textbox", name="Device Name *")).to_have_value("")
    expect(page.get_by_role("textbox", name="Assigned To")).to_have_value("")
    
    # Step 4: Edit the device
    page.get_by_role("button", name="Edit").click()
    
    # Verify edit mode
    expect(page.get_by_role("heading", level=2).first).to_have_text("Edit Device")
    expect(page.get_by_role("textbox", name="Device Name *")).to_have_value(device_name)
    expect(page.get_by_role("textbox", name="Assigned To")).to_have_value(assigned_to)
    
    # Update the device
    updated_name = "ThinkPad X1 Carbon Gen 11"
    updated_assigned_to = "John Connor"
    
    page.get_by_role("textbox", name="Device Name *").fill(updated_name)
    page.get_by_role("textbox", name="Assigned To").fill(updated_assigned_to)
    page.get_by_role("button", name="Update Device").click()
    
    # Verify we're back in add mode and changes are reflected
    expect(page.get_by_role("heading", level=2).first).to_have_text("Add New Device")
    expect(page.get_by_role("heading", level=3, name=updated_name)).to_be_visible()
    expect(page.get_by_text(f"Assigned to: {updated_assigned_to}")).to_be_visible()
    
    # Step 5: Delete the device
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Delete").click()
    
    # Step 6: Verify the device is removed
    expect(page.get_by_role("heading", level=3, name=updated_name)).not_to_be_visible()
    expect(page.get_by_text("No devices found")).to_be_visible()
    expect(page.get_by_role("button", name="Edit")).not_to_be_visible()
    expect(page.get_by_role("button", name="Delete")).not_to_be_visible()


def test_responsive_ui_updates(clean_state: Page):
    """
    Test that UI updates in real-time without requiring page refresh.
    
    Verifies:
    - Adding a device immediately shows it in the list
    - Editing a device immediately updates the displayed information
    - Deleting a device immediately removes it from the view
    """
    page = clean_state
    
    # Add a device and verify immediate update
    page.get_by_role("textbox", name="Device Name *").fill("Surface Laptop")
    page.get_by_role("button", name="Add Device").click()
    
    # Should see device immediately without refresh
    expect(page.get_by_role("heading", level=3, name="Surface Laptop")).to_be_visible()
    
    # Edit and verify immediate update
    page.get_by_role("button", name="Edit").click()
    page.get_by_role("textbox", name="Device Name *").fill("Surface Laptop 5")
    page.get_by_role("button", name="Update Device").click()
    
    # Should see updated name immediately (only one device should be present)
    expect(page.get_by_role("heading", level=3)).to_have_count(1)
    expect(page.get_by_role("heading", level=3)).to_have_text("Surface Laptop 5")
    
    # Delete and verify immediate update
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Delete").click()
    
    # Should see empty state immediately
    expect(page.get_by_text("No devices found")).to_be_visible()

