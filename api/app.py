from flask import Flask

from .extensions import api, db, ma, bcrypt
from .config import app_configs
from .resources import Login, Logout, User, Users, Idea, Ideas, Ping



def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(app_configs[config_name])
  
  api.app = app
  api.title = 'Ideas API'
  api.prefix = "/api"
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