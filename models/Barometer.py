from models import Time
from database import BaseModel
from peewee import AutoField, ForeignKeyField, FloatField


class Barometer(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    time = ForeignKeyField(Time, backref='barometers', on_delete='CASCADE')
    pressure = FloatField(null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'time': {
                'time': self.time.time,
                'flight': self.time.flight.id,
            },
            'pressure': self.pressure
        }

    class Meta:
        db_table = 'barometers'
