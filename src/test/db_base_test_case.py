import unittest
import test.base_test_setup 
from model.db import db

class DBBaseTestCase(unittest.TestCase):
    """ Base Tests using a test database"""

    def setUp(self):
        self.db = db
        db.session.commit()
        db.drop_all()
        db.Base.metadata.create_all(db.engine)
        db.session.commit()

    def tearDown(self):
        pass
