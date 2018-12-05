from . import db
from marshmallow import fields, Schema
import datetime

class PatientModel(db.Model):

	__tablename__ = 'patient_infos'

	id = db.Column(db.Integer, primary_key = True)
	beneficiary_name = db.Column(db.String(128), nullable = False)
	district = db.Column(db.String(128), nullable = False)
	sector = db.Column(db.String(128), nullable = False)
	village = db.Column(db.String(128), nullable = False)
	balance = db.Column(db.Integer)
	owner_id = db.Column(db.Integer,unique = True)
	head_household_name = db.Column(db.String(128), nullable = False)
	sex = db.Column(db.String(20), nullable = False)
	tel_patient = db.Column(db.Integer)
	created_at = db.Column(db.DateTime)
	modified_at = db.Column(db.DateTime)


	def __init__(self,data):
		self.beneficiary_name = data.get('beneficiary_name')
		self.district = data.get('district')
		self.sector = data.get('sector')
		self.village = data.get('village')
		self.balance = data.get('balance')
		self.owner_id = data.get('owner_id')
		self.head_household_name = data.get('head_household_name')
		self.sex = data.get('sex')
		self.created_at = datetime.datetime.utcnow()
		self.modified_at = datetime.datetime.utcnow()

	def save(self):
		db.session.add(self)
		db.session.commit()

	def update(self,data):
		for key, item in data.items():
			setattr(self, key, data)
		self.modified_at = datetime.datetime.utcnow()
		db.session.commit()


	def delete(self):
		db.session.delete(self)
		db.session.commit()

	@staticmethod
	def get_all_patients_infos():
		return PatientModel.query.all()

	@staticmethod
	def get_one_patient_infos(id):
		return PatientModel.query.all(id)

	@staticmethod
	def update(self,data):
		for key,item in data.items():
			setattr(self, key, item)
		self.modified_at = datetime.datetime.utcnow()
		db.session.commit()

	def __repr__(self):
		return '<id {}>'.format(self.id)

class PatientSchema(Schema):

	id = fields.Int(dump_only = True)
	beneficiary_name = fields.Str(required = True)
	district = fields.Str(required = True)
	sector = fields.Str(required = True)
	village = fields.Str(required = True)
	balance = fields.Int(required = True)
	owner_id = fields.Int(required = True)
	head_household_name = fields.Str(required = True)
	sex = fields.Str(required = True)
	created_at = fields.DateTime(dump_only = True)
	modified_at = fields.DateTime(dump_only = True)

		

