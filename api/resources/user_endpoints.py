from datetime import datetime
import uuid

from flask_restplus import Resource

from ..extensions import api, bcrypt
from ..models import User, user_schema, users_schema
from ..decorators import admin_required, login_required
from ..fields import user_fields, user_credential_fields, update_user_fields


class UsersEndpoint(Resource):
  @admin_required
  def get(self):
    """Return a list of users."""

    return users_schema.dump(User.objects.all())
  
  @api.expect(user_fields)
  @admin_required
  def post(self):
    """Create a new user."""

    user_data, error = user_schema.load(api.payload)
    user_data["public_id"] = uuid.uuid4()

    try:
      pswd = user_data["password"]
    except KeyError as e:
      return {"msg": "Password required."}, 400
    else:
      user_data["password"] = bcrypt.generate_password_hash(pswd).decode('utf-8')

    try:
      new_user = User(**user_data).save()
    except Exception as e:
      return str(e), 400
    
    return user_schema.dump(new_user), 200


class UserEndpoint(Resource):
  @login_required
  def get(self, user_id):
    """Return a specific user entry."""

    user = User.objects.get_or_404(public_id=user_id)
    return user_schema.dump(user)

  @api.expect(update_user_fields)
  @admin_required
  def put(self, user_id):
    """Update a user entry."""

    user_data, error = user_schema.load(api.payload['data'])

    user = User.objects.get_or_404(public_id=user_id)
    user.update(updated_at=datetime.utcnow, **user_data)
    
    return user_schema.dump(user)

  @admin_required
  def delete(self, user_id):
    """Delete a specific user entry."""

    user = User.objects.get_or_404(public_id=user_id)
    return user.delete()