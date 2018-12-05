import unittest
import os
import json
from ..app import create_app

class TestPatientInfos(unittest.TestCase):
  def test_patient_infos(self):
    response = self.client.post(
      '/api/v1/patient_infos',
      data = json.dumps(dict(
          beneficiary_name = 'shema',
          district = 'kayonza',
          sector = '  nyamirama',
          village = 'rulambi',
          balance = 10000,
          owner_id = 345654333,
          head_household_name = 'eric',
          sex = 'Male',
          tel_patient = 2345665334
      )),
      content_type = 'applicatio/json'
    )
    json_data = json.loads(res.data)
    self.assertEqual(res.status_code, 201)