from fastapi import HTTPException
from peewee import DoesNotExist
from models import User, Device, Flight, Accelerometer, Barometer, Gps, Gyroscope, Magnetometer, Temperature

from database import objects


async def add_device(user_id: id, imei: str):
    user = await objects.get_or_none(User.select().where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    dev = await objects.create(
        Device,
        user=user,
        IMEI=imei
    )
    return dev.get_dto()


async def remove_device(user_id: int, device_id: int):
    user = await objects.get_or_none(User.select().where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    device = await objects.get_or_none(Device.select().where(Device.id == device_id, Device.user == user))
    if not device:
        raise HTTPException(status_code=400, detail="Device not found or does not belong to this user")

    await objects.delete(device)


async def get_and_write_data(data):
    try:
        device = await objects.get(Device, Device.IMEI == data.imei)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Device not found")

    flights = await objects.execute(Flight.select().where(Flight.IMEI == device).order_by(Flight.flight_number.desc()))
    last_flight = flights[0] if flights else None
    flight_number = (last_flight.flight_number + 1) if last_flight else 1

    flight = await objects.create(Flight, flight_number=flight_number, IMEI=device, time=data.time)

    await objects.create(
        Accelerometer,
        flight=flight,
        X=data.acceleration.x,
        Y=data.acceleration.y,
        Z=data.acceleration.z
    )

    await objects.create(Barometer, flight=flight, pressure=data.pressure)

    await objects.create(
        Gps,
        flight=flight,
        latitude=data.latitude,
        longitude=data.longitude,
        altitude_gps=data.altitude_gps
    )

    await objects.create(Gyroscope, flight=flight, X=data.gyro.x, Y=data.gyro.y, Z=data.gyro.z)

    await objects.create(
        Magnetometer,
        flight=flight,
        X=data.magnetometer.x,
        Y=data.magnetometer.y,
        Z=data.magnetometer.z
    )

    await objects.create(
        Temperature,
        flight=flight,
        temperature_mpu=data.temperature_mpu,
        temperature_bmp=data.temperature_bmp
    )

    return flight.get_dto()


async def get_devices():
    devices = await objects.execute(Device.select())
    return [device.get_dto() for device in devices]