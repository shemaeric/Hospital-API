import unittest
import config
from ..app import create_app

app = create_app("testing")
class TestDevelopmentConfig(unittest.TestCase):
  def create_app(self):
    app.config.from_object('project.server.config.DevelopmentConfig')
    return app

  def test_app_is_development(self):
    self.assertTrue(app.config['DEBUG'] is False)
    self.assertFalse(create_app is None)
    self.assertTrue(
        app.config['DATABASE_URL'] == 'postgres://postgres:shema@127.0.0.1:5432/stackoverflow'
    )


class TestTestingConfig(unittest.TestCase):
  def create_app(self):
    app.config.from_object('project.server.config.TestingConfig')
    return app

  def test_app_is_testing(self):
    self.assertTrue(app.config['DEBUG'])
    self.assertTrue(
      app.config['DATABASE_URL'] == 'postgres://postgres:shema@127.0.0.1:5432/stackoverflow'
      )