from flask_restplus import Resource, fields
from flask_jwt_extended import create_access_token

from ..extensions import api, bcrypt
from ..models import User, user_schema, users_schema
from ..fields import user_credential_fields


@api.expect(user_credential_fields)
class Login(Resource):
  def post(self):
    """Login and authenticate a user."""
    
    user_data, error = user_schema.load(api.payload)
    
    if not user_data["email"]:
        return {"msg": "Missing username parameter"}, 400
    if not user_data["password"]:
        return {"msg": "Missing password parameter"}, 400

    user = User.objects.get_or_404(email=user_data["email"])
    
    login_successful = bcrypt.check_password_hash(user.password, user_data["password"])

    if not login_successful:
      return {"msg": "Incorrect password"}, 400

    return create_access_token(identity=user.public_id), 200


class Logout(Resource):
  """Logout a user and revoke their token."""

  def post(self):
    pass