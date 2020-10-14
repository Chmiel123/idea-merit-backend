from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity
from model.profile.account import Account
from model.profile.login_direct import LoginDirect

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

class AccountRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if Account.find_by_username(data['username']):
            return {'message': f'User {data["username"]} already exists'}

        new_account = Account(
            name = data['username'],
        )
        new_direct_login = LoginDirect(
            password = LoginDirect.generate_hash(data['password']),
            account = new_account
        )

        try:
            new_account.save_to_db()
            new_direct_login.save_to_db()
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': f'User {data["username"]} was created',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except:
            return {'message': 'Something went wrong'}, 500


class AccountLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_account = Account.find_by_username(data['username'])

        if not current_account:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        
        if LoginDirect.verify_hash(data['password'], current_account.direct_login.password):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(current_account.name),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}


# class AccountLogoutAccess(Resource):
#     @jwt_required
#     def post(self):
#         jti = get_raw_jwt()['jti']
#         try:
#             revoked_token = RevokedTokenModel(jti = jti)
#             revoked_token.add()
#             return {'message': 'Access token has been revoked'}
#         except:
#             return {'message': 'Something went wrong'}, 500


# class AccountLogoutRefresh(Resource):
#     @jwt_refresh_token_required
#     def post(self):
#         jti = get_raw_jwt()['jti']
#         try:
#             revoked_token = RevokedTokenModel(jti = jti)
#             revoked_token.add()
#             return {'message': 'Refresh token has been revoked'}
#         except:
#             return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}

class CurrentAccount(Resource):
    @jwt_required
    def get(self):
        account = Account.find_by_username(get_jwt_identity())
        return {
            'id': str(account.id),
            'name': account.name,
            'domain': account.domain,
            'registered_date': str(account.registered_date),
            'login': {
                'password': account.direct_login.password
            }
        }

# class Users(Resource):
#     def get(self):
#         return User.return_all()

#     def get(self, id):
#         return User.return_all()
    
#     def delete(self):
#         return User.delete_all()


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }
