from api import app, db, bcrypt
from api.pdf.models import Pdf
from api.pdf.schema import pdf_schema, pdfs_schema
from api.pdf.utils import gen_pdf
from flask import request, jsonify
from api.auth.decorators import logged
from api.pdf.decorators import belongs_to

@app.route('/pdf', endpoint = 'pdf_all')
@logged
def pdf_all(*args, **kwargs):
	pdfs = pdfs_schema.dump(Pdf.query.filter_by(uid = kwargs.get('uid')))
	return jsonify(pdfs.data)

@app.route('/pdf/<int:pid>', endpoint = 'pdf_get_pdf')
@logged
@belongs_to
def pdf_get_pdf(pid,*args,**kwargs):
	pdf = Pdf.query.get(pid)
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

@app.route('/pdf/create', methods=['POST'], endpoint = 'pdf_create')
@logged
def pdf_create(*args, **kwargs):
	pfile = request.files['pfile']
	#create a pdf instance by passing respective data
	pdf = Pdf(pfile.filename,pfile.read())
	pdf.uid = kwargs['uid']
	#save to database
	db.session.add(pdf)
	db.session.commit()
	return pdf_schema.jsonify(pdf)

@app.route('/pdf/fill/<int:pid>', endpoint = 'pdf_fill')
@logged
@belongs_to
def pdf_fill(pid):
	return gen_pdf(pid)