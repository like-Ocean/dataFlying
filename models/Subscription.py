import datetime

from models import User, Plan
from peewee import ForeignKeyField, DateTimeField, AutoField
from database import BaseModel


# Добавил id
class Subscription(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    user = ForeignKeyField(User, backref='subscriptions', on_delete='CASCADE')
    plan = ForeignKeyField(Plan, backref='subscriptions', on_delete='CASCADE')
    start_date = DateTimeField(default=datetime.datetime.now)

    def get_dto(self):
        return {
            'id': self.id,
            'user': {
                'id': self.user.id,
                'login': self.user.login,
                'email': self.user.email,
                'IMEI': self.user.IMEI
            },
            'plan': {
                'id': self.plan.id,
                'name': self.plan.name,
                'duration_in_hours': self.plan.duration_in_hours
            },
            'start_date': self.start_date
        }

    class Meta:
        db_table = 'subscriptions'

