import unittest

from test.db_base_test_case import DBBaseTestCase
from model.profile.account import Account
from model.profile.account_email import AccountEmail
from model.profile.email_verification import EmailVerification
from logic import email_logic

class EmailLogicTest(DBBaseTestCase):
    def test_email_and_email_verification(self):
        account = Account()
        account.name = "john"
        account.save_to_db()
        account_email = AccountEmail(
            account = account,
            email = "john@smith.com"
        )
        account_email.save_to_db()
        ev = email_logic.generate_verification(account_email)
        found_account = Account.find_by_username("john")
        found_ev = EmailVerification.find_by_email(found_account.emails[0].email)
        verified = email_logic.verify(found_ev.verification_key)

        self.assertEqual(found_account.emails[0], account_email)
        self.assertEqual(found_ev, ev)
        self.assertEqual(verified, True)
        
    def test_multiple_email_verification(self):
        account = Account(
            name = "john"
        )
        account.save_to_db()
        account_email = AccountEmail(
            account = account,
            email = "john@smith.com"
        )
        account_email.save_to_db()
        email_logic.generate_verification(account_email)
        email_logic.generate_verification(account_email)
        email_logic.generate_verification(account_email)
        ev = email_logic.generate_verification(account_email)
        found_account = Account.find_by_username("john")
        found_ev = EmailVerification.find_by_email(found_account.emails[0].email)

        nbr_found_ev = len(self.db.session.query(EmailVerification).filter_by(email = account_email.email).all())
        self.assertEqual(nbr_found_ev, 1)

        verified = email_logic.verify(found_ev.verification_key)

        nbr_found_ev = len(self.db.session.query(EmailVerification).filter_by(email = account_email.email).all())
        self.assertEqual(nbr_found_ev, 0)

        self.assertEqual(found_account.emails[0], account_email)
        self.assertEqual(found_ev, ev)
        self.assertEqual(verified, True)

    def test_email_primary(self):
        account = Account(name = "john")
        account.save_to_db()
        account_email1 = AccountEmail(
            account = account,
            email = "john@smith.com"
        )
        account_email1.save_to_db()
        account_email2 = AccountEmail(
            account = account,
            email = "john@smith.net"
        )
        account_email2.save_to_db()
        account_email3 = AccountEmail(
            account = account,
            email = "john@smith.eu"
        )
        account_email3.save_to_db()
        email_logic.set_primary(AccountEmail.find_by_email("john@smith.com"))
        self.assertTrue(AccountEmail.find_by_email("john@smith.com").primary)
        self.assertFalse(AccountEmail.find_by_email("john@smith.net").primary)
        self.assertFalse(AccountEmail.find_by_email("john@smith.eu").primary)
        email_logic.set_primary(AccountEmail.find_by_email("john@smith.net"))
        self.assertFalse(AccountEmail.find_by_email("john@smith.com").primary)
        self.assertTrue(AccountEmail.find_by_email("john@smith.net").primary)
        self.assertFalse(AccountEmail.find_by_email("john@smith.eu").primary)
        email_logic.set_primary(AccountEmail.find_by_email("john@smith.eu"))
        self.assertFalse(AccountEmail.find_by_email("john@smith.com").primary)
        self.assertFalse(AccountEmail.find_by_email("john@smith.net").primary)
        self.assertTrue(AccountEmail.find_by_email("john@smith.eu").primary)

if __name__ == '__main__':
    unittest.main()