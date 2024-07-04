from fastapi import APIRouter, Response, Depends
from service import device_service
from models import User
from service.user_service import get_current_user
from .device_scheme import SensorDataModel, DeviceModel, RemoveDeviceModel


device_router = APIRouter(prefix="/devices", tags=["devices"])


@device_router.post("/add/device")
async def add_device(device_model: DeviceModel, current_user: User = Depends(get_current_user)):
    device_data = await device_service.add_device(device_model.user_id, device_model.imei)
    return device_data


@device_router.delete("/remove/device")
async def remove_device_route(device_model: RemoveDeviceModel, current_user: User = Depends(get_current_user)):
    await device_service.remove_device(device_model.user_id, device_model.device_id)
    return Response(status_code=204)


@device_router.get("/")
async def get_devices():
    devices = await device_service.get_devices()
    return devices


@device_router.get("/flights")
async def get_flights():
    flights = await device_service.get_flights()
    return flights


@device_router.post("/add/data")
async def add_data(data: SensorDataModel):
    result = await device_service.get_and_write_data(data)
    return result
