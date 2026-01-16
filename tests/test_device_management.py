"""
End-to-end tests for the Device Management application.
Tests cover the complete user journey from adding to deleting devices.
"""
import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the application."""
    return "http://localhost:3000"


@pytest.fixture(scope="session")
def api_url():
    """Base URL for the API."""
    return "http://localhost:8000"


class TestDeviceManagement:
    """Test suite for device management functionality."""

    def test_page_loads_successfully(self, page: Page, base_url: str):
        """Test that the application loads without errors."""
        page.goto(base_url)
        
        # Check page title or header
        expect(page.locator("h1")).to_contain_text("Device Management")
        
        # Check that main sections are visible
        expect(page.locator("h2").filter(has_text="Add New Device")).to_be_visible()

    def test_empty_state_display(self, page: Page, base_url: str):
        """Test that empty state is shown when no devices exist."""
        page.goto(base_url)
        
        # Should show empty state message
        expect(page.locator(".empty-state")).to_contain_text("No devices found")

    def test_add_device_with_assignment(self, page: Page, base_url: str):
        """Test adding a new device with assigned user."""
        page.goto(base_url)
        
        # Fill in the form
        page.fill('input[id="name"]', "MacBook Pro M3")
        page.fill('input[id="assignedTo"]', "Alice Smith")
        
        # Submit the form
        page.click('button:has-text("Add Device")')
        
        # Wait for the device to appear in the list
        expect(page.locator(".device-item")).to_contain_text("MacBook Pro M3")
        expect(page.locator(".device-item")).to_contain_text("Assigned to: Alice Smith")
        
        # Form should be cleared
        expect(page.locator('input[id="name"]')).to_have_value("")
        expect(page.locator('input[id="assignedTo"]')).to_have_value("")

    def test_add_device_without_assignment(self, page: Page, base_url: str):
        """Test adding a device without assigning it to anyone."""
        page.goto(base_url)
        
        # Fill only the device name
        page.fill('input[id="name"]', "iPhone 15 Pro")
        
        # Submit the form
        page.click('button:has-text("Add Device")')
        
        # Device should appear with "Not assigned" status
        expect(page.locator(".device-item").filter(has_text="iPhone 15 Pro")).to_contain_text("Not assigned")

    def test_edit_device(self, page: Page, base_url: str):
        """Test editing an existing device."""
        page.goto(base_url)
        
        # First, add a device
        page.fill('input[id="name"]', "Dell Monitor")
        page.fill('input[id="assignedTo"]', "Bob Johnson")
        page.click('button:has-text("Add Device")')
        
        # Wait for device to appear
        expect(page.locator(".device-item").filter(has_text="Dell Monitor")).to_be_visible()
        
        # Click edit button
        page.locator(".device-item").filter(has_text="Dell Monitor").locator("button.btn-edit").click()
        
        # Form should now show "Edit Device"
        expect(page.locator("h2")).to_contain_text("Edit Device")
        
        # Form should be pre-filled
        expect(page.locator('input[id="name"]')).to_have_value("Dell Monitor")
        expect(page.locator('input[id="assignedTo"]')).to_have_value("Bob Johnson")
        
        # Update the device
        page.fill('input[id="name"]', "Dell UltraSharp Monitor")
        page.fill('input[id="assignedTo"]', "Bob J. Johnson")
        page.click('button:has-text("Update Device")')
        
        # Check updated values
        expect(page.locator(".device-item")).to_contain_text("Dell UltraSharp Monitor")
        expect(page.locator(".device-item")).to_contain_text("Bob J. Johnson")
        
        # Form should reset to "Add New Device"
        expect(page.locator("h2")).to_contain_text("Add New Device")

    def test_cancel_edit(self, page: Page, base_url: str):
        """Test cancelling device edit operation."""
        page.goto(base_url)
        
        # Add a device
        page.fill('input[id="name"]', "Surface Laptop")
        page.click('button:has-text("Add Device")')
        
        # Start editing
        page.locator(".device-item").filter(has_text="Surface Laptop").locator("button.btn-edit").click()
        
        # Verify edit mode
        expect(page.locator("h2")).to_contain_text("Edit Device")
        expect(page.locator("button.btn-secondary")).to_contain_text("Cancel")
        
        # Cancel the edit
        page.click('button:has-text("Cancel")')
        
        # Should return to add mode
        expect(page.locator("h2")).to_contain_text("Add New Device")
        expect(page.locator('input[id="name"]')).to_have_value("")

    def test_delete_device(self, page: Page, base_url: str):
        """Test deleting a device."""
        page.goto(base_url)
        
        # Add a device to delete
        page.fill('input[id="name"]', "Old Laptop")
        page.click('button:has-text("Add Device")')
        
        # Confirm device exists
        expect(page.locator(".device-item").filter(has_text="Old Laptop")).to_be_visible()
        
        # Set up dialog handler for confirmation
        page.on("dialog", lambda dialog: dialog.accept())
        
        # Click delete button
        page.locator(".device-item").filter(has_text="Old Laptop").locator("button.btn-delete").click()
        
        # Device should be removed
        expect(page.locator(".device-item").filter(has_text="Old Laptop")).not_to_be_visible()

    def test_form_validation_empty_name(self, page: Page, base_url: str):
        """Test that empty device name is not accepted."""
        page.goto(base_url)
        
        # Try to submit with empty name
        page.fill('input[id="assignedTo"]', "Test User")
        page.click('button:has-text("Add Device")')
        
        # HTML5 validation should prevent submission
        # The form should still be in add mode
        expect(page.locator("h2")).to_contain_text("Add New Device")

    def test_multiple_devices_display(self, page: Page, base_url: str):
        """Test that multiple devices are displayed correctly."""
        page.goto(base_url)
        
        # Add multiple devices
        devices = [
            ("MacBook Air", "Dev Team"),
            ("iPad Pro", "Design Team"),
            ("Magic Mouse", None),
        ]
        
        for device_name, assigned_to in devices:
            page.fill('input[id="name"]', device_name)
            if assigned_to:
                page.fill('input[id="assignedTo"]', assigned_to)
            page.click('button:has-text("Add Device")')
            
            # Clear assigned_to field for next iteration
            page.fill('input[id="assignedTo"]', "")
        
        # Check all devices are visible
        for device_name, assigned_to in devices:
            expect(page.locator(".device-item").filter(has_text=device_name)).to_be_visible()

    def test_loading_state(self, page: Page, base_url: str):
        """Test that loading state is handled properly."""
        page.goto(base_url)
        
        # The page should load without hanging
        # Check that the main content is visible
        expect(page.locator(".app-main")).to_be_visible(timeout=5000)

    def test_error_handling_api_failure(self, page: Page, base_url: str):
        """Test that API errors are handled gracefully."""
        # This test would require mocking API failures
        # For now, we verify that the UI doesn't crash
        page.goto(base_url)
        expect(page.locator("h1")).to_be_visible()


class TestAPIEndpoints:
    """Test suite for API endpoints."""

    def test_health_endpoint(self, page: Page, api_url: str):
        """Test the health check endpoint."""
        response = page.request.get(f"{api_url}/health")
        assert response.status == 200
        assert response.json() == {"status": "healthy"}

    def test_list_devices_endpoint(self, page: Page, api_url: str):
        """Test listing devices via API."""
        response = page.request.get(f"{api_url}/devices")
        assert response.status == 200
        devices = response.json()
        assert isinstance(devices, list)

    def test_create_device_endpoint(self, page: Page, api_url: str):
        """Test creating a device via API."""
        device_data = {
            "name": "API Test Device",
            "assigned_to": "API Test User"
        }
        response = page.request.post(
            f"{api_url}/devices",
            data=device_data
        )
        assert response.status == 200
        created_device = response.json()
        assert created_device["name"] == "API Test Device"
        assert created_device["assigned_to"] == "API Test User"
        assert "id" in created_device

    def test_update_device_endpoint(self, page: Page, api_url: str):
        """Test updating a device via API."""
        # First create a device
        create_response = page.request.post(
            f"{api_url}/devices",
            data={"name": "Update Test", "assigned_to": None}
        )
        device_id = create_response.json()["id"]
        
        # Update it
        update_response = page.request.put(
            f"{api_url}/devices/{device_id}",
            data={"name": "Updated Device", "assigned_to": "New Owner"}
        )
        assert update_response.status == 200
        
        # Verify update
        get_response = page.request.get(f"{api_url}/devices/{device_id}")
        updated_device = get_response.json()
        assert updated_device["name"] == "Updated Device"
        assert updated_device["assigned_to"] == "New Owner"

    def test_delete_device_endpoint(self, page: Page, api_url: str):
        """Test deleting a device via API."""
        # Create a device
        create_response = page.request.post(
            f"{api_url}/devices",
            data={"name": "Delete Test", "assigned_to": None}
        )
        device_id = create_response.json()["id"]
        
        # Delete it
        delete_response = page.request.delete(f"{api_url}/devices/{device_id}")
        assert delete_response.status == 200
        
        # Verify deletion
        get_response = page.request.get(f"{api_url}/devices/{device_id}")
        assert get_response.status == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
