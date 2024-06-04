from models import Time
from database import BaseModel
from peewee import AutoField, ForeignKeyField, FloatField


class Temperature(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    time = ForeignKeyField(Time, backref='temperatures', on_delete='CASCADE')
    temperature_mpu = FloatField(null=False)
    temperature_bmp = FloatField(null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'time': {
                'time': self.time.time,
                'flight': self.time.flight.id,
            },
            'temperature_mpu': self.temperature_mpu,
            'temperature_bmp': self.temperature_bmp
        }

    class Meta:
        db_table = 'temperatures'
