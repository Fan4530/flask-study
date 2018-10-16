from flask_restplus import Resource

from ..models import User


class Users(Resource):
  def get(self):
    pass

  def post(self):
    pass


class User(Resource):
  def get(self, id):
    pass

  def put(self, id):
    pass
  
  def delete(self, id):
    pass