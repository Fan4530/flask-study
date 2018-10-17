from functools import wraps

from flask import abort, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from .extensions import api
from .models import User

def admin_required(f):
  @wraps(f)
  @api.doc(security='apikey')
  def decorated_fucntion(*args, **kwargs):

    try:
      verify_jwt_in_request()
    except Exception as e:
      abort(403, {'msg': "Invalid JWT or login credentials"})

    current_user_id = get_jwt_identity()
    current_user = User.objects.get_or_404(public_id=current_user_id)

    if not current_user.role == "admin":
      abort(403, {'msg': 'Admin status required'})
    
    return f(*args, **kwargs)
  
  return decorated_fucntion


def login_required(f):
  @wraps(f)
  @api.doc(security='apikey')
  def decorated_fucntion(*args, **kwargs):

    try:
      verify_jwt_in_request()
    except Exception as e:
      abort(403, {'msg': "Invalid JWT or login credentials"})
    
    return f(*args, **kwargs)
  
  return decorated_fucntion
