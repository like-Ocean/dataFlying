from pydantic import BaseModel, Field
from datetime import datetime


class DeviceModel(BaseModel):
    user_id: int = Field(...)
    imei: str = Field(...)


class RemoveDeviceModel(BaseModel):
    user_id: int = Field(...),
    device_id: int = Field(...)


class AccelerationModel(BaseModel):
    x: float = Field(...)
    y: float = Field(...)
    z: float = Field(...)


class GyroModel(BaseModel):
    x: float = Field(...)
    y: float = Field(...)
    z: float = Field(...)


class MagnetometerModel(BaseModel):
    x: float = Field(...)
    y: float = Field(...)
    z: float = Field(...)


class SensorDataModel(BaseModel):
    imei: str = Field(...)
    acceleration: AccelerationModel
    gyro: GyroModel
    magnetometer: MagnetometerModel
    temperature_mpu: float = Field(...)
    temperature_bmp: float = Field(...)
    pressure: float = Field(...)
    altitude: float = Field(...)
    latitude: float = Field(...)
    longitude: float = Field(...)
    altitude_gps: float = Field(...)
    time: datetime
