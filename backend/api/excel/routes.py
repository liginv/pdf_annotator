from api.pdf.models import Pdf
from flask import request, jsonify
from api import app, db
from api.auth.decorators import logged
from flask_cors import cross_origin

# @app.route('/upload', endpoint = 'excel_upload')
# @cross_origin(supports_credentials=True)
# @logged
# def excel_upload():
	

@app.route('/upload/create', methods=['POST'], endpoint = 'excel_create')
@cross_origin(supports_credentials=True)
@logged
def excel_create(*args, **kwargs):
	efile = request.files['excel']
	ename = efile.filename
	pid = request.form['pid']
	#attatch the excel to the Pdf
	pdf = Pdf.query.get(pid)
	if pdf and pdf.uid == kwargs.get('uid'):
		pdf.efile = efile.read()
		pdf.ename = ename
		db.session.commit()
	else:
		return jsonify({
			'error': 'Invalid request',
			'reason': 'Requested resource does not belongs to the current user'
		}), 400
	
	return jsonify({
		'success': 'File uploaded successfully'
	}), 200
