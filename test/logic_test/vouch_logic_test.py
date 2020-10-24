import unittest

from test.db_base_test_case import DBBaseTestCase
from model.profile.account import Account
from model.profile.vouch import Vouch
from model.profile.vouch_request import VouchRequest
from logic import vouch_logic

class VouchLogicTest(DBBaseTestCase):
    def test_make_request(self):
        account1 = Account(name = "john")
        account1.save_to_db()
        account2 = Account(name = "jane")
        account2.save_to_db()
        vouch_logic.make_request(account1, account1, account2)
        vr = VouchRequest.find_by_ids(account1.id, account2.id)
        self.assertEqual(vr.top_id, account1.id)
        self.assertEqual(vr.bottom_id, account2.id)

if __name__ == '__main__':
    unittest.main()