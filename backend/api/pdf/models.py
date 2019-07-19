from api import db

class Pdf(db.Model):
	pid = db.Column(db.Integer, primary_key=True)
	pname = db.Column(db.String(255), nullable=False)
	pfile = db.Column(db.LargeBinary)
	zones = db.relationship('Zone', backref='zone', lazy=True)
	efile = db.Column(db.LargeBinary, nullable=True)
	ename = db.Column(db.String(255), nullable=True)
	uid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

	def __init__(self,name,data):
		self.pname = name
		self.pfile = data

	def __repr__(self):
		return f'Pdf({self.pid},{self.pname})'