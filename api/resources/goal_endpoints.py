import sys
from flask import request
from flask_restplus import Resource
import logging

from api.fields import goal_fields
from ..extensions import api

from api.models import goals_schema, Goal, goal_schema, User


class GoalsEndPoint(Resource):
    goals_logger = logging.getLogger('Goals')
    goals_logger.setLevel(logging.NOTSET)

    def get(self):
        """Return a list of goals with filters"""
        filters = request.get_json(force=True)
        self.goals_logger.info('info Return a list of goals with filters: ')
        self.goals_logger.info(filters)

        goals = Goal.objects(__raw__=filters)
        return goals_schema.dump(goals)

    @api.expect(goal_fields)
    def post(self):
        """Create a new goal"""
        request_body = request.get_json(force=True)
        self.goals_logger.info('Start to create a new goal')
        self.goals_logger.debug('The request body is: %s', request_body)

        goal, error = goal_schema.load(request_body)
        if error:
            self.goals_logger.error("Schema load error, check your request body!")
            return None, 500

        # print("The goal body is : ", file=sys.stderr)
        # print(goal_schema.dump(goal), file=sys.stderr)

        contributors = User.objects(role="contributor")
        len_contributors = len(contributors)
        total_goals = request_body["total_number"]

        personal_total_goals = int(total_goals / len_contributors)
        self.goals_logger.debug('The personal total goals numbers is: %s', personal_total_goals)

        mark_idx = total_goals % len_contributors

        for c, contributor in enumerate(contributors):
            assignee_id = str(contributor.id)

            self.goals_logger.debug("Start to create goal for %s", assignee_id)

            personal_goal = Goal(verticals=request_body["verticals"],
                                 assignee=assignee_id,
                                 deadline=request_body["deadline"],
                                 total_number=personal_total_goals + 1
                                 )
            if c < mark_idx:
                personal_goal.total_number = personal_total_goals

            personal_goal = personal_goal.save()
            goal.personal_goals.append(str(personal_goal.id))

        try:
            new_goal = goal.save()
            self.goals_logger.info('The new global goal has been saved!')
        except Exception as e:
            self.goals_logger.error("Fail to save, %s", str(e))
            return str(e), 400
        # TODO: Fan -- why there is two elements in the return lists?
        return goal_schema.dump(new_goal), 200


class GoalEndPoint(Resource):
    goal_logger = logging.getLogger('Goal')
    goal_logger.setLevel(logging.NOTSET)
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
            self.goal_logger.debug('The goal has been changed!')
        except Exception as e:
            return str(e), 400

        self.goal_logger.info('Check if need to change the total goal number..')
        try:
            new_total_number = goal_patch["total_number"]
            self.goal_logger.debug('The total number has been changed to %s', new_total_number)
        except Exception as e:
            self.goal_logger.debug('The total goals number has no change')
            new_total_number = goal.total_number

        self.goal_logger.info('start to update personal goals')
        if goal.personal_goals:

            self.goal_logger.debug("show change content json: %s", goal_patch)

            personal_total_goals = int(new_total_number / len(goal.personal_goals))
            mark_idx = new_total_number % len(goal.personal_goals)

            for c, goal_id in enumerate(goal.personal_goals):
                self.goal_logger.debug("idx: %d, goal_id: %s", c, goal_id)

                personal_goal = Goal.objects(id=str(goal_id))

                self.goal_logger.debug("Personal goal %s has been fetched", personal_goal)


                if c < mark_idx:
                    goal_patch["total_number"] = personal_total_goals + 1
                else:
                    goal_patch["total_number"] = personal_total_goals

                self.goal_logger.debug("The new goal patch is: %s", goal_patch)

                personal_goal.update(**goal_patch)

        self.goal_logger.debug("Global and personal goals have been changed", goal_patch)
        return 200
