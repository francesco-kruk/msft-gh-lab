"""
In-memory repository for device CRUD operations.
"""
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional

from ..schemas import DeviceCreate, DeviceUpdate, DeviceResponse
from .base import DeviceRepository


class InMemoryDeviceRepository(DeviceRepository):
    """In-memory repository implementation."""

    def __init__(self) -> None:
        self._devices: Dict[str, DeviceResponse] = {}

    async def list_devices(self, skip: int = 0, limit: int = 100) -> List[DeviceResponse]:
        """List all devices with pagination."""
        devices = sorted(
            self._devices.values(),
            key=lambda device: device.created_at,
            reverse=True,
        )
        return devices[skip: skip + limit]

    async def get_device(self, device_id: str) -> Optional[DeviceResponse]:
        """Get a device by ID."""
        return self._devices.get(device_id)

    async def create_device(self, device: DeviceCreate) -> DeviceResponse:
        """Create a new device."""
        now = datetime.now(timezone.utc)
        device_id = str(uuid.uuid4())

        created = DeviceResponse(
            id=device_id,
            name=device.name,
            assigned_to=device.assigned_to,
            created_at=now,
            updated_at=now,
        )

        self._devices[device_id] = created
        return created

    async def update_device(self, device_id: str, device: DeviceUpdate) -> Optional[DeviceResponse]:
        """Update an existing device."""
        existing = self._devices.get(device_id)
        if existing is None:
            return None

        updated = DeviceResponse(
            id=existing.id,
            name=device.name if device.name is not None else existing.name,
            assigned_to=device.assigned_to if device.assigned_to is not None else existing.assigned_to,
            created_at=existing.created_at,
            updated_at=datetime.now(timezone.utc),
        )

        self._devices[device_id] = updated
        return updated

    async def delete_device(self, device_id: str) -> bool:
        """Delete a device by ID."""
        if device_id not in self._devices:
            return False
        del self._devices[device_id]
        return True
