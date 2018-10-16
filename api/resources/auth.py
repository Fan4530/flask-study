from flask_restplus import Resource

from ..models import User, user_schema, users_schema


class Login(Resource):
  def post(self):
    pass


class Logout(Resource):
  def post(self):
    pass