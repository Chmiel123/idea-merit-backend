import unittest

from test.db_base_test_case import DBBaseTestCase
from model.profile.account import Account
from model.profile.account_email import AccountEmail
from model.profile.email_verification import EmailVerification

class EmailModelTest(DBBaseTestCase):
    def test_email_and_email_verification(self):
        account = Account()
        account.name = "john"
        account.save_to_db()
        account_email = AccountEmail(
            account = account,
            email = "john@smith.com"
        )
        account_email.save_to_db()
        ev = EmailVerification.generate_verification(account_email)
        found_account = Account.find_by_username("john")
        found_ev = EmailVerification.find_by_email(found_account.emails[0].email)
        verified = EmailVerification.verify(found_account.emails[0].email, found_ev.verification)

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
        EmailVerification.generate_verification(account_email)
        EmailVerification.generate_verification(account_email)
        EmailVerification.generate_verification(account_email)
        ev = EmailVerification.generate_verification(account_email)
        found_account = Account.find_by_username("john")
        found_ev = EmailVerification.find_by_email(found_account.emails[0].email)
        verified = EmailVerification.verify(found_account.emails[0].email, found_ev.verification)

        nbr_found_ev = len(self.db.session.query(EmailVerification).filter_by(email = account_email.email).all())

        self.assertEqual(nbr_found_ev, 1)
        self.assertEqual(found_account.emails[0], account_email)
        self.assertEqual(found_ev, ev)
        self.assertEqual(verified, True)


if __name__ == '__main__':
    unittest.main()