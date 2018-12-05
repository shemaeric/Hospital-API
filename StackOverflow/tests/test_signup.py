import unittest
import os
import json
from ..app import create_app,db


class UsersTest(unittest.TestCase):
  """
  Users Test Case
  """
  def setUp(self):
    """
    Test Setup
    """
    self.app = create_app("testing")
    self.client = self.app.test_client
    self.user = {
      'name': 'olawale',
      'email': 'olawale@mail.com',
      'password': 'passw0rd!'
    }

    with self.app.app_context():
      # create all tables
      db.create_all()
  
  def test_user_creation(self):
    """ test user creation with valid credentials """
    res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user))
    json_data = json.loads(res.data)
    self.assertTrue(json_data.get('jwt_token'))
    self.assertEqual(res.status_code, 201)
