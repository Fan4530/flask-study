from flask_restplus import Resource

from ..models import Idea, idea_schema, ideas_schema


class IdeasEndpoint(Resource):
  def get(self):
    pass

  def post(self):
    pass


class IdeaEndpoint(Resource):
  def get(self, id):
    pass

  def put(self, id):
    pass
  
  def delete(self, id):
    pass