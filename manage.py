import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from StackOverflow.models import UserModel


env_name = os.getenv('FLASK_ENV', 'default')

from StackOverflow.app import create_app

app = create_app(env_name)
from StackOverflow.models import db
migrate = Migrate(app=app, db=db)

manager = Manager(app=app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
  manager.run()