from models import Flight
from database import BaseModel
from peewee import AutoField, ForeignKeyField, FloatField


class Barometer(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    flight = ForeignKeyField(Flight, backref='barometers', on_delete='CASCADE')
    pressure = FloatField(null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'flight': {
                'id': self.flight.id,
            },
            'pressure': self.pressure
        }

    class Meta:
        db_table = 'barometers'
