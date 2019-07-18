from api import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255), unique = True, nullable = False)
    username = db.Column(db.String(255), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    key = db.Column(db.String(255), unique = True, nullable = True)
    is_active = db.Column(db.Boolean, default = False)

    def __init__(self,e,u,p):
        self.username = u
        self.password = p
        self.email = e

    def __repr__(self):
        return f'User({self.id}, {self.username})'