import sys
from flask import request
from flask_restplus import Resource

from api.fields import goal_fields
from ..extensions import api

from api.models import goals_schema, Goal, goal_schema, User


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

        json_body = request.get_json(force=True)
        print(json_body, file=sys.stderr)

        goal, error = goal_schema.load(json_body)
        if error:
            return "Schema load error, check your request body!", 500

        # print("The goal body is : ", file=sys.stderr)
        # print(goal_schema.dump(goal), file=sys.stderr)

        contributors = User.objects(role="contributor")
        len_contributors = len(contributors)
        total_goals = json_body["total_number"]
        personal_total_goals = int(total_goals / len_contributors)
        mark_idx = total_goals % len_contributors
        print(personal_total_goals)

        for i in range(len_contributors):
            assignee_id = str(contributors[i].id)

            print(assignee_id, file=sys.stderr)

            personal_goal = Goal(verticals=json_body["verticals"],
                                 assignee=assignee_id,
                                 deadline=json_body["deadline"],
                                 total_number=personal_total_goals + 1
                                 )
            if i < mark_idx:
                personal_goal.total_number = personal_total_goals
            personal_goal = personal_goal.save()
            goal.personal_goals.append(str(personal_goal.id))

        try:
            print(goal.personal_goals)
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

        goal_patch = request.get_json(force=True)
        try:
            goal.update(**goal_patch)
            print('The goal has been changed!', file=sys.stderr)
        except Exception as e:
            return str(e), 400

        try:
            new_total_number = goal_patch["total_number"]
        except Exception as e:
            new_total_number = None

        # start to update personal goals
        if goal.personal_goals and new_total_number is not None:

            len_contributors = len(goal.personal_goals)

            print("show change content json", file=sys.stderr)
            print(goal_patch, file=sys.stderr)

            personal_total_goals = int(new_total_number / len_contributors)
            mark_idx = new_total_number % len_contributors
            for c, assignee in enumerate(goal.personal_goals):
                print(c, file=sys.stderr)
                print(assignee, file=sys.stderr)

                personal_goal = Goal.objects(id=str(assignee))

                print("personal goal has been fetched: ", file=sys.stderr)
                print(personal_goal, file=sys.stderr)

                if c < mark_idx:
                    goal_patch["total_number"] = personal_total_goals
                else:
                    goal_patch["total_number"] = personal_total_goals + 1

                print("The new goal patch is :", file=sys.stderr)
                print(goal_patch, file=sys.stderr)

                personal_goal.update(**goal_patch)

        return "Global and personal goals have been changed"
