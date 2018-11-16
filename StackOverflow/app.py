from flask import Flask
from config import app_config
from StackOverflow.models import db, bcrypt

def create_app(env_name):
	
	app = Flask(__name__)

	# app.config.from_object(app_config[env_name])
	bcrypt.init_app(app)

	db.init_app(app)
	# app.register_blueprint(user_blueprint, url_prefix = '/api/v1/users')

	@app.route('/', methods=['GET'])

	def index():
		return 'Congratulation! Your first endpoint is working'

	return app