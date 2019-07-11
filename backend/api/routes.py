from api.models import Pdf, Zone
from flask import request, Response, jsonify, render_template
from api import app, db
from api.schema import zone_schema, pdf_schema, zones_schema
import json

@app.route('/', methods=['GET'])
def home():
	return render_template('index.html')

@app.route('/post_pdf', methods=['POST'])
def post_pdf():

	print("\n\n")
	print(request.files)
	print("\n\n")

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
		zone.left = zone_obj.get('left')
		zone.top = zone_obj.get('top')
		zone.width = zone_obj.get('width')
		zone.heigth = zone_obj.get('height')
		zone.pageOffset_left = zone_obj.get('pageOffset_left')
		zone.pageOffset_top = zone_obj.get('pageOffset_top')
		zone.pageno = zone_obj.get('pageno')
		zone.canvas_width = zone_obj.get('canvas_width')
		zone.canvas_height = zone_obj.get('canvas_height')
		db.session.commit()
		output.append(zone)
	result = zones_schema.dump(output)
	return jsonify(result.data)

@app.route('/post_zones', methods=['POST'])
def post_zones():
	print(request.get_json())
	res = Response()
	res.headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/json',
		'Access-Control-Allow-Headers': 'Content-Type',
		'Access-Control-Allow-Methods': 'POST, OPTIONS',
		'Access-Control-Allow-Origin': '*'
	}
	#resp = Response()
	#resp.headers['Access-Control-Allow-Origin'] = '*'
	#response.headers.add('Access-Control-Allow-Origin', '*')
	zones = request.json['zones']
	print(zones)
	output = []
	for zone_obj in zones:
		zone = Zone(zone_obj['zname'],zone_obj['left'],zone_obj['top'],zone_obj['width'],zone_obj['height'],zone_obj['pageOffset_left'],zone_obj['pageOffset_top'],zone_obj['pageno'],zone_obj['canvas_width'],zone_obj['canvas_height'])
		zone.pid = request.json['pid']
		db.session.add(zone)
		db.session.commit()
		output.append(zone)
	result = zones_schema.dump(output)
	jsonify(result.data)

	print(request.json)

	res.response = {
		'status': 200
	}
	return jsonify(result.data)


@app.route('/delete_zones', methods=['DELETE'])
def delete_zones():
	zids = request.json['zids']
	output = []
	print(request.json)
	for zid in zids:
		zone = Zone.query.get(zid)
		db.session.delete(zone)
		db.session.commit()
		output.append(zone)
	result = zones_schema.dump(output)
	# res.response = {
	# 	'status': 200
	# }
	return  jsonify(result.data)




