from api.models import Pdf, Zone
from flask import request, Response, jsonify, render_template
from api import app, db
from api.schema import zone_schema, pdf_schema, zones_schema, pdfs_schema
import json

@app.route('/', methods=['GET'])
def home():
	return render_template('index.html')

@app.route('/post_pdf', methods=['POST'])
def post_pdf():
	resp = Response()
	resp.headers['Access-Control-Allow-Origin'] = '*'
	resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
	resp.status_code = 204
	#response.headers.add('Access-Control-Allow-Origin', '*')
	pfile = request.files['pfile']
	#create a pdf instance by passing respective data
	pdf = Pdf(pfile.filename,pfile.read())
	#save to database
	db.session.add(pdf)
	db.session.commit()
	return pdf_schema.jsonify(pdf)

@app.route('/put_zones', methods=['PUT'])
def put_zones():
	zones = request.json['zones']
	output = []
	for zone_obj in zones:
		zone = Zone.query.get(zone_obj.get('zid'))
		zone.zname = zone_obj.get('zname')
		zone.lx = zone_obj.get('lx')
		zone.ly = zone_obj.get('ly')
		zone.rx = zone_obj.get('rx')
		zone.ry = zone_obj.get('ry')
		zone.page = zone_obj.get('page')
		zone.page_height = zone_obj.get('page_height')
		zone.page_width = zone_obj.get('page_width')
		db.session.commit()
		output.append(zone)
	result = zones_schema.dump(output)
	return jsonify(result.data)

@app.route('/post_zones', methods=['POST'])
def post_zones():
	#print(request.get_json())
	res = Response()
	res.headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/json',
		'Access-Control-Allow-Headers': 'Content-Type',
		'Access-Control-Allow-Methods': 'POST, OPTIONS',
		'Access-Control-Allow-Origin': '*'
	}

	pid = request.json['pid']
	zones = request.json['zones']

	print(pid,zones)

	output = []

	for zone_obj in zones:
		zone = Zone(zone_obj['zname'],zone_obj['lx'],zone_obj['ly'],zone_obj['rx'],zone_obj['ry'],zone_obj['page'],zone_obj['page_height'],zone_obj['page_width'])
		zone.pid = pid
		db.session.add(zone)
		db.session.commit()
		output.append(zone)
	
	result = zones_schema.dump(output)

	res.response = {
		'status': 200
	}
	return jsonify(result.data)


@app.route('/delete_zones', methods=['DELETE'])
def delete_zones():
	zones = request.json['zones']
	output = []
	for zone_obj in zones:
		zone = Zone.query.get(zone_obj.get('zid'))
		db.session.delete(zone)
		db.session.commit()
		output.append(zone)
	result = zones_schema.dump(output)
	return jsonify(result.data)

@app.route('/get_pdfs')
def get_pdfs():
	pdfs = pdfs_schema.dump(Pdf.query.all())
	return jsonify(pdfs.data)

@app.route('/get_zones')
def get_zones():
	zones = zones_schema.dump(Zone.query.all())
	return jsonify(zones.data)

@app.route('/get_pdf/<int:pdf_id>')
def get_pdf(pdf_id):
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
		zoneObj["lx"] = zone.lx
		zoneObj["ly"] = zone.ly
		zoneObj["rx"] = zone.rx
		zoneObj["ry"] = zone.ry
		zoneObj["page"] = zone.page
		zoneObj["page_height"] = zone.page_height
		zoneObj["page_width"] = zone.page_width
		zoneArr.append(zoneObj)

	output["zones"] = zoneArr
	return jsonify(output)

from .pdf_maker import *

@app.route('/gen_pdf/<int:pid>')
def gen_pdf_func(pid):
	gen_pdf(pid)
	return jsonify({
			'status': 200
		})