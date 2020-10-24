import unittest
import test.base_test_setup 
from model.db import db
from app import app

class AppBaseTestCase(unittest.TestCase):
    ''' Base Tests using a test database and a flask app'''

    def setUp(self):
        self.db = db
        app.testing = True
        self.app = app.test_client()
        db.session.commit()
        db.drop_all()
        db.Base.metadata.create_all(db.engine)
        db.session.commit()

    def tearDown(self):
        pass

    def get_auth(self, url):
        return self.app.get(
            url,
            headers={'Authorization': f'Bearer {self.access_token}'},
            follow_redirects=True
        )
    def post_auth(self, url, data):
        return self.app.post(
            url,
            headers={'Authorization': f'Bearer {self.access_token}'},
            data=data,
            follow_redirects=True
        )

    def put_auth(self, url, data):
        return self.app.put(
            url,
            headers={'Authorization': f'Bearer {self.access_token}'},
            data=data,
            follow_redirects=True
        )
    def delete_auth(self, url, data):
        return self.app.delete(
            url,
            headers={'Authorization': f'Bearer {self.access_token}'},
            data=data,
            follow_redirects=True
        )

    def register_and_login(self, username='user', password='pass'):
        self.register(username, password)
        self.access_token = self.login(username, password).json['access_token']

    def register(self, username, password):
        return self.app.post(
            '/account/register',
            data=dict(username = username, password = password),
            follow_redirects=True
        )

    def login(self, username, password):
        return self.app.post(
            '/account/login',
            data=dict(username = username, password = password),
            follow_redirects=True
        )
