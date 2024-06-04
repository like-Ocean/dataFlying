from peewee import AutoField, TextField
from database import BaseModel


class Feature(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    name = TextField(null=False)
    slag = TextField(null=False)
    description = TextField(null=True)

    def get_dto(self):
        return {
            'id': self.id,
            'name': self.name,
            'slag': self.slag,
            'description': self.description,
        }

    class Meta:
        db_table = 'features'
