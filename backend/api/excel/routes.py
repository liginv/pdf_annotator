from api.pdf.models import Pdf
from flask import request, jsonify, render_template
from api import app, db
from api.auth.decorators import logged
from api.pdf.decorators import belongs_to

@app.route('/upload', endpoint = 'excel_upload')
@logged
def excel_upload():
	return render_template('excel_uploader.html')

@app.route('/upload/create', methods=['POST'], endpoint = 'excel_create')
@logged
@belongs_to
def excel_create():
	efile = request.files['excel']
	ename = efile.filename
	pid = request.form['pid']
	#attatch the excel to the Pdf
	pdf = Pdf.query.get(pid)
	if pdf:
		pdf.efile = efile.read()
		pdf.ename = ename
		db.session.commit()
	else:
		return jsonify({
			'error': 'invalid request',
			'reason': 'requested resource does not belongs to the current user'
		}), 400
	
	return jsonify({
		'success': 'file uploaded successfully'
	}), 200