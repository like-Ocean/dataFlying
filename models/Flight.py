from models import Device
from peewee import DateTimeField, AutoField, ForeignKeyField, IntegerField
from database import BaseModel


class Flight(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    flight_number = IntegerField(null=False, unique=False)
    IMEI = ForeignKeyField(Device, backref='flight', on_delete='CASCADE', null=False)
    time = DateTimeField(null=False, unique=False)

    def get_dto(self):
        return {
            'id': self.id,
            'flight_number': self.flight_number,
            'device': {
                'id': self.IMEI.id,
                'user': {
                    'id': self.IMEI.user.id,
                    'login': self.IMEI.user.login,
                    'email': self.IMEI.user.email,
                    'role': self.IMEI.user.role
                },
                'IMEI': self.IMEI.IMEI,
            },
            'time': self.time
        }

    class Meta:
        db_table = 'flights'
