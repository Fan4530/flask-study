from marshmallow_mongoengine import ModelSchema

from ..extensions import db


class User(db.Document):
  pass 


class UserSchema(ModelSchema):
    class Meta:
        model = User


user_schema = UserSchema()
users_schema = UserSchema(many=True)
