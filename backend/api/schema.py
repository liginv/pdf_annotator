from api import app
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)

class ZoneSchema(ma.Schema):
	class Meta:
		fields = ('zid','zname','lx','ly','rx','ry')

class PdfSchema(ma.Schema):
	class Meta:
		fields = ('pid','pname')

zone_schema = ZoneSchema(strict=True)
zones_schema = ZoneSchema(many=True,strict=True)
pdf_schema = PdfSchema(strict=True)