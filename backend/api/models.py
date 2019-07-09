from api import db

class Pdf(db.Model):
	pid = db.Column(db.Integer, primary_key=True)
	pname = db.Column(db.String(255), nullable=False)
	pfile = db.Column(db.LargeBinary)
	zones = db.relationship('Zone', backref='zone', lazy=True)

	def __init__(self,name,data):
		self.pname = name
		self.pfile = data

	def __repr__(self):
		return f'Pdf({self.pid},{self.pname})'

class Zone(db.Model):
	zid = db.Column(db.Integer, primary_key=True)
	zname = db.Column(db.String(50), nullable=False)
	lx = db.Column(db.Integer, nullable=False)
	ly = db.Column(db.Integer, nullable=False)
	rx = db.Column(db.Integer, nullable=False)
	ry = db.Column(db.Integer, nullable=False)
	offset = db.Column(db.Integer, nullable=False)
	pageno = db.Column(db.Integer)
	pid = db.Column(db.Integer, db.ForeignKey('pdf.pid'), nullable=False)

	def __init__(self,name,lx,ly,rx,ry):
		self.zname = name
		self.lx = lx
		self.ly = ly
		self.rx = rx
		self.ry = ry

	def __repr__(self):
		return f'Zone({self.zname},{self.lx},{self.ly},{self.rx},{self.ry})'