from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.profile.account import Account
from logic import idea_logic
from util import response
from util.exception import IMException

idea_get_parser = reqparse.RequestParser()
idea_get_parser.add_argument('id', location='args', required = False)
idea_get_parser.add_argument('name', location='args', required = False)
idea_get_parser.add_argument('parent_id', location='args', required = False)
idea_get_parser.add_argument('author_id', location='args', required = False)
idea_get_parser.add_argument('page', location='args', required = False, type = int)

idea_post_parser = reqparse.RequestParser()
idea_post_parser.add_argument('parent_id', help = 'This field cannot be blank', required = True)
idea_post_parser.add_argument('name', help = 'This field cannot be blank', required = True)
idea_post_parser.add_argument('content', help = 'This field cannot be blank', required = True)
idea_post_parser.add_argument('initial_resource', help = 'This field cannot be blank', required = True, type=float)

vote_parser = reqparse.RequestParser()
vote_parser.add_argument('idea_id', help = 'This field cannot be blank', required = True)
vote_parser.add_argument('resource', help = 'This field cannot be blank', required = True)

class Idea(Resource):
    def get(self):
        try:
            data = idea_get_parser.parse_args()
            if data['id']:
                found = idea_logic.get_by_id(data['id'])
                if not found:
                    return response.error('Idea not found')
                return found.to_dict()
            elif data['name']:
                found = idea_logic.get_by_name(data['name'])
                if not found:
                    return response.error('Idea not found')
                return found.to_dict()
            elif data['parent_id']:
                return [x.to_dict() for x in idea_logic.get_by_parent_id(data['parent_id'], data['page'])]
            elif data['author_id']:
                return [x.to_dict() for x in idea_logic.get_by_author_id(data['author_id'], data['page'])]
            else:
                return [x.to_dict() for x in idea_logic.get_root_ideas(data['page'])]
        except IMException as e:
            return response.error(e.args[0])

    @jwt_required
    def post(self):
        account = Account.find_by_username(get_jwt_identity())
        data = idea_post_parser.parse_args()
        try:
            idea_logic.create_idea(account, data['parent_id'], data['name'], data['content'], data['initial_resource'])
            return response.ok()
        except IMException as e:
            return response.error(e.args[0])

class VoteIdea(Resource):
    @jwt_required
    def post(self):
        account = Account.find_by_username(get_jwt_identity())
        data = vote_parser.parse_args()
        try:
            result = idea_logic.vote(account, data['idea_id'], float(data['resource']))
            return response.ok(result)
        except IMException as e:
            return response.error(e.args[0])