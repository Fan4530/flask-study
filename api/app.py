from flask import Flask
from flask_restplus import Api
from flask_mongoengine import MongoEngine
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

from .config import app_configs
from .resources import Login, Logout, User, Users, Idea, Ideas, Ping

api = Api()
db = MongoEngine()
ma = Marshmallow()
bcrypt = Bcrypt()

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(app_configs[config_name])
  
  api = Api(app, title='Ideas API', prefix="/api")
  api.add_resource(Ping, '/ping', endpoint='ping')
  api.add_resource(Login, '/auth/login', endpoint='login')
  api.add_resource(Logout, '/auth/logout', endpoint='logout')
  api.add_resource(Users, '/users', endpoint='users')
  api.add_resource(User, '/users/<int:user_id>', endpoint='user')
  api.add_resource(Ideas, '/ideas/', endpoint='ideas')
  api.add_resource(Idea, '/ideas/<int:idea_id>', endpoint='idea')

  db.init_app(app)
  ma.init_app(app)
  bcrypt.init_app(app)

  return app