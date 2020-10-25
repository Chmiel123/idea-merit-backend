import unittest
import json

from test.app_base_test_case import AppBaseTestCase
from model.profile.account import Account
from model.profile.email_verification import EmailVerification

class UserResourceTest(AppBaseTestCase):
    def test_register(self):
        self.register('user', 'pass')
        user = Account.find_by_username('user')
        self.assertEqual(user.name, 'user')
        result = self.register('user', 'pass')
        self.assertEqual(result.json['status'], 'Error')

    def test_register_login(self):
        self.register('user', 'pass')
        result = self.login('user', 'pass')
        self.assertEqual(result.json['message'], 'Logged in as user')

    def test_email(self):
        self.register_and_login()
        result = self.post_auth(
            '/account/email',
            dict(email = 'user@example.com')
        )
        result = self.post_auth(
            '/account/email',
            data=dict(email = 'user@example.net')
        )
        result = self.get_auth(
            '/account/email'
        )
        self.assertEqual(result.json['emails'][0]['email'], 'user@example.com')
        self.assertEqual(result.json['emails'][1]['email'], 'user@example.net')
        ev = self.db.session.query(EmailVerification).filter_by(email = 'user@example.com').first()
        result = self.get_auth(
            '/account/email/verify?verify=abc'
        )
        self.assertEqual(result.json['message'], 'Could not verify email address')
        result = self.get_auth(
            f'/account/email/verify?verify={ev.verification_key}'
        )
        self.assertEqual(result.json['message'], 'Ok')

    def test_email_limit(self):
        self.register_and_login()
        result = self.post_auth(
            '/account/email',
            data=dict(email = 'user@example.com')
        )
        self.assertEqual(result.json['message'], 'Sent verification email')
        result = self.post_auth(
            '/account/email',
            data=dict(email = 'user@example.net')
        )
        self.assertEqual(result.json['message'], 'Sent verification email')
        result = self.post_auth(
            '/account/email',
            data=dict(email = 'user@info.net')
        )
        self.assertEqual(result.json['message'], 'Sent verification email')
        result = self.post_auth(
            '/account/email',
            data=dict(email = 'user@info.com')
        )
        self.assertEqual(result.json['message'], 'Maximum number of emails per account reached')

        
    def test_email_delete(self):
        self.register_and_login()
        result = self.post_auth(
            '/account/email',
            data=dict(email = 'user@example.com')
        )
        result = self.post_auth(
            '/account/email',
            data=dict(email = 'user@example.net')
        )
        result = self.delete_auth(
            '/account/email',
            data=dict(email = 'user@example.com')
        )
        result = self.get_auth(
            '/account/email'
        )
        self.assertEqual(len(result.json['emails']), 1)
        self.assertEqual(result.json['emails'][0]['email'], 'user@example.net')


    def test_secret(self):
        self.register_and_login()
        result = self.get_auth(
            '/secret'
        )
        self.assertEqual(result.json['answer'], 42)
        
if __name__ == '__main__':
    unittest.main()