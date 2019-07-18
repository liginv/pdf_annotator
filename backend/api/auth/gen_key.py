from datetime import datetime as dd
from api import bcrypt

def gen_key():
    time = dd.now().strftime('%s')
    hashed = bcrypt.generate_password_hash(time)
    return hashed