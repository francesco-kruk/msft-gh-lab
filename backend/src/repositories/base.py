"""
Repository interface for device storage.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from ..schemas import DeviceCreate, DeviceUpdate, DeviceResponse


class DeviceRepository(ABC):
    """Abstract repository interface for device CRUD."""

    @abstractmethod
    async def list_devices(self, skip: int = 0, limit: int = 100) -> List[DeviceResponse]:
        """List all devices with pagination."""

    @abstractmethod
    async def get_device(self, device_id: str) -> Optional[DeviceResponse]:
        """Get a device by ID."""

    @abstractmethod
    async def create_device(self, device: DeviceCreate) -> DeviceResponse:
        """Create a new device."""

    @abstractmethod
    async def update_device(self, device_id: str, device: DeviceUpdate) -> Optional[DeviceResponse]:
        """Update an existing device."""

    @abstractmethod
    async def delete_device(self, device_id: str) -> bool:
        """Delete a device by ID."""
