from models import Flight
from database import BaseModel
from peewee import AutoField, ForeignKeyField, FloatField


class Gyroscope(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    flight = ForeignKeyField(Flight, backref='gyroscopes', on_delete='CASCADE')
    X = FloatField(null=False)
    Y = FloatField(null=False)
    Z = FloatField(null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'flight': {
                'id': self.flight.id,
            },
            'X': self.X,
            'Y': self.Y,
            'Z': self.Z
        }

    class Meta:
        db_table = 'gyroscopes'
