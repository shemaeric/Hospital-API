import json
from .base_test import BaseTestCase

class TestUserLogin(BaseTestCase):
  def test_login(self):
    with self.client:
      response_register = self.client.post(
        'api/v1/users',
        data = json.dumps(dict(
          name = 'shema',
          email = 'myemail@mail.com',
          password = 'shema123'
          )),
        content_type = 'application/json'
      )
      response = self.client.post(
        '/api/v1/users/login',
        data = json.dumps(dict(
          email = 'myemail@email.com',
          password = 'shema123',
          name = 'shema'
        )),
        content_type = "application/json"
      )
      response_data = json.loads(response.data.decode())
      print(response_data)
      self.assertTrue(response_data['status'] == 'success')
      self.assertTrue(response_data['message'] == 'Successfully logged in as shema')
      self.assertTrue(response_data['Authorization'])
      self.assertEqual(response.status_code, 201)

  def test_login_with_none_existing_username(self):
    with self.client:
      response = self.client.post(
        '/api/v1/users/login',
        data=json.dumps(dict(
          email = 'myemail@email.com',
          password = 'shema123',
          name = 'shema'
        )),
        content_type='application/json'
      )
      response_data = json.loads(response.data.decode())
      self.assertTrue(response_data['status'] == 'fail')
      self.assertTrue(response_data['message'] == 'The username you provided does not exist')
      self.assertEqual(response.status_code, 404)

  def test_login_with_a_wrong_password(self):
    with self.client:
      response = self.client.post(
        '/api/v1/users/login',
        data=json.dumps(dict(
          email = 'myemail@mail.com',
          password = 'shema123',
          name = 'shema'
        )),
        content_type = "application/json"
      )
      response_data = json.loads(response.data.decode())
      print(response_data)
      self.assertTrue(response_data['status'] == 'fail')
      self.assertTrue(response_data['message'] == 'The password you provided did not match the database password')
      self.assertEqual(response.status_code, 401)


