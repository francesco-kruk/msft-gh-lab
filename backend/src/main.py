"""
FastAPI backend for device inventory management.
Uses Cosmos DB with Azure managed identity for authentication.
"""
import logging
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .db.cosmos import close_cosmos_client, get_cosmos_client
from .schemas import DeviceCreate, DeviceUpdate, DeviceResponse
from . import repositories as device_repo
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown."""
    logger.info("Starting application...")
    
    storage_mode = device_repo.get_storage_mode()
    logger.info(f"Storage mode: {storage_mode}")

    if storage_mode == "cosmos":
        # Test Cosmos DB connection on startup (but don't block if it fails)
        try:
            await get_cosmos_client()
            logger.info("Cosmos DB connection established")
        except Exception as e:
            logger.warning(f"Could not connect to Cosmos DB at startup: {e}")
            # Don't fail startup - let individual requests handle the error
    
    yield
    
    # Cleanup on shutdown
    logger.info("Shutting down application...")
    if storage_mode == "cosmos":
        await close_cosmos_client()
    logger.info("Application shutdown complete")


app = FastAPI(
    title="Device Inventory API",
    description="API for managing device inventory",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware - configured from environment variable
# In production, set ALLOWED_ORIGINS to specific frontend domain(s)
allowed_origins_str = os.environ.get("ALLOWED_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS configured with allowed origins: {allowed_origins}")


@app.get("/health")
async def health_check():
    """Health check endpoint for container app probes."""
    return {"status": "healthy"}


@app.get("/devices", response_model=List[DeviceResponse])
async def list_devices(skip: int = 0, limit: int = 100):
    """List all devices with pagination."""
    try:
        return await device_repo.list_devices(skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Error listing devices: {e}")
        raise HTTPException(status_code=500, detail="Failed to list devices")


@app.get("/devices/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: str):
    """Get a device by ID."""
    try:
        device = await device_repo.get_device(device_id)
        if device is None:
            raise HTTPException(status_code=404, detail="Device not found")
        return device
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting device {device_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get device")


@app.post("/devices", response_model=DeviceResponse, status_code=201)
async def create_device(device: DeviceCreate):
    """Create a new device."""
    try:
        return await device_repo.create_device(device)
    except Exception as e:
        logger.error(f"Error creating device: {e}")
        raise HTTPException(status_code=500, detail="Failed to create device")


@app.put("/devices/{device_id}", response_model=DeviceResponse)
async def update_device(device_id: str, device: DeviceUpdate):
    """Update an existing device."""
    try:
        updated = await device_repo.update_device(device_id, device)
        if updated is None:
            raise HTTPException(status_code=404, detail="Device not found")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating device {device_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update device")


@app.delete("/devices/{device_id}", status_code=204)
async def delete_device(device_id: str):
    """Delete a device by ID."""
    try:
        deleted = await device_repo.delete_device(device_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Device not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting device {device_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete device")
