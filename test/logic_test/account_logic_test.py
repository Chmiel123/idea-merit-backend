import unittest

from test.db_base_test_case import DBBaseTestCase
from model.profile.account import Account

class UserLogicTest(DBBaseTestCase):
    def test_save_to_db_and_find(self):
        account = Account()
        account.name = "john"
        account.save_to_db()
        found_account = Account.find_by_username("john")
        self.assertEqual(account, found_account)

    def test_save_to_db_and_find_with_domain(self):
        account = Account()
        account.name = "john"
        account.domain = "john.com"
        account.save_to_db()
        found_account = Account.find_by_username("john", "john.com")
        self.assertEqual(account, found_account)

if __name__ == '__main__':
    unittest.main()