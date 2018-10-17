from datetime import datetime

from marshmallow_mongoengine import ModelSchema

from ..extensions import db, ma


class User(db.Document):
  public_id = db.UUIDField(required=True, unique=True)
  email = db.EmailField(required=True, unique=True)
  password = db.StringField(max_length=80, required=True)
  first_name = db.StringField(max_length=50)
  last_name = db.StringField(max_length=50)
  role = db.StringField(default="writer", validation=lambda role: role in ["writer", "admin"])
  created_at = db.DateTimeField(default=datetime.utcnow)

  meta = {'collection': 'users'}


class UserSchema(ModelSchema):
    class Meta:
        model = User


user_schema = UserSchema(load_only=("id", "password", "created_at"))
users_schema = UserSchema(many=True)
