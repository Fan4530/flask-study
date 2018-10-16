from flask_restplus import Api
from flask_mongoengine import MongoEngine
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

api = Api()
db = MongoEngine()
ma = Marshmallow()
bcrypt = Bcrypt()