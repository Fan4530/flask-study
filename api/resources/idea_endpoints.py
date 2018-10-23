from datetime import datetime
import uuid

from flask_restplus import Resource, reqparse
from flask_jwt_extended import get_jwt_identity

from ..extensions import api
from ..models import User, Idea, idea_schema, ideas_schema
from ..decorators import admin_required, login_required
from ..fields import idea_fields, update_idea_fields


idea_parser = reqparse.RequestParser()
idea_parser.add_argument('type', type=str, help='Must be one of [draft, pitch, title]')
idea_parser.add_argument('user_id', type=str, help="User's public_id")

class IdeasEndpoint(Resource):
  @api.doc(params={'type': 'draft, pitch, or title', 'user': 'user_id'})
  def get(self):
    """Return a list of ideas"""

    args = idea_parser.parse_args()

    return ideas_schema.dump(Idea.objects.all())

  @api.expect(idea_fields)
  @login_required
  def post(self):
    """Create a new idea"""

    user_id = get_jwt_identity()
    idea_data, error = idea_schema.load(api.payload)

    try:
      new_idea = Idea(creator_id=user_id, **idea_data).save()
    except Exception as e:
      return str(e), 400

    return idea_schema.dump(new_idea), 200


class IdeaEndpoint(Resource):
  @login_required
  def get(self, idea_id):
    """Return a specific user entry."""

    idea = Idea.objects.get_or_404(id=idea_id)
    return idea_schema.dump(idea)

  @api.expect(update_idea_fields)
  @login_required
  def patch(self, idea_id):
    """Update the idea"""

    idea = Idea.objects.get_or_404(id=idea_id)

    user_id = get_jwt_identity()
    current_user = User.objects.get_or_404(public_id=user_id)

    idea_data, error = idea_schema.load(api.payload['data'])

    # print(new_idea.pitch_approvals)
    # print(len(new_idea.pitch_approvals))
    # print(new_idea.title_approvals)
    # print(len(new_idea.title_approvals))
    
    if idea_data.get("assignee", None):
      if current_user.role != "admin":
        return {"msg": "Only admins can assign pitches."}, 403

      if idea.assignee:
        return {"msg": "This pitch has already been assigned to {}.".format(idea.assignee)}, 400
    
      if idea.idea_type != "pitch":
        return {"msg": "Only pitches can be assigned."}, 400
      
      assignee_id = uuid.UUID('urn:uuid:{}'.format(idea_data["assignee"]))
      print(type(assignee_id))
      idea.update(assignee=assignee_id, idea_status="assigned", updated_at=datetime.utcnow)

    if idea_data.get("title", None):
      if idea.idea_type == "pitch":
        return {"msg": "Unable to edit pitches."}, 400

      if idea.idea_type == "draft" and current_user.public_id != idea.creator_id:
        return {"msg": "Unable to edit draft."}, 403
    
      if idea.idea_type == "title" and current_user.public_id != idea.assignee:
        return {"msg": "Unable to edit title."}, 403

      idea.update(title=idea_data["title"], updated_at=datetime.utcnow)
    
    if idea_data.get("details", None):
      if idea.idea_type == "pitch":
        return {"msg": "Unable to edit pitches."}, 400
      
      if idea.idea_type == "draft" and current_user.public_id != idea.creator_id:
        return {"msg": "Unable to edit draft."}, 403
    
      if idea.idea_type == "title" and current_user.public_id != idea.assignee:
        return {"msg": "Unable to edit title."}, 403

      idea.update(details=idea_data["details"], updated_at=datetime.utcnow)

    if api.payload.get("action", None) == "pitch":
      if idea.idea_type != "draft" or current_user.public_id != idea.creator_id:
        return {"msg": "You can only pitch your own drafts."}, 403
      
      idea.update(idea_type="pitch", status="awaiting approval", updated_at=datetime.utcnow)

    if api.payload.get("action", None) == "approve pitch":
      if current_user.role != "admin":
        return {"msg": "Only admins can approve pitches."}, 403

      approval = {
        "approver": current_user.public_id,
        "timestamp": datetime.utcnow,
        "approved": 1
      }

      idea.update(status="approved", updated_at=datetime.utcnow)

    new_idea = Idea.objects.get_or_404(id=idea_id)
    
    return idea_schema.dump(new_idea)
  
  @login_required
  def delete(self, idea_id):
    """Delete an idea"""

    idea = Idea.objects.get_or_404(id=idea_id)
    return idea.delete()