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
	resp = Response()
	resp.headers['Access-Control-Allow-Origin'] = '*'
	#if request.method == 'OPTIONS':
	resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
	resp.status_code = 204
	#	return resp

	print("\n\n")
	print(request.form)
	print(request.files)
	print("\n\n")
	#response.headers.add('Access-Control-Allow-Origin', '*')
	pfile = request.form['pfile']
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
	pid=0
	for zone_obj in zones:
		pid=pid+1
		zone = Zone(zone_obj['cordinates']['zname'],zone_obj['cordinates']['lx'],zone_obj['cordinates']['ly'],zone_obj['cordinates']['rx'],zone_obj['cordinates']['ry'])
		zone.pid = pid
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
	zones = request.json['zones']
	output = []
	for zone_obj in zones:
		zone = Zone.query.get(zone_obj.get('zid'))
		db.session.delete(zone)
		db.session.commit()
		output.append(zone)
	result = zones_schema.dump(output)
	return jsonify(result.data)




