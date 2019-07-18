from api.auth.user import User
from api.status_codes import status_codes
from api import bcrypt, app, db
from api.auth.gen_key import gen_key
from flask import jsonify, request

def validate_email(email_):
    email = str(email_).strip.split('@')
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
    username = str(username_).strip()
    if len(username) > 4 and len(username.split()) == 1:
        #check if exists
        user = User.query.filter_by(username = username).first()
        if user:
            return False, 'username not available'
        return True, 'valid username', username
    else:
        return False, 'username should be atleast 5 characters long and cannot contain white space'

def validate_password(password_):
    password = str(password_).strip()
    if len(password) >= 8:
        return True, 'valid password', password
    return False, 'password should be atleast 8 characters long'

@app.route('/register', methods = ['POST'])
def register():
    #response object
    resp = {}
    status = status_codes['SUCCESS']
    
    try:
        username = validate_username(request.json['username'])
        password = validate_password(request.json['password'])
        email = validate_email(request.json['email'])
        
        if username[0] and password[0] and email[0]:
            user = User(email[2], username[2], password[2])
            db.session.add(user)
            db.session.commit()
            resp['success'] = 'registeration successfull'

        else:
            resp['error'] = 'registeration failed'
            resp['reason'] = {
                'username': username[1],
                'password': password[1],
                'email': email[1]
            }

    except KeyError:
        resp['error'] = 'registeration failed'
        resp['reason'] = 'username, password and email required'
        status = status_codes['BAD_REQUEST']

    return jsonify(resp), status