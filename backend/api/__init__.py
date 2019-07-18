from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow

#app config
app = Flask(__name__,static_url_path="",static_folder="static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors = CORS(app, resources={r"*": {"origins": "*"}})
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
ma = Marshmallow(app)

#routes import
from api import routes
from api.excel import routes
from api.auth import routes
from api.pdf import routes
from api.zones import routes