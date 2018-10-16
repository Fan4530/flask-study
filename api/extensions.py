from flask_restplus import Api
from flask_mongoengine import MongoEngine
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

api = Api()
db = MongoEngine()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()