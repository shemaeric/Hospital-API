import unittest
import config
from ..app import create_app

class TestDevelopmentConfig(unittest.TestCase):
  def create_app(self):
    app.config.from_object('project.server.config.DevelopmentConfig')
    return app

  def test_app_is_development(self):
    # self.assertTrue(app.config['DEBUG'] is True)
    self.assertFalse(current_app is None)
    self.assertTrue(
        app.config['JWT_SECRET_KEY'] == 'postgresql://postgres:shema@127.0.0.1:543/stackoverflow'
    )


class TestTestingConfig(unittest.TestCase):
  def create_app(self):
    app.config.from_object('project.server.config.TestingConfig')
    return app

  def test_app_is_testing(self):
    self.assertTrue(app.config['DEBUG'])
    self.assertTrue(
      app.config['JWT_SECRET_KEY'] == 'postgresql://postgres:shema@127.0.0.1:543/stackoverflow'
      )