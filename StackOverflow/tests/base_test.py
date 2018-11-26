from unittest import TestCase
from .app import create_app
from migrate import DBMigration

class BaseTestCase(TestCase):


  def setUp(self):
    self.app = create_app(settings.TESTING)
    self.migrate = DBMigration()
    self.migrate.create_all()
    self.client = self.app.test_client()
    self.app_context = self.app.app_context()
    self.app_context.push()

  def tearDown(self):
    """removes the db and the context"""
    self.app_context.pop()