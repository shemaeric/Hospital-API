import jwt
import os
import datetime
from flask import json, Response, request, g
from functools import wraps
from ..models.UserModel import UserModel

class Auth():

	@staticmethod
	def generate_token():

		try:

			payload = {

			    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
			    'iat': datetime.datetime.utcnow(),
			    'sub': user_id
			}

			return jwt.encode(
				payload,
				app.config.get('SECRETE_KEY'),
				algorithm='HS256'
			)

		except Exception as e:
			return e
	@staticmethod
	def decode_auth():
		"""
		Decode token methode
		"""
		re = {'data': {}, 'error': {}}
		try:
			payload = jwt.decode(token, os.getenv('JWT_SECRETE_KEY'))
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
			return func(*args, **kwargs)
		return decorated_auth

