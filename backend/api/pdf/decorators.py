from api.auth.models import User
from api.pdf.models import Pdf
from api.status_codes import status_codes
from flask import request, jsonify

def belongs_to(func):
    def check_belongs_to_current_user(*args, **kwargs):
        #get key if available
        if request.json:
            key = str(request.json['key'])
        elif request.form:
            key = str(request.form['key'])
        elif request.args:
            key = str(request.args.get('key'))
        #fetch user
        user = User.query.filter_by(key = key).first()
        #fetch requested pdf
        pdf = Pdf.query.filter_by(pid = kwargs.get('pid')).first()
        if pdf and pdf.uid == user.id:
            #resource belongs to the requested user
            return func(*args, **kwargs)
        else:
            #invalid request
            return jsonify({
                'error': 'invalid request',
                'reason': 'requested resource does not belongs to the current user'
            }), status_codes['BAD_REQUEST']

    return check_belongs_to_current_user