from api.auth.models import User
from api.status_codes import status_codes
from flask import request, jsonify

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