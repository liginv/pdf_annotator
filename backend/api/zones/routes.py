from api.zones.models import Zone
from api.pdf.models import Pdf
from flask import request, Response, jsonify
from api import app, db, bcrypt
from api.zones.schema import zone_schema, zones_schema
from api.auth.decorators import logged


@app.route('/zone/create', methods=['POST'], endpoint = 'zone_create')
@logged
def zone_create(*args, **kwargs):
	#handles XSRF
	res = Response()
	res.headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/json',
		'Access-Control-Allow-Headers': 'Content-Type',
		'Access-Control-Allow-Methods': 'POST, OPTIONS',
		'Access-Control-Allow-Origin': '*'
	}

	try:
		#validate request
		pid = request.json['pid']
		pdf = Pdf.query.get(pid)
		if not pdf:
			raise AssertionError
		assert(pdf.uid == kwargs.get('uid'))
		zones = request.json['zones']
		output = []
		
		for zone_obj in zones:
			#create zone instance
			zone = Zone(
				zone_obj['zname'],
				zone_obj['left'],
				zone_obj['top'],
				zone_obj['width'],
				zone_obj['height'],
				zone_obj['pageOffset_left'],
				zone_obj['pageOffset_top'],
				zone_obj['pageno'],
				zone_obj['canvas_width'],
				zone_obj['canvas_height']
			)
			zone.pid = pid
			#save
			db.session.add(zone)
			db.session.commit()
			output.append(zone)
		
		result = zones_schema.dump(output)
		res.response = {
			'success': 'zone created'
		}
		return jsonify(result.data), 200
	
	except AssertionError:
		return jsonify({
			'error': 'invalid request',
			'reason': 'requested resource does not belongs to current user'
		})

@app.route('/zone/update', methods=['PUT'], endpoint = 'zone_update')
@logged
def zone_update(*args, **kwargs):
	zones = request.json['zones']
	#check request
	try:
		for zone_obj in zones:
			zid = zone_obj.get('zid')
			zone = Zone.query.get(zid)
			if not zone:
				raise AssertionError
			pdf = Pdf.query.get(zone.pid)
			assert(pdf.uid == kwargs.get('uid'))
	except AssertionError:
		return jsonify({
			'error': 'invalid request',
			'reason': 'request contains resource which does not belongs to current user'
		})
	#valid request
	output = []
	for zone_obj in zones:
		zid = zone_obj.get('zid')
		zone = Zone.query.get(zid)
		
		#update zone using new values
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
		
		#save update
		db.session.commit()
		output.append(zone)

	result = zones_schema.dump(output)
	return jsonify(result.data)

@app.route('/zone/delete', methods=['DELETE'], endpoint = 'zone_delete')
@logged
def zone_delete(*args, **kwargs):
	zids = request.json['zids']
	#check request
	try:
		for zid in zids:
			zone = Zone.query.get(zid)
			if not zone:
				raise AssertionError
			pdf = Pdf.query.get(zone.pid)
			assert(pdf.uid == kwargs.get('uid'))
	except AssertionError:
		return jsonify({
			'error': 'invalid request',
			'reason': 'request contains resource which does not belongs to current user'
		})
	#valid request
	output = []
	for zid in zids:
		zone = Zone.query.get(zid)
		#delete and save
		db.session.delete(zone)
		db.session.commit()
		output.append(zone)

	result = zones_schema.dump(output)
	return  jsonify(result.data)