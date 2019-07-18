from api.auth.user import User
from api.status_codes import status_codes
from api import bcrypt, app, db
from api.auth.gen_key import gen_key
from flask import jsonify, request

@app.route('/login', methods = ['POST'])
def login():
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

def logged(func):
    def func(*args, **kwargs):
        try:
            if request.json:
                key = str(request.json['key'])
            elif request.form:
                key = str(request.form['key'])
            elif request.args:
                key = str(request.args.get('key'))
            user = User.query.filter_by(key = key).first()
            if not user:
                return jsonify({
                    'error': 'login failed',
                    'reason': 'invalid api key'
                }), status_codes['BAD_REQUEST']

        except KeyError:
            return jsonify({
                'error': 'failed',
                'reason': 'api key required'
            }), status_codes['BAD_REQUEST']
    
    return func

        