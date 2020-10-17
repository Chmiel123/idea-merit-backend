from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity
from model.profile.account import Account
from model.profile.login_direct import LoginDirect
from model.profile.account_email import AccountEmail
from model.profile.email_verification import EmailVerification
from logic import email_logic
from config.config import config

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

email_parser = reqparse.RequestParser()
email_parser.add_argument('email', help = 'This field cannot be blank', required = True)
email_parser.add_argument('primary')

email_verification_parser = reqparse.RequestParser()
email_verification_parser.add_argument('verify', help = 'This field cannot be blank', location='args', required = True)

class AccountRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if Account.find_by_username(data['username']):
            return {'message': f'User {data["username"]} already exists'}

        new_account = Account(
            name = data['username'],
        )
        new_login_direct = LoginDirect(
            password = LoginDirect.generate_hash(data['password']),
            account = new_account
        )

        try:
            new_account.save_to_db()
            new_login_direct.save_to_db()
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
        
        if LoginDirect.verify_hash(data['password'], current_account.login_direct.password):
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
            'emails': [{'email': x.email, 'verified': x.verified} for x in account.emails]
        }

    @jwt_required
    def post(self):
        data = email_parser.parse_args()

        account = Account.find_by_username(get_jwt_identity())
        ev = None

        for email in account.emails:
            if email.email == data['email']:
                if not email.verified:
                    ev = email_logic.generate_verification(email)
                    #TODO: send actual email
                    return {'message': 'Resent verification email'}
                if data['primary']:
                    email.primary = data['primary']
                    email.save_to_db()

        max_emails = config['email']['max_emails_per_account']
        if len(account.emails) >= max_emails:
            return {'message': 'Maximum number of emails per account reached', 'value': max_emails}
        
        account_email = AccountEmail(
            account = account,
            email = data['email']
        )
        if data['primary']:
            account_email.primary = data['primary']
        account_email.save_to_db()
        ev = email_logic.generate_verification(account_email.email)
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
            return {'message': 'Ok'}
        else:
            return {'message': 'Could not verify email address'}

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
