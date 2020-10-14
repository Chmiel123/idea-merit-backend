import unittest
import json

from test.app_base_test_case import AppBaseTestCase
from model.profile.account import Account

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