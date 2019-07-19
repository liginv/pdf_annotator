from api.auth.models import User
from api.pdf.models import Pdf
from api.status_codes import status_codes
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
                    'error': 'auth failed',
                    'reason': 'invalid api key'
                }), status_codes['BAD_REQUEST']
            #user valid
            kwargs['uid'] = user.id

        except KeyError:
            return jsonify({
                'error': 'auth failed',
                'reason': 'api key required'
            }), status_codes['BAD_REQUEST']
        else:
            return func(*args, **kwargs)
    return check_api_key