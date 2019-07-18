from api import app, db, bcrypt
from api.pdf.models import Pdf
from api.pdf.schema import pdf_schema, pdfs_schema
from api.pdf.utils import gen_pdf
from flask import request, jsonify
from api.auth.decorators import logged

@app.route('/pdf')
@logged
def pdf_all():
	pdfs = pdfs_schema.dump(Pdf.query.all())
	return jsonify(pdfs.data)

@app.route('/pdf/<int:pdf_id>')
@logged
def pdf_get_pdf(pdf_id):
	pdf = Pdf.query.get(pdf_id)
	zones = pdf.zones
	output = {}
	output["pid"] = pdf.pid
	output["pname"] = pdf.pname

	zoneArr = []
	for zone in  zones:
		zoneObj = {}
		zoneObj["zid"] = zone.zid
		zoneObj["zname"] = zone.zname
		zoneObj["left"] = zone.left
		zoneObj["top"] = zone.top
		zoneObj["width"] = zone.width
		zoneObj["height"] = zone.height
		zoneObj["pageOffset_left"] = zone.pageOffset_left
		zoneObj["pageOffset_top"] = zone.pageOffset_top
		zoneObj["pageno"] = zone.pageno
		zoneObj["canvas_width"] = zone.canvas_width
		zoneObj["canvas_height"] = zone.canvas_height
		zoneArr.append(zoneObj)

	output["zones"] = zoneArr
	return jsonify(output)

@app.route('/pdf/create', methods=['POST'])
@logged
def pdf_create():
	pfile = request.files['pfile']
	#create a pdf instance by passing respective data
	pdf = Pdf(pfile.filename,pfile.read())
	#save to database
	db.session.add(pdf)
	db.session.commit()
	return pdf_schema.jsonify(pdf)

@app.route('/pdf/fill/<int:pid>')
@logged
def pdf_fill(pid):
	return gen_pdf(pid)