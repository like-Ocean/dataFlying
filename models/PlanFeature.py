from models import Plan, Feature
from peewee import BooleanField, ForeignKeyField
from database import BaseModel


class PlanFeature(BaseModel):
    plan = ForeignKeyField(Plan, backref='plan_features', on_delete='CASCADE')
    feature = ForeignKeyField(Feature, backref='plan_features', on_delete='CASCADE')
    is_enabled = BooleanField(default=False)

    def get_dto(self):
        return {
            'plan': {
                'id': self.plan.id,
                'name': self.plan.name,
                'price': self.plan.price,
                'duration_in_hours': self.plan.duration_in_hours
            },
            'feature': {
                'id': self.feature.id,
                'name': self.feature.name,
                'slag': self.feature.slag
            },
            'is_enabled': self.is_enabled
        }

    class Meta:
        db_table = 'plan_feature'
