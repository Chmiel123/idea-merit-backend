
from util.exception import IMException
from model.profile.account import Account
from model.profile.login_direct import LoginDirect

def create_account_with_password(username: str, password: str):
    #split domain if exists
    ats = [i for i, ltr in enumerate(username) if ltr == '@']
    if len(ats) > 0:
        raise IMException('Invalid username format: one or more @ symbols')

    #The rest
    if Account.find_by_username(username):
        raise IMException(f'User {username} already exists')

    new_account = Account(username)
    new_account.save_to_db()
    new_login_direct = LoginDirect(account = new_account, password = LoginDirect.generate_hash(password))
    new_login_direct.save_to_db()

    return new_account, new_login_direct

def login(username: str, password: str) -> Account:
    current_account = Account.find_by_username(username)

    if not current_account:
        raise IMException(f'User {username} doesn\'t exist')
    
    if LoginDirect.verify_hash(password, current_account.login_direct.password):
        return current_account
    else:
        raise IMException('Wrong credentials')