import unittest
import json

from test.app_base_test_case import AppBaseTestCase
from model.profile.account import Account
from model.profile.email_verification import EmailVerification
from model.profile.password_reset import PasswordReset

class UserResourceTest(AppBaseTestCase):
    def test_register(self):
        self.register('user', 'pass')
        user = Account.find_by_username('user')
        self.assertEqual(user.name, 'user')
        result = self.register('user', 'pass')
        self.assertEqual(result.json['status'], 'Error')

    def test_register_login(self):
        self.register('user', 'pass')
        user = self.login('user', 'pass')
        self.assertEqual(user.name, 'user')
        user = self.login('user', 'wrong')
        self.assertIsNone(user)

    def test_register_with_email(self):
        result = self.app.post(
            '/account/register',
            data=dict(username = 'user', password = 'pass', email = 'user@example.com'),
            follow_redirects=True
        )
        user = self.login('user', 'pass')
        self.assertEqual(user.name, 'user')
        result = self.get_auth(
            '/account/email'
        )
        self.assertEqual(result.json['emails'][0]['email'], 'user@example.com')


    def test_password_reset(self):
        self.register('user', 'pass')
        user = self.login('user', 'pass')
        self.assertEqual(user.name, 'user')
        result = self.post_auth(
            '/account/email',
            dict(email = 'user@example.com')
        )
        self.assertEqual(result.json['status'], 'Ok')
        result = self.post_auth(
            '/account/password_reset_gen',
            dict(email = 'user@example.com')
        )
        self.assertEqual(result.json['status'], 'Ok')
        pr = PasswordReset.find_by_account_id(user.id)
        result = self.post_auth(
            '/account/password_reset_verify',
            dict(
                verification_key = pr.verification_key,
                password = 'pass2'
            )
        )
        self.assertEqual(result.json['status'], 'Ok')
        user = self.login('user', 'pass2')
        self.assertEqual(user.name, 'user')

    def test_login_refresh(self):
        self.register('user', 'pass')
        user = self.login('user', 'pass')
        self.assertEqual(user.name, 'user')
        result = self.app.get(
            '/account/refresh',
            headers={'Authorization': f'Bearer {user.refresh_token}'},
        )
        self.assertIsNotNone(result.json['access_token'])

    def test_current_account(self):
        self.register_and_login()
        result = self.get_auth(
            '/account/current'
        )
        self.assertIsNotNone(result.json['id'])

    def test_get_account(self):
        self.register_and_login('john', 'pass')
        self.register_and_login('jane', 'pass')
        result = self.app.get(
            '/account?name=john'
        )
        self.assertEqual(result.json['name'], 'john')
        result = self.app.get(
            f"/account?id={result.json['id']}"
        )
        self.assertEqual(result.json['name'], 'john')
        result = self.app.get(
            '/account?name=jane'
        )
        self.assertEqual(result.json['name'], 'jane')

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
        result = self.post_auth(
            '/account/email',
            data=dict(email = 'user@example.net')
        )
        self.assertEqual(result.json['message'], 'Resent verification email')
        result = self.get_auth(
            '/account/email'
        )
        self.assertEqual(result.json['emails'][0]['email'], 'user@example.com')
        self.assertEqual(result.json['emails'][1]['email'], 'user@example.net')
        ev = self.db.session.query(EmailVerification).filter_by(email = 'user@example.com').first()
        result = self.get_auth(
            '/account/email/verify?verify=abc'
        )
        self.assertEqual(result.json['message'], 'Email could not be verified')
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
        self.assertEqual(result.json['message'], 'Maximum number of emails (3) per account reached')

        
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

        result = self.delete_auth(
            '/account/email',
            data=dict(email = 'user@nonexistent.com')
        )
        self.assertEqual(result.json['message'], 'Email not found')
        self.register_and_login()
        result = self.delete_auth(
            '/account/email',
            data=dict(email = 'user@example.com')
        )
        self.assertEqual(result.json['message'], 'Email not found')

    def test_email_primary(self):
        self.register_and_login()
        result = self.post_auth(
            '/account/email',
            data=dict(email = 'user@example.com', primary = True)
        )
        result = self.post_auth(
            '/account/email',
            data=dict(email = 'user@example.net', primary = False)
        )
        result = self.get_auth(
            '/account/email'
        )
        self.assertTrue(result.json['emails'][0]['primary'])
        self.assertFalse(result.json['emails'][1]['primary'])
        result = self.post_auth(
            '/account/email',
            data=dict(email = 'user@example.eu')
        )
        result = self.post_auth(
            '/account/email',
            data=dict(email = 'user@example.net', primary = True)
        )
        result = self.get_auth(
            '/account/email'
        )
        self.assertEqual(len(result.json['emails']), 3)
        self.assertFalse(result.json['emails'][0]['primary'])
        self.assertFalse(result.json['emails'][1]['primary'])
        self.assertTrue(result.json['emails'][2]['primary'])

    def test_secret(self):
        self.register_and_login()
        result = self.get_auth(
            '/secret'
        )
        self.assertEqual(result.json['answer'], 42)
        
if __name__ == '__main__':
    unittest.main()