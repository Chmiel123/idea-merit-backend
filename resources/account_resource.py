from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity
from model.profile.account import Account
from model.profile.login_direct import LoginDirect
from model.profile.account_email import AccountEmail
from model.profile.email_verification import EmailVerification
from logic import email_logic, account_logic
from config.config import config
from util import response
from util.exception import IMException

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', help = 'This field cannot be blank', required = True)
login_parser.add_argument('password', help = 'This field cannot be blank', required = True)

email_parser = reqparse.RequestParser()
email_parser.add_argument('email', help = 'This field cannot be blank', required = True)
email_parser.add_argument('primary')

email_verification_parser = reqparse.RequestParser()
email_verification_parser.add_argument('verify', help = 'This field cannot be blank', location='args', required = True)

class AccountRegistration(Resource):
    def post(self):
        data = login_parser.parse_args()
        try:
            account_logic.create_account_with_password(data['username'], data['password'])

            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'status': 'Ok',
                'message': f'User {data["username"]} was created',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except IMException as e:
            return response.error(e.args[0])


class AccountLogin(Resource):
    def post(self):
        data = login_parser.parse_args()
        try:
            current_account = account_logic.login(data['username'], data['password'])

            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'status': 'Ok',
                'message': f'Logged in as {current_account.name}',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except IMException as e:
            return response.error(e.args[0])


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
            'created_date': str(account.created_date),
            'login': {
                'password': account.login_direct.password
            },
            'emails': dict(account.emails)
        }

class Email(Resource):
    @jwt_required
    def get(self):
        account = Account.find_by_username(get_jwt_identity())
        return {
            'emails': [{'email': x.email, 'verified': x.verified, 'primary': x.primary} for x in account.emails]
        }

    @jwt_required
    def post(self):
        data = email_parser.parse_args()
        account = Account.find_by_username(get_jwt_identity())

        for account_email in account.emails:
            if account_email.email == data['email']:
                if not account_email.verified:
                    email_logic.generate_verification(account_email)
                    #TODO: send actual email
                    return {'message': 'Resent verification email'}
                if data['primary']:
                    email_logic.set_primary(account_email)

        max_emails = config['email']['max_emails_per_account']
        if len(account.emails) >= max_emails:
            return {'message': 'Maximum number of emails per account reached', 'value': max_emails}
        
        account_email = AccountEmail(
            account = account,
            email = data['email']
        )
        account_email.save_to_db()
        if data['primary']:
            email_logic.set_primary(account_email)
        email_logic.generate_verification(account_email)
        #TODO: send actual email
        return {'message': 'Sent verification email'}
    
    @jwt_required
    def delete(self):
        data = email_parser.parse_args()
        account = Account.find_by_username(get_jwt_identity())
        for email in account.emails:
            if email.email == data['email']:
                AccountEmail.delete_by_email(email.email)
                return {'message': 'Sent verification email'}



class EmailVerify(Resource):
    def get(self):
        data = email_verification_parser.parse_args()
        result = email_logic.verify(data['verify'])
        if result:
            return response.ok()
        else:
            return response.error('Could not verify email address')

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
