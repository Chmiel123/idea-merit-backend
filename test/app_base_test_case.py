import unittest
import base_test_setup 
from model.db import db
from app import app

class AppBaseTestCase(unittest.TestCase):
    """ Base Tests using a test database"""

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        db.session.commit()
        db.Base.metadata.drop_all()
        db.Base.metadata.create_all(db.engine)
        db.session.commit()

    def tearDown(self):
        pass
