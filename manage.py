import os
import unittest

from flask_script import Manager
from dotenv import load_dotenv

from api import create_app

load_dotenv()

app = create_app(os.getenv('ENVIRONMENT', 'dev'))

manager = Manager(app)

@manager.command
def run():
  app.run()

@manager.command
def test():
  """Runs the unit tests."""

  tests = unittest.TestLoader().discover('api/tests/', pattern='*/test_*.py')
  unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()