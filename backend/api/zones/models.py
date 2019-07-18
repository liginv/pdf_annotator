from api import db

class Zone(db.Model):
	zid = db.Column(db.Integer, primary_key=True)
	zdata = db.Column(db.String(500), nullable=True)
	zname = db.Column(db.String(50), nullable=False)
	left = db.Column(db.Integer, nullable=False)
	top = db.Column(db.Integer, nullable=False)
	width = db.Column(db.Integer, nullable=False)
	height = db.Column(db.Integer, nullable=False)
	pageOffset_left = db.Column(db.Integer, nullable=False)
	pageOffset_top = db.Column(db.Integer, nullable=False)
	pageno = db.Column(db.Integer, nullable=True)
	canvas_width = db.Column(db.Integer, nullable=True)
	canvas_height = db.Column(db.Integer, nullable=True)
	pid = db.Column(db.Integer, db.ForeignKey('pdf.pid'), nullable=False)

	def __init__(self,name,left,top,width,height,offset_left,offset_top,pageno,canvas_width,canvas_height):
		self.zname = name
		self.left = left
		self.top = top
		self.width = width
		self.height = height
		self.pageOffset_left = offset_left
		self.pageOffset_top = offset_top
		self.pageno = pageno
		self.canvas_width = canvas_width
		self.canvas_height = canvas_height

	def __repr__(self):
		return f'Zone({self.zname},{self.left},{self.top},{self.width},{self.height})'