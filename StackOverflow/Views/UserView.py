from flask import request, json, Response, Blueprint, g
from ..models.UserModel import UserModel, UserSchema
from ..Auth.auth import Auth

user_api = Blueprint('user_api', __name__)
user_schema = UserSchema()

@user_api.route('/', methods= ['POST'])
def create():

	req_data = request.get_json(force=True)
	data,error = user_schema.load(req_data)

	if error:
		return custom_response(error, 400)

	user_in_db = UserModel.get_user_by_email(data.get('email'))
	if user_in_db:
		message = {'error': 'User already exist, please supply another email address'}
		return custom_response(message, 400)

	user = UserModel(data)
	user.save()

	ser_data = user_schema.dump(user).data
	token = Auth.generate_token(ser_data.get('id'))
	return custom_response({'jwt_token': token}, 201)

@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_a_user():

	user = UserModel.get_one_user(user_id)
	if not user:
		return custom_response({'error': 'user not found'}, 404)

	ser_user = user_schema.dump(user).data
	return custom_response(ser_user, 200)
	
@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():

	user = UserModel.get_one_user(g.user.get('id'))
	ser_user = user_schema.dump(user).data
	return custom_response(ser_user, 200)

def login():

	req_data = request.get_json(force = True)
	data,error = user_schema.load(req_data)

	if error:
		return custom_response(error,400)
	if not data.get('email') or not data.get('password'):
		return custom_response({'error': 'you need email and password to sign in'}, 400)

	user = UserModel.get_user_by_email(data.get('email'))
	if not user:
		return custom_response({'error': 'invalid credentials'}, 400)
	if not user.check_hash(data.get('password')):
		return custom_response({'error': 'invalid credentials'}, 400)
	ser_data = user_schema.load(user).data
	token = Auth.generate_token(ser_data.get('id'))
	return custom_response(200)

def custom_response(res, status_code):

	return Response(
		mimetype = "Application/json",
		response = json.dumbs(res),
		status = status_code
		)
