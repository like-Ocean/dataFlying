from models import User
from peewee import ForeignKeyField, TextField, AutoField
from database import BaseModel


class Device(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    user = ForeignKeyField(User, backref='device', on_delete='CASCADE', null=False)
    IMEI = TextField(null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'user': {
                'id': self.user.id,
                'login': self.user.login,
                'email': self.user.email,
                'role': self.user.role
            },
            'IMEI': self.IMEI
        }

    class Meta:
        db_table = 'devices'
