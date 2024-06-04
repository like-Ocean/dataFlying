from models import Flight
from peewee import ForeignKeyField, DateTimeField
from database import BaseModel


class Time(BaseModel):
    time = DateTimeField(primary_key=True, unique=True)
    flight = ForeignKeyField(Flight, backref='times', on_delete='CASCADE')

    def get_dto(self):
        return {
            'time': self.time,
            'flight': {
                'id': self.flight.id,
                'IMEI': self.flight.IMEI,
                'user_phone_number': self.flight.user_phone_number.phone_number
            }
        }

    class Meta:
        db_table = 'times'
