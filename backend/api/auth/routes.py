from api.auth.models import User
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
    status = 200
    
    try:
        username = validate_username(request.json['username'])
        password = validate_password(request.json['password'])
        email = validate_email(request.json['email'])
        
        if username[0] and password[0] and email[0]:
            user = User(email[2], username[2], password[2])
            db.session.add(user)
            db.session.commit()
            resp['success'] = 'Account created successfully'

        else:
            resp['error'] = 'Registeration failed'
            resp['reason'] = {
                'username': username[1],
                'password': password[1],
                'email': email[1]
            }
            status = 400

    except KeyError:
        resp['error'] = 'Registeration failed'
        resp['reason'] = 'username, password and email required'
        status = 400

    return jsonify(resp), status

@app.route('/auth/login', methods = ['POST'])
@cross_origin(supports_credentials=True)
def auth_login():
    #response object
    resp = {}
    status = 200
    
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
                resp['error'] = 'Login failed'
                resp['reason'] = 'Invalid username or password'
                status = 400
        else:
            resp['error'] = 'Login failed'
            resp['reason'] = 'Invalid username or password'
            status = 400
    
    except KeyError:
        resp['error'] = 'Login falied'
        resp['reason'] = 'sername and password field required'
        status = 400

    return jsonify(resp), status