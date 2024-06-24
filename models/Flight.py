from models import User
from peewee import TextField, AutoField, ForeignKeyField
from database import BaseModel


class Flight(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    user_IMEI = ForeignKeyField(User, backref='flights_IMEI', on_delete='CASCADE')
    user_phone_number = ForeignKeyField(User, backref='flights', on_delete='CASCADE')

    def get_dto(self):
        return {
            'id': self.id,
            'user_IMEI': self.user_IMEI.IMEI,
            'user_phone_number': self.user_phone_number.phone_number
        }

    class Meta:
        db_table = 'flights'
