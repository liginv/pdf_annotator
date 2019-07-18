from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from  flask_bcrypt import Bcrypt

app = Flask(__name__,static_url_path="",static_folder="static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors = CORS(app, resources={r"*": {"origins": "*"}})
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from api import routes