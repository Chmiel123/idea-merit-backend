import string
import random
import datetime
from util.exception import IMException
from model.profile.email_verification import EmailVerification
from model.profile.account_email import AccountEmail
from config.config import config

def generate_verification(account_email: AccountEmail) -> EmailVerification:
    if account_email.verified:
        raise IMException('Account already verified')
    EmailVerification.delete_by_email(account_email.email)
    
    ev = EmailVerification(account_email.email)
    ev.save_to_db()
    return ev

def set_primary(account_email: AccountEmail) -> None:
    # get all emails for account and set to non primary
    for ae in account_email.account.emails:
        if ae.primary:
            ae.primary = False
            ae.save_to_db()
    # set to primary
    account_email.primary = True
    account_email.save_to_db()

def verify(verification_key: str) -> bool:
    found_ev = EmailVerification.find_by_verify_key(verification_key)
    if found_ev:
        found_account_email = AccountEmail.find_by_email(found_ev.email)
        max_hours = config['email']['email_verification_hours']
        if found_ev.verification_key == verification_key:
            if found_ev.created_date + datetime.timedelta(hours=max_hours) > datetime.datetime.utcnow():
                found_account_email.verified = True
                EmailVerification.delete_by_email(found_ev.email)
                return True
            else:
                raise IMException('Verification expired')
        else:
            raise IMException('Invalid verification key')
    else:
        raise IMException('Email could not be verified')
    return False

