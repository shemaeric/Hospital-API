import jwt
import os
import datetime
from flask import json, Response, request, g, make_response
from functools import wraps
from werkzeug.security import safe_str_cmp
from ..models.UserModel import UserModel, UserSchema
from ..models.PatientsModel import PatientModel,PatientSchema

user_schema = UserSchema()
JWT_SECRET_KEY = 'secret'
JWT_ALGORITHM = 'HS256'

class Auth():

	@staticmethod
	def generate_token(user_id):
		payload = {
				'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
				'sub': user_id
		}
		token = jwt.encode(payload, JWT_SECRET_KEY, 'HS256')
		return json.dumps({'token': token.decode('utf-8')})
	@staticmethod
	def decode_token(token):
		"""
		Decode token method
		"""
		re = {'data': {}, 'error': {}}
		try:
			payload = jwt.decode(token, JWT_SECRET_KEY)
			re['data'] = {'user_id': payload['sub']}
			return re
		except jwt.ExpiredSignatureError as e1:
			re['error'] = {'message': 'token expired, please login again'}
			return re
		except jwt.InvalidTokenError:
			re['error'] = {'message': 'Invalid token, please try again with a new token'}
			return re

	@staticmethod
	def auth_required(func):
		"""
		Auth Decorator
		"""

		@wraps(func)
		def decorated_auth(*args, **kwargs):
			if 'api-token' not in request.headers:
				return Response(
					mimetype="application/json",
					response=json.dumps({'error': 'Authentication token is not available, please login to get one'}),
					status=400
				)

			token = request.headers.get('api-token')
			data = Auth.decode_token(token)
			if data['error']:

				return Response(
					mimetype="application/json",
					response=json.dumps({'error': 'Authentication token is not available, please login to get one'}),
					status=400
				)

			user_id = data['data']['user_id']
			check_user = UserModel.get_one_user(user_id)
			if not check_user:
				return Response(
					mimetype = "application/json",
					response=json.dumps({'error': 'user does not exist, invalid token'}),
					status=400
				)
			g.user = {'id': user_id}
			return func(user_id,*args, **kwargs)
		return decorated_auth

