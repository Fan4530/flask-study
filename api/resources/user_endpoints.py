import uuid

from flask_restplus import Resource, fields

from ..extensions import api, db, bcrypt
from ..models import User, user_schema, users_schema


required_user_credentials = api.model('Required user credentials.', {
    'email': fields.String,
    'password': fields.String,
})

required_user_update_fields = api.model('Required fields for updating a user entry.', {
    'action': fields.String,
    'property': fields.String
})

class UsersEndpoint(Resource):
  def get(self):
    """Return a list of users."""

    return users_schema.dump(User.objects.all())

  @api.expect(required_user_credentials)
  def post(self):
    """Create a new user."""

    user_data, error = user_schema.load(api.payload)
    user_data["public_id"] = uuid.uuid4()

    try:
      pswd = user_data["password"]
    except KeyError as e:
      return {"msg": "Password required."}, 400
    else:
      user_data["password"] = bcrypt.generate_password_hash(pswd)

    try:
      new_user = User(**user_data).save()
    except Exception as e:
      return str(e), 400
    
    return user_schema.dump(new_user), 200


class UserEndpoint(Resource):
  def get(self, user_id):
    """Return a specific user entry."""

    user = User.objects.get_or_404(public_id=user_id)
    return user_schema.dump(user)

  @api.expect(required_user_update_fields)
  def put(self, user_id):
    """Update a user entry."""

    user_data, error = user_schema.load(api.payload)
    user = User.objects.get_or_404(public_id=user_id)
    user.role = user_data["role"]
    
    return user_schema.dump(user.save())

  def delete(self, user_id):
    """Delete a specific user entry."""

    user = User.objects.get_or_404(public_id=user_id)
    return user.delete()