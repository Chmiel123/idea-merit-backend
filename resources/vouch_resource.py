from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.profile.account import Account
from logic import vouch_logic
from util import response
from util.exception import IMException

request_parser = reqparse.RequestParser()
request_parser.add_argument('top_id', help = 'This field cannot be blank', required = True)
request_parser.add_argument('bottom_id', help = 'This field cannot be blank', required = True)

class VouchRequest(Resource):
    @jwt_required
    def get(self):
        account = Account.find_by_username(get_jwt_identity())
        vouch_requests = vouch_logic.get_requests(account)
        return [x.to_dict() for x in vouch_requests]

    @jwt_required
    def post(self):
        try:
            data = request_parser.parse_args()
            account = Account.find_by_username(get_jwt_identity())
            top = Account.find_by_id(data['top_id'])
            bottom = Account.find_by_id(data['bottom_id'])
            result = vouch_logic.make_request(account, top, bottom)
            return response.ok(result)
        except IMException as e:
            return response.error(e.args[0])

    @jwt_required
    def delete(self):
        try:
            data = request_parser.parse_args()
            account = Account.find_by_username(get_jwt_identity())
            top = Account.find_by_id(data['top_id'])
            bottom = Account.find_by_id(data['bottom_id'])
            result = vouch_logic.remove_vouch_request(account, top, bottom)
            return response.ok(result)
        except IMException as e:
            return response.error(e.args[0])

class Vouch(Resource):
    @jwt_required
    def get(self):
        account = Account.find_by_username(get_jwt_identity())
        vouches = vouch_logic.get_vouches(account)
        return [x.to_dict() for x in vouches]

    @jwt_required
    def delete(self):
        try:
            data = request_parser.parse_args()
            account = Account.find_by_username(get_jwt_identity())
            top = Account.find_by_id(data['top_id'])
            bottom = Account.find_by_id(data['bottom_id'])
            result = vouch_logic.remove_vouch(account, top, bottom)
            return response.ok(result)
        except IMException as e:
            return response.error(e.args[0])