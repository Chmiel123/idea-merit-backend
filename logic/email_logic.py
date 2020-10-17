import string
import random
import datetime
from util.exception import IMException
from model.profile.email_verification import EmailVerification
from model.profile.account_email import AccountEmail
from config.config import config


def generate_verification(email: str) -> EmailVerification:
    EmailVerification.delete_by_email(email)
    
    random_string = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(20))
    ev = EmailVerification(
        email=email,
        verification_key = random_string
    )
    ev.save_to_db()
    return ev
        
def verify(verification_key: str) -> bool:
    found_ev = EmailVerification.find_by_verify_key(verification_key)
    if found_ev:
        found_account_email = AccountEmail.find_by_email(found_ev.email)
        max_hours = config['email']['email_verification_hours']
        if found_ev.verification_key == verification_key and found_ev.created_date + datetime.timedelta(hours=max_hours) > datetime.datetime.utcnow():
            found_account_email.verified = True
            EmailVerification.delete_by_email(found_ev.email)
            return True
        else:
            return False
    return False
