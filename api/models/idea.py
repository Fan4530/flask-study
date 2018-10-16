from marshmallow_mongoengine import ModelSchema

from ..extensions import db


class Idea(db.Document):
  pass 


class IdeaSchema(ModelSchema):
    class Meta:
        model = Idea


idea_schema = IdeaSchema()
ideas_schema = IdeaSchema(many=True)