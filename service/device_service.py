from typing import Optional
from datetime import datetime
from fastapi import HTTPException
from peewee import DoesNotExist, fn
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

    # flight_number теперь с устройства приходит
    flight = await objects.create(Flight, flight_number=data.flight_number, IMEI=device, time=data.time)

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


async def get_user_devices(user_id: int):
    user = await objects.get_or_none(User.select().where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    devices = await objects.execute(Device.select().where(Device.user == user))

    return [device.get_dto() for device in devices]


async def get_user_device(user_id: int, device_id: int):
    user = await objects.get_or_none(User.select().where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    device = await objects.get_or_none(Device.select().where(Device.user == user, Device.id == device_id))
    if not device:
        raise HTTPException(status_code=400, detail="Device not found")

    return device.get_dto()


async def get_user_flights(user_id: int, imei: Optional[str] = None,
                           start_date: Optional[datetime] = None, page: int = 1, page_size: int = 20):
    user = await objects.get_or_none(User.select().where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    query = Flight.select(
        Flight.flight_number,
        Flight.IMEI,
        fn.MIN(Flight.time).alias('time')
    ).join(Device).join(User).where(User.id == user_id).group_by(Flight.flight_number, Flight.IMEI).order_by(Flight.flight_number)
    if imei:
        query = query.where(Device.IMEI == imei)
    if start_date:
        query = query.where(Flight.time >= start_date)

    total_flights = await objects.count(query)
    flights = await objects.execute(query.paginate(page, page_size))

    return {
        'total': total_flights,
        'page': page,
        'page_size': page_size,
        'flights': [flight.get_dto() for flight in flights]
    }


async def get_user_flight(user_id: int, flight_id: int):
    user = await objects.get_or_none(User.select().where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    flight = await objects.get_or_none(Flight.select().join(Device).where(Device.user == user, Flight.id == flight_id))
    if not flight:
        raise HTTPException(status_code=400, detail="Flight not found")

    accelerometers = await objects.execute(Accelerometer.select().where(Accelerometer.flight == flight))
    barometers = await objects.execute(Barometer.select().where(Barometer.flight == flight))
    gps_data = await objects.execute(Gps.select().where(Gps.flight == flight))
    gyroscopes = await objects.execute(Gyroscope.select().where(Gyroscope.flight == flight))
    magnetometers = await objects.execute(Magnetometer.select().where(Magnetometer.flight == flight))
    temperatures = await objects.execute(Temperature.select().where(Temperature.flight == flight))

    flight_data = flight.get_dto()
    flight_data['sensors'] = {
        'accelerometers': [sensor.get_dto() for sensor in accelerometers],
        'barometers': [sensor.get_dto() for sensor in barometers],
        'gps_data': [sensor.get_dto() for sensor in gps_data],
        'gyroscopes': [sensor.get_dto() for sensor in gyroscopes],
        'magnetometers': [sensor.get_dto() for sensor in magnetometers],
        'temperatures': [sensor.get_dto() for sensor in temperatures],
    }

    return flight_data


async def get_flight_by_flight_number(user_id: int, flight_number: int, IMEI: str):
    users = await objects.execute(User.select().where(User.id == user_id))
    if not users:
        raise HTTPException(status_code=400, detail="User not found")
    for user in users:
        flights = await objects.execute(
            Flight.select()
            .join(Device)
            .where((Flight.flight_number == flight_number) & (Device.user == user) & (Device.IMEI == IMEI))
        )
        if not flights:
            raise HTTPException(status_code=400, detail="Flight not found")

        for flight in flights:
            accelerometers = await objects.execute(
                Accelerometer.select().join(Flight, on=(Flight.id == Accelerometer.flight)).where(Flight.flight_number == flight_number)
            )
            barometers = await objects.execute(
                Barometer.select().join(Flight).where(Flight.flight_number == flight_number)
            )
            gps_data = await objects.execute(
                Gps.select().join(Flight).where(Flight.flight_number == flight_number)
            )
            gyroscopes = await objects.execute(
                Gyroscope.select().join(Flight).where(Flight.flight_number == flight_number)
            )
            magnetometers = await objects.execute(
                Magnetometer.select().join(Flight).where(Flight.flight_number == flight_number)
            )
            temperatures = await objects.execute(
                Temperature.select().join(Flight).where(Flight.flight_number == flight_number)
            )

            flight_data = flight.get_dto()

            flight_data['sensors'] = {
                'all_times': [
                    {'time': flight.time, 'flight': {'id': flight.id}} for flight in flights
                ],
                'accelerometers': [sensor.get_dto() for sensor in accelerometers],
                'barometers': [sensor.get_dto() for sensor in barometers],
                'gps_data': [sensor.get_dto() for sensor in gps_data],
                'gyroscopes': [sensor.get_dto() for sensor in gyroscopes],
                'magnetometers': [sensor.get_dto() for sensor in magnetometers],
                'temperatures': [sensor.get_dto() for sensor in temperatures],
            }

            return flight_data
