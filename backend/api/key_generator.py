from api import bcrypt
import datetime

def api_key_generator():
	return bcrypt.generate_password_hash(datetime.datetime.now().strftime('%s')).decode('utf8')