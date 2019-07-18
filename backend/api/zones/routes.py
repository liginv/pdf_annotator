from api.zones.models import Zone
from flask import request, Response, jsonify
from api import app, db, bcrypt
from api.zones.schema import zone_schema, zones_schema

@app.route('/zone')
def zone_all():
	zones = zones_schema.dump(Zone.query.all())
	return jsonify(zones.data)

@app.route('/zone/create', methods=['POST'])
def zone_create():
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

	output = []
	for zone_obj in zones:
		zone = Zone(zone_obj['zname'],zone_obj['left'],zone_obj['top'],zone_obj['width'],zone_obj['height'],zone_obj['pageOffset_left'],zone_obj['pageOffset_top'],zone_obj['pageno'],zone_obj['canvas_width'],zone_obj['canvas_height'])
		zone.pid = request.json['pid']
		db.session.add(zone)
		db.session.commit()
		output.append(zone)
	
	result = zones_schema.dump(output)

	res.response = {
		'status': 200
	}
	return jsonify(result.data)

@app.route('/zone/update', methods=['PUT'])
def zone_update():
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

@app.route('/zone/delete', methods=['DELETE'])
def zone_delete():
	zids = request.json['zids']
	output = []
	
	for zid in zids:
		zone = Zone.query.get(zid)
		db.session.delete(zone)
		db.session.commit()
		output.append(zone)
	result = zones_schema.dump(output)

	return  jsonify(result.data)