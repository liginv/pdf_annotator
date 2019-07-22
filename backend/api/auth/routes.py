from api.auth.models import User
from api.status_codes import status_codes
from api import bcrypt, app, db
from flask import jsonify, request
from api.auth.decorators import logged
from api.auth.utils import (
    validate_email,
    validate_password,
    validate_username,
    gen_key
)
from flask_cors import cross_origin

@app.route('/auth/register', methods = ['POST'])
@cross_origin(supports_credentials=True)
def auth_register():
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

@app.route('/auth/login', methods = ['POST'])
@cross_origin(supports_credentials=True)
def auth_login():
    #response object
    resp = {}
    status = status_codes['SUCCESS']
    
    try:
        username = request.json['username']
        password = request.json['password']

        #check credentials
        user = User.query.filter_by(username = username).first()
        if user:
            is_pass_valid = bcrypt.check_password_hash(user.password, password)
            if is_pass_valid:
                resp['id'] = user.id
                #no api key attatched
                if not user.key:
                    user.key = gen_key()
                    db.session.commit()
                resp['key'] = user.key
            else:
                resp['error'] = 'login failed'
                resp['reason'] = 'invalid username or password'
        else:
            resp['error'] = 'login failed'
            resp['reason'] = 'invalid username or password'
    
    except KeyError:
        resp['error'] = 'login falied'
        resp['reason'] = 'username and password field required'
        status = status_codes['BAD_REQUEST']

    return jsonify(resp), status