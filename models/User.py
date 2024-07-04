from peewee import TextField, AutoField, IntegerField
from database import BaseModel


class User(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    login = TextField(null=False, unique=True)
    email = TextField(null=False)
    role = IntegerField(null=True)
    password = TextField(null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'login': self.login,
            'email': self.email,
            'role': self.role
        }

    class Meta:
        db_table = 'users'
