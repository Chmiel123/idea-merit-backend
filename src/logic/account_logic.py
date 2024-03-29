import uuid
import datetime
from util.exception import IMException
from model.profile.account import Account
from model.profile.account_password import AccountPassword
from model.profile.account_email import AccountEmail
from model.profile.password_reset import PasswordReset
from config.config import config

def get_by_id(id: uuid) -> Account:
    return Account.find_by_id(id)

def get_by_username(name: str) -> Account:
    return Account.find_by_username(name)

def create_account_with_password(username: str, password: str):
    #split domain if exists
    ats = [i for i, ltr in enumerate(username) if ltr == '@']
    if len(ats) > 0:
        raise IMException('Invalid username format: one or more @ symbols')

    #The rest
    if Account.find_by_username(username):
        raise IMException(f'User {username} already exists')

    new_account = Account(username)
    new_account.virtual_resource_accrued = config['vote']['gift_resource_to_new_accounts']
    new_account.save_to_db()
    new_account_password = AccountPassword(new_account.id, password)
    new_account_password.save_to_db()

    return new_account, new_account_password

def login(username_or_email: str, password: str) -> Account:
    current_account = Account.find_by_username(username_or_email)

    if current_account:
        if AccountPassword.verify_hash(password, current_account.account_password.password):
            return current_account
    
    current_email = AccountEmail.find_by_email(username_or_email)
    if current_email:
        current_account = Account.find_by_id(current_email.account_id)
        if current_account:
            if AccountPassword.verify_hash(password, current_account.account_password.password):
                return current_account
    
    else:
        raise IMException('Wrong credentials.')

def generate_password_reset(email: str):
    found_email_account = AccountEmail.find_by_email(email)
    if not found_email_account:
        raise IMException('Email not found')
    
    PasswordReset.delete_by_account_id(found_email_account.account_id)
    pr = PasswordReset(found_email_account.account_id)
    pr.save_to_db()
    #TODO: send email with verification key

def verify_password_reset(verification_key: str, new_password: str):
    found_pr = PasswordReset.find_by_verify_key(verification_key)
    if not found_pr:
        raise IMException('Invalid verification key')
    max_hours = config['limit']['password_reset_hours']
    if found_pr.created_date + datetime.timedelta(hours=max_hours) > datetime.datetime.utcnow():
        #create
        AccountPassword.delete_by_account_id(found_pr.account_id)
        new_account_password = AccountPassword(found_pr.account_id, new_password)
        new_account_password.save_to_db()
        return 'Password reset succesfully'
    else:
        raise IMException('Password reset expired')