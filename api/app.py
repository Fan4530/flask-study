from flask import Flask

from api.resources.goal_endpoints import GoalEndPoint, GoalsEndPoint
from .extensions import api, db, ma, bcrypt, jwt
from .config import app_configs
from .resources import Ping, Login, Logout, UsersEndpoint, UserEndpoint, IdeasEndpoint, IdeaEndpoint


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_configs[config_name])

    db.init_app(app)

    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    api.init_app(app)
    api.title = 'Ideas API'
    api.authorizations = {
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }

    api.add_resource(Ping, '/ping', endpoint='ping')
    api.add_resource(Login, '/auth/login', endpoint='login')
    api.add_resource(Logout, '/auth/logout', endpoint='logout')
    api.add_resource(UsersEndpoint, '/users', endpoint='users')
    api.add_resource(UserEndpoint, '/users/<string:user_id>', endpoint='user')
    api.add_resource(IdeasEndpoint, '/ideas/', endpoint='ideas')
    api.add_resource(IdeaEndpoint, '/ideas/<string:idea_id>', endpoint='idea')

    api.add_resource(GoalsEndPoint, '/goals', endpoint='goals')
    api.add_resource(GoalEndPoint, '/goal/<string:goal_id>', endpoint='goal')

    return app
