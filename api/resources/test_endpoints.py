from flask_restplus import Resource


class Ping(Resource):
  """Ping API as a test"""

  def get(self):
    return {"data": "pong"}