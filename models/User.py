from peewee import TextField, AutoField, IntegerField
from database import BaseModel


class User(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    login = TextField(null=False, unique=True)
    email = TextField(null=False)
    role = IntegerField(null=False)
    IMEI = TextField(null=False)
    phone_number = TextField(null=False)
    password = TextField(null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'login': self.login,
            'email': self.email,
            'role': self.role,
            'IMEI': self.IMEI,
            'phone_number': self.phone_number
        }

    class Meta:
        db_table = 'users'
