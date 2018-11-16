import os

class Development(object):

  DEBUG = True
  TESTING = True
  JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class Production(object):

  DEBUG = False
  TESTING = False
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
  JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

  ACCEPT = True
  PENDING = False
  VOTES = 0
  DOWNVOTE = VOTES - 1

app_config = {
    'development': Development,
    'production': Production,
    'default': Production
}