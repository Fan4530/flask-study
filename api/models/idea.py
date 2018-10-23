from datetime import datetime

from marshmallow_mongoengine import ModelSchema

from ..extensions import db


class Idea(db.Document):
  creator_id = db.UUIDField(required=True)
  assignee = db.UUIDField(default=None, null=True)
  title = db.StringField(required=True, max_length=255)
  details = db.StringField(max_length=1024)
  idea_type = db.StringField(default="draft", validation=lambda idea_type: idea_type in ["draft", "pitch", "title"])
  status = db.StringField(default="drafted", validation=lambda status: status in ["drafted", "awaiting approval", "approved", "parked", "rejected", "assigned"])
  created_at = db.DateTimeField(default=datetime.utcnow)
  updated_at = db.DateTimeField(default=datetime.utcnow)
  pitch_approvals = db.ListField(field=db.DictField(null=True), default=lambda: [])
  title_approvals = db.ListField(field=db.DictField(null=True), default=lambda: [])

  meta = {'collection': 'ideas'}

class IdeaSchema(ModelSchema):
  class Meta:
    model = Idea

display_only_fields = ("creator_id")
idea_schema = IdeaSchema(dump_only=display_only_fields)
ideas_schema = IdeaSchema(dump_only=display_only_fields, many=True)