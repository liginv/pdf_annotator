from api import app, ma

class PdfSchema(ma.Schema):
	class Meta:
		fields = ('pid','pname')

pdf_schema = PdfSchema(strict=True)
pdfs_schema = PdfSchema(many=True,strict=True)