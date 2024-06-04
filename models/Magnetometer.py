from models import Time
from database import BaseModel
from peewee import AutoField, ForeignKeyField, FloatField


class Magnetometer(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    time = ForeignKeyField(Time, backref='magnetometers', on_delete='CASCADE')
    X = FloatField(null=False)
    Y = FloatField(null=False)
    Z = FloatField(null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'time': {
                'time': self.time.time,
                'flight': self.time.flight.id,
            },
            'X': self.X,
            'Y': self.Y,
            'Z': self.Z
        }

    class Meta:
        db_table = 'magnetometers'
