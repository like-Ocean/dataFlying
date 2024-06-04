from peewee import TextField, AutoField, DecimalField, Check
from database import BaseModel


class Plan(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    name = TextField(null=False)
    description = TextField(null=False)
    price = DecimalField(max_digits=7, decimal_places=2, constraints=[Check('price >= 0')])
    duration_in_hours = DecimalField(max_digits=5, decimal_places=2)

    def get_dto(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'duration_in_hours': self.duration_in_hours
        }

    class Meta:
        db_table = 'plans'
