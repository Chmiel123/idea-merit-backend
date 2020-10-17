import unittest
import json

from test.app_base_test_case import AppBaseTestCase
from model.profile.account import Account
from model.profile.email_verification import EmailVerification

def register(app, username, password):
    return app.post(
        '/account/register',
        data=dict(username = username, password = password),
        follow_redirects=True
    )

def login(app, username, password):
    return app.post(
        '/account/login',
        data=dict(username = username, password = password),
        follow_redirects=True
    )

class UserResourceTest(AppBaseTestCase):
    def test_register(self):
        register(self.app, 'user', 'pass')
        user = Account.find_by_username('user')
        self.assertEqual(user.name, 'user')

    
    def test_register_login(self):
        register(self.app, 'user', 'pass')
        result = login(self.app, 'user', 'pass')
        self.assertEqual(result.json['message'], 'Logged in as user')

    def test_email(self):
        register(self.app, 'user', 'pass')
        access_token = login(self.app, 'user', 'pass').json['access_token']
        result = self.app.post(
            '/account/email',
            headers={"Authorization": f"Bearer {access_token}"},
            data=dict(email = 'user@example.com'),
            follow_redirects=True
        )
        result = self.app.post(
            '/account/email',
            headers={"Authorization": f"Bearer {access_token}"},
            data=dict(email = 'user@example.net'),
            follow_redirects=True
        )
        result = self.app.get(
            '/account/email',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
            follow_redirects=True,
        )
        self.assertEqual(result.json['emails'][0]['email'], 'user@example.com')
        self.assertEqual(result.json['emails'][1]['email'], 'user@example.net')
        ev = self.db.session.query(EmailVerification).filter_by(email = 'user@example.com').first()
        result = self.app.get(
            '/account/email/verify?verify=abc',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
            follow_redirects=True,
        )
        self.assertEqual(result.json['message'], 'Could not verify email address')
        result = self.app.get(
            f'/account/email/verify?verify={ev.verification_key}',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
            follow_redirects=True,
        )
        self.assertEqual(result.json['message'], 'Ok')

    def test_email_limit(self):
        register(self.app, 'user', 'pass')
        access_token = login(self.app, 'user', 'pass').json['access_token']
        result = self.app.post(
            '/account/email',
            headers={"Authorization": f"Bearer {access_token}"},
            data=dict(email = 'user@example.com'),
            follow_redirects=True
        )
        self.assertEqual(result.json['message'], 'Sent verification email')
        result = self.app.post(
            '/account/email',
            headers={"Authorization": f"Bearer {access_token}"},
            data=dict(email = 'user@example.net'),
            follow_redirects=True
        )
        self.assertEqual(result.json['message'], 'Sent verification email')
        result = self.app.post(
            '/account/email',
            headers={"Authorization": f"Bearer {access_token}"},
            data=dict(email = 'user@info.net'),
            follow_redirects=True
        )
        self.assertEqual(result.json['message'], 'Sent verification email')
        result = self.app.post(
            '/account/email',
            headers={"Authorization": f"Bearer {access_token}"},
            data=dict(email = 'user@info.com'),
            follow_redirects=True
        )
        self.assertEqual(result.json['message'], 'Maximum number of emails per account reached')

        


    def test_secret(self):
        register(self.app, 'user', 'pass')
        access_token = login(self.app, 'user', 'pass').json['access_token']
        result = self.app.get(
            '/secret',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
            follow_redirects=True
        )
        self.assertEqual(result.json['answer'], 42)
        
if __name__ == '__main__':
    unittest.main()