import sys

from flask import request
from flask_restplus import Resource

from api.fields import goal_fields
from ..extensions import api

from api.models import goals_schema, Goal, goal_schema


class GoalsEndPoint(Resource):


    def get(self):
        """Return a list of goals with filters"""
        filters = request.get_json(force=True);
        print('Return a list of goals with filters: ', file=sys.stderr)
        print(filters, file=sys.stderr)
        goals = Goal.objects(__raw__=filters)
        return goals_schema.dump(goals)


    @api.expect(goal_fields)
    def post(self):
        """Create a new goal"""
        print('Start to create a new goal!', file=sys.stderr)

        print(request.get_json(force=True), file=sys.stderr)

        goal, error = goal_schema.load(request.get_json(force=True))
        if error:
            return "Schema load error, check your request body!", 500

        # print("The goal body is : ", file=sys.stderr)
        # print(goal_schema.dump(goal), file=sys.stderr)

        try:
            new_goal = goal.save()
            print('The new goal has been saved!', file=sys.stderr)
        except Exception as e:
            return str(e), 400
        # TODO: Fan -- why there is two elements in the return lists?
        return goal_schema.dump(new_goal), 200


class GoalEndPoint(Resource):
    def get(self, goal_id):
        """Return a specific goal."""
        goal = Goal.objects.get_or_404(id=goal_id)
        return goal_schema.dump(goal)

    def delete(self, goal_id):
        """Delete a goal"""
        goal = Goal.objects.get_or_404(id=goal_id)
        return goal.delete()

    @api.expect(goal_fields)
    def patch(self, goal_id):
        """Update a goal"""
        print("Start to update a new goal ", file=sys.stderr)
        goal = Goal.objects.get_or_404(id=goal_id)
        try:
            goal.update(**request.get_json(force=True))
            return 'The goal has been changed!', 200
        except Exception as e:
            return str(e), 400
        # TODO: the gaol that is return is not updated
        # return goal_schema.dump(goal)
