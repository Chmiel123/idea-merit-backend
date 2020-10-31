import unittest

from test.db_base_test_case import DBBaseTestCase
from logic import account_logic
from model.profile.account import Account
from model.profile.account_email import AccountEmail
from model.profile.password_reset import PasswordReset

class AccountLogicTest(DBBaseTestCase):
    def test_save_to_db_and_find(self):
        account = Account('john')
        account.save_to_db()
        found_account = Account.find_by_username('john')
        self.assertEqual(account, found_account)

    def test_password_reset(self):
        account_logic.create_account_with_password('john', 'pass')
        found_account = Account.find_by_username('john')
        self.assertIsNotNone(found_account.login_direct)
        self.assertEqual(found_account.name, 'john')
        account = account_logic.login('john', 'pass')
        self.assertIsNotNone(found_account.login_direct)
        self.assertEqual(account, found_account)
        account_email = AccountEmail(
            account = account,
            email = 'john@smith.com'
        )
        account_email.save_to_db()

        account_logic.generate_password_reset(account_email.email)
        pr = PasswordReset.find_by_account_id(found_account.id)
        account_logic.verify_password_reset(pr.verification_key, 'pass2')

        account = account_logic.login('john', 'pass2')
        self.assertIsNotNone(found_account.login_direct)
        self.assertEqual(account, found_account)



if __name__ == '__main__':
    unittest.main()