from flask import render_template
from api import app
from flask_cors import cross_origin

@app.route('/', methods=['GET'])
@cross_origin(supports_credentials=True)
def home():
	return render_template('index.html')