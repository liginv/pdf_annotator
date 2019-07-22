from api.auth.models import User
from api.pdf.models import Pdf
from flask import request, jsonify

def logged(func):
    def check_api_key(*args, **kwargs):
        try:
            #get key if available
            if request.json:
                key = str(request.json['key'])
            elif request.form:
                key = str(request.form['key'])
            elif request.args:
                key = str(request.args.get('key'))
            else:
                raise KeyError
            #fetch user using key
            user = User.query.filter_by(key = key).first()
            if not user:
                return jsonify({
                    'error': 'Authentication failed',
                    'reason': 'Invalid api key'
                }), 401
            #user valid
            kwargs['uid'] = user.id

        except KeyError:
            return jsonify({
                'error': 'Authentication failed',
                'reason': 'Api key required'
            }), 401
        else:
            return func(*args, **kwargs)
    return check_api_key