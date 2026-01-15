"""
Cosmos DB repository for device CRUD operations.
"""
import uuid
import logging
from datetime import datetime, timezone
from typing import List, Optional

from azure.cosmos.exceptions import CosmosResourceNotFoundError

from ..db.cosmos import get_devices_container
from ..schemas import DeviceCreate, DeviceUpdate, DeviceResponse
from .base import DeviceRepository

logger = logging.getLogger(__name__)


def _doc_to_device(doc: dict) -> DeviceResponse:
    """Convert a Cosmos DB document to a DeviceResponse."""
    return DeviceResponse(
        id=doc["id"],
        name=doc["name"],
        assigned_to=doc.get("assigned_to"),
        created_at=datetime.fromisoformat(doc["created_at"]),
        updated_at=datetime.fromisoformat(doc["updated_at"]),
    )


class CosmosDeviceRepository(DeviceRepository):
    """Cosmos DB-backed repository implementation."""

    async def list_devices(self, skip: int = 0, limit: int = 100) -> List[DeviceResponse]:
        """List all devices with pagination."""
        container = await get_devices_container()

        query = "SELECT * FROM c ORDER BY c.created_at DESC OFFSET @skip LIMIT @limit"
        parameters = [
            {"name": "@skip", "value": skip},
            {"name": "@limit", "value": limit},
        ]

        devices = []
        async for item in container.query_items(
            query=query,
            parameters=parameters,
        ):
            devices.append(_doc_to_device(item))

        return devices

    async def get_device(self, device_id: str) -> Optional[DeviceResponse]:
        """Get a device by ID."""
        container = await get_devices_container()

        try:
            doc = await container.read_item(item=device_id, partition_key=device_id)
            return _doc_to_device(doc)
        except CosmosResourceNotFoundError:
            return None

    async def create_device(self, device: DeviceCreate) -> DeviceResponse:
        """Create a new device."""
        container = await get_devices_container()

        now = datetime.now(timezone.utc).isoformat()
        device_id = str(uuid.uuid4())

        doc = {
            "id": device_id,
            "name": device.name,
            "assigned_to": device.assigned_to,
            "created_at": now,
            "updated_at": now,
        }

        result = await container.create_item(body=doc)
        logger.info(f"Created device: {device_id}")

        return _doc_to_device(result)

    async def update_device(self, device_id: str, device: DeviceUpdate) -> Optional[DeviceResponse]:
        """Update an existing device."""
        container = await get_devices_container()

        try:
            # Read the existing document
            existing = await container.read_item(item=device_id, partition_key=device_id)

            # Update only the fields that were provided
            if device.name is not None:
                existing["name"] = device.name
            if device.assigned_to is not None:
                existing["assigned_to"] = device.assigned_to

            existing["updated_at"] = datetime.now(timezone.utc).isoformat()

            # Replace the document
            result = await container.replace_item(item=device_id, body=existing)
            logger.info(f"Updated device: {device_id}")

            return _doc_to_device(result)
        except CosmosResourceNotFoundError:
            return None

    async def delete_device(self, device_id: str) -> bool:
        """Delete a device by ID."""
        container = await get_devices_container()

        try:
            await container.delete_item(item=device_id, partition_key=device_id)
            logger.info(f"Deleted device: {device_id}")
            return True
        except CosmosResourceNotFoundError:
            return False
