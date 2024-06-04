from models import User
from peewee import TextField, AutoField, ForeignKeyField
from database import BaseModel


# IMEI то же вторичный ключ ?
class Flight(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    IMEI = TextField(null=False)
    user_phone_number = ForeignKeyField(User, backref='flights', on_delete='CASCADE')

    def get_dto(self):
        return {
            'id': self.id,
            'IMEI': self.IMEI,
            'user_phone_number': self.user_phone_number.phone_number
        }

    class Meta:
        db_table = 'flights'
