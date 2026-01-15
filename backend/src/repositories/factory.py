"""
Repository factory and storage mode selection.
"""
import os
from typing import Optional

from .base import DeviceRepository
from .cosmos_repository import CosmosDeviceRepository
from .memory_repository import InMemoryDeviceRepository

_repo: Optional[DeviceRepository] = None


def get_storage_mode() -> str:
    """Get the current storage mode from environment variables."""
    mode = os.environ.get("STORAGE_MODE", "cosmos").strip().lower()
    return mode or "cosmos"


def get_repository() -> DeviceRepository:
    """Get the configured repository implementation."""
    global _repo

    if _repo is None:
        mode = get_storage_mode()
        if mode == "memory":
            _repo = InMemoryDeviceRepository()
        elif mode == "cosmos":
            _repo = CosmosDeviceRepository()
        else:
            raise ValueError(f"Unsupported STORAGE_MODE: {mode}")

    return _repo
