from datetime import datetime

from marshmallow_mongoengine import ModelSchema

from ..extensions import db, ma


class Goal(db.Document):
    # TODO: what should be required
    assignee = db.StringField(default=None, null=True)
    verticals = db.StringField(required=True, max_length=255)
    deadline = db.StringField(default=None)
    total_number = db.IntField(default=0)
    completed_number = db.IntField(default=0)
    personal_goals = db.ListField(db.StringField(max_length=300), default=[])
    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'goals'}
class GoalSchema(ModelSchema):
  class Meta:
    model = Goal

goal_schema = GoalSchema()
goals_schema = GoalSchema(many=True)