import os
from flask import Flask
from config import app_config
from StackOverflow.models import db, bcrypt
from StackOverflow.Views.UserView import user_api as user_blueprint
from .Views.Patient_info_view import patient_info_api as patient_info_blueprint

def create_app(env_name):
	
	app = Flask(__name__)
	env_name = os.getenv('FLASK_ENV', 'default')
	print("jklllll",env_name)

	app.config.from_object(app_config[env_name])
	bcrypt.init_app(app)

	db.init_app(app)
	app.register_blueprint(user_blueprint, url_prefix = '/api/v1/users')
	app.register_blueprint(patient_info_blueprint, url_prefix = '/api/v1/patient_info')

	@app.route('/', methods=['GET'])

	def index():
		return 'Congratulation! Your first endpoint is working'

	return app