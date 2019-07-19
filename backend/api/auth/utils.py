from api.auth.models import User
from datetime import datetime as dd
from api import bcrypt

def validate_email(email_):
    email = email_.strip().split('@')
    if len(email) > 1:
        has_period = len(email[-1].strip().split('.')) > 1
        if has_period:
            #check if exists
            email = ''.join(email)
            user = User.query.filter_by(email = email).first()
            if user:
                return False, 'email not available'
            return True, 'valid email', email
    return False, 'invalid email'

def validate_username(username_):
    username = username_.strip()
    if len(username) > 4 and len(username.split()) == 1:
        #check if exists
        user = User.query.filter_by(username = username).first()
        if user:
            return False, 'username not available'
        return True, 'valid username', username
    else:
        return False, 'username should be atleast 5 characters long and cannot contain white space'

def validate_password(password_):
    password = password_.strip()
    if len(password) >= 8:
        return True, 'valid password', bcrypt.generate_password_hash(password).decode()
    return False, 'password should be atleast 8 characters long'

def gen_key():
    time = dd.now().strftime('%s')
    hashed = bcrypt.generate_password_hash(time).decode()
    return hashed