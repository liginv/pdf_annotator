from api import app
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)

class ZoneSchema(ma.Schema):
	class Meta:
		fields = ('zid','zname','left','top','width','height','pageOffset_left','pageOffset_top','pageno','canvas_width','canvas_height')

class PdfSchema(ma.Schema):
	class Meta:
		fields = ('pid','pname')

zone_schema = ZoneSchema(strict=True)
zones_schema = ZoneSchema(many=True,strict=True)
pdf_schema = PdfSchema(strict=True)
pdfs_schema = PdfSchema(many=True,strict=True)