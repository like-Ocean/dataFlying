from models import Flight
from database import BaseModel
from peewee import AutoField, ForeignKeyField, FloatField


class Gps(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    flight = ForeignKeyField(Flight, backref='gps', on_delete='CASCADE')
    latitude = FloatField(null=False)
    longitude = FloatField(null=False)
    altitude_gps = FloatField(null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'flight': {
                'id': self.flight.id,
            },
            'latitude': self.latitude,
            'longitude': self.longitude,
            'altitude_gps': self.altitude_gps
        }

    class Meta:
        db_table = 'gps'
