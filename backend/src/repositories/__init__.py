"""Repository exports with runtime selection."""
from typing import List, Optional

from ..schemas import DeviceCreate, DeviceUpdate, DeviceResponse
from .factory import get_repository, get_storage_mode


async def list_devices(skip: int = 0, limit: int = 100) -> List[DeviceResponse]:
    """List all devices with pagination."""
    repository = get_repository()
    return await repository.list_devices(skip=skip, limit=limit)


async def get_device(device_id: str) -> Optional[DeviceResponse]:
    """Get a device by ID."""
    repository = get_repository()
    return await repository.get_device(device_id)


async def create_device(device: DeviceCreate) -> DeviceResponse:
    """Create a new device."""
    repository = get_repository()
    return await repository.create_device(device)


async def update_device(device_id: str, device: DeviceUpdate) -> Optional[DeviceResponse]:
    """Update an existing device."""
    repository = get_repository()
    return await repository.update_device(device_id, device)


async def delete_device(device_id: str) -> bool:
    """Delete a device by ID."""
    repository = get_repository()
    return await repository.delete_device(device_id)


__all__ = [
    "get_storage_mode",
    "list_devices",
    "get_device",
    "create_device",
    "update_device",
    "delete_device",
]
