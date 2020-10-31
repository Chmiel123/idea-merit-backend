"""Main entry for the app. Declared routes"""

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

from config.config import config
import resources.account_resource
import resources.vouch_resource

app = Flask(__name__)
app.config['SECRET_KEY'] = config['other']['secret_key']
app.config['JWT_SECRET_KEY'] = config['other']['jwt_secret_key']

jwt = JWTManager(app)
api = Api(app)

if __name__ == "__main__":
    app.run()

@app.route('/ping')
def index():
    return 'pong'


api.add_resource(resources.account_resource.AccountRegistration, '/account/register')
api.add_resource(resources.account_resource.AccountLogin, '/account/login')
api.add_resource(resources.account_resource.TokenRefresh, '/account/refresh')
api.add_resource(resources.account_resource.PasswordResetGen, '/account/password_reset_gen')
api.add_resource(resources.account_resource.PasswordResetVerify, '/account/password_reset_verify')
api.add_resource(resources.account_resource.CurrentAccount, '/account/current')
api.add_resource(resources.account_resource.Email, '/account/email')
api.add_resource(resources.account_resource.EmailVerify, '/account/email/verify')
api.add_resource(resources.account_resource.SecretResource, '/secret')
api.add_resource(resources.vouch_resource.VouchRequest, '/vouch/vouch_request')
api.add_resource(resources.vouch_resource.Vouch, '/vouch/vouch')
