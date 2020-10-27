import unittest

from test.db_base_test_case import DBBaseTestCase
from util.exception import IMException
from model.profile.account import Account
from model.profile.vouch import Vouch
from model.profile.vouch_request import VouchRequest
from logic import vouch_logic

class VouchLogicTest(DBBaseTestCase):
    def test_make_request(self):
        account1 = Account('john')
        account1.save_to_db()
        account2 = Account('jane')
        account2.save_to_db()
        account3 = Account('joe')
        account3.save_to_db()
        vouch_logic.make_request(account1, account1, account2)
        vr = VouchRequest.find_by_ids(account1.id, account2.id)
        self.assertIsNotNone(vr)
        self.assertEqual(vr.top_id, account1.id)
        self.assertEqual(vr.bottom_id, account2.id)
        self.assertRaises(IMException, vouch_logic.make_request, account2, account1, account1)
        self.assertRaises(IMException, vouch_logic.make_request, account1, account2, account3)
        vouch_logic.make_request(account1, account2, account1)
        vr = VouchRequest.find_by_ids(account2.id, account1.id)
        self.assertIsNotNone(vr)

    def test_accept_request(self):
        account1 = Account('john')
        account1.save_to_db()
        account2 = Account('jane')
        account2.save_to_db()

        vouch_logic.make_request(account1, account1, account2)
        vouch_logic.make_request(account2, account1, account2)
        vouch = Vouch.find_by_ids(account1.id, account2.id)
        self.assertIsNotNone(vouch)
        self.assertRaises(IMException, vouch_logic.make_request, account1, account1, account2)

        vouch_logic.make_request(account1, account2, account1)
        self.assertRaises(IMException, vouch_logic.make_request, account1, account2, account1)
        vouch = Vouch.find_by_ids(account2.id, account1.id)
        self.assertIsNone(vouch)

        vouch_logic.make_request(account2, account2, account1)
        vouch = Vouch.find_by_ids(account2.id, account1.id)
        self.assertIsNotNone(vouch)

    # "4: 0.2, 5: 0.4, 6: 0.6, 7: 0.8, 8: 1"
    def test_speed_per_vouch_nbr(self):
        self.assertEqual(vouch_logic.speed_per_vouch_nbr(0), 0)
        self.assertEqual(vouch_logic.speed_per_vouch_nbr(1), 0)
        self.assertEqual(vouch_logic.speed_per_vouch_nbr(2), 0)
        self.assertEqual(vouch_logic.speed_per_vouch_nbr(3), 0)
        self.assertEqual(vouch_logic.speed_per_vouch_nbr(4), 0.2)
        self.assertEqual(vouch_logic.speed_per_vouch_nbr(5), 0.4)
        self.assertEqual(vouch_logic.speed_per_vouch_nbr(6), 0.6)
        self.assertEqual(vouch_logic.speed_per_vouch_nbr(7), 0.8)
        self.assertEqual(vouch_logic.speed_per_vouch_nbr(8), 1)
        self.assertEqual(vouch_logic.speed_per_vouch_nbr(9), 1)
        self.assertEqual(vouch_logic.speed_per_vouch_nbr(10), 1)

if __name__ == '__main__':
    unittest.main()