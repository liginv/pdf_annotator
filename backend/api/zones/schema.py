from api import app, ma

class ZoneSchema(ma.Schema):
    class Meta:
        fields = ('zid','zname','left','top','width','height','pageOffset_left','pageOffset_top','pageno','canvas_width','canvas_height')

zone_schema = ZoneSchema(strict=True)
zones_schema = ZoneSchema(many=True,strict=True)