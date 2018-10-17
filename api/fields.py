from flask_restplus import fields

from .extensions import api


user_fields = api.model('User fields', {
    'email': fields.String,
    'password': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'role': fields.String
})

user_credential_fields = api.model('User credential fields', {
    'email': fields.String,
    'password': fields.String,
})

update_user_fields = api.model('Upate user fields', {
    'action': fields.String,
    'data': fields.Nested(user_fields)
})