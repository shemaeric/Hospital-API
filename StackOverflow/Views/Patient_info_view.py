from flask import request, json, Response, Blueprint, g
from ..Auth.auth import Auth
from ..models.PatientsModel import PatientModel, PatientSchema


patient_info_api = Blueprint('patient_info_api', __name__)
patient_info_schema = PatientSchema()

@patient_info_api.route('/', methods = ['POST'])
def create():
	req_data = request.get_json()
	print("hjfdddd",req_data)
	data,error = patient_info_schema.load(req_data)
	if error :
		return custom_response(error, 400)
	post = PatientModel(data)
	post.save()
	data = patient_info_schema.dump(post).data
	return custom_response(data, 201)

@patient_info_api.route('/', methods = ['GET'])
def get_all():
	"""
	get all patients
	"""

	posts = PatientModel.get_all_patients_infos()
	data = patient_info_schema.dump(posts, many = True).data
	return custom_response(data, 200)

@patient_info_api.route('/me', methods = ['GET'])
def get_one(patient_id):
	"""
	get one patient infos
	"""

	post = PatientModel.get_one_patient_infos(patient_id)
	if not post:
		return custom_response({'error': 'Patient not found'}, 404)

	data = patient_info_schema.dump(post).data
	return custom_response(data, 200)

@patient_info_api.route('/<patient_id>', methods = ['PUT'])
@Auth.auth_required
def update(patient_id):
	req_data = request.get_json()
	post = PatientModel.get_one_patient_infos(patient_id)
	if not post:
		return custom_response({'error': 'patient information not found'})
	data, error = patient_info_schema.dump(req_data, partial = True)
	if error:
		return custom_response(error, 400)
	post.update(data)

	data = patient_info_schema.dump(post).data
	return custom_response(data, 200)


	
@patient_info_api.route('/<int:patient_id>', methods = ['DELETE'])
def delete(patient_id):
	"""
	delete a patient infos
	"""
	post = PatientModel.get_one_patient_infos(patient_id)
	if not post:
		return custom_response({'error':'patient not found'}, 400)
	data = patient_info_schema.dump(post).data
	if data.get('user_id') != g.user.id('id'):
		return custom_response({'error': 'permission denied'}, 400)

	post.delete()
	return custom_response({'message' : 'deleted'}, 204)

def custom_response(res, status_code):
	return Response(
		mimetype = "application/json",
		response = json.dumps(res),
		status = status_code
		)




