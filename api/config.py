import os
from urllib.parse import urlparse

from dotenv import load_dotenv


load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
  """Parent configuration class."""

  CSRF_ENABLED = True
  DEBUG = False
  JWT_SECRET_KEY = os.getenv('JWT_SECRET')

  MONGODB_HOST = os.getenv('DATABASE_URL')
  
  parsed_host = urlparse(MONGODB_HOST)
  MONGODB_DB = parsed_host.path.strip("/")
  MONGODB_PORT = parsed_host.port
  MONGODB_USERNAME = parsed_host.username
  MONGODB_PASSWORD = parsed_host.password

  SECRET = os.getenv('SECRET')


class DevelopmentConfig(BaseConfig):
  """Configurations for Development."""

  DEBUG = True


class TestingConfig(BaseConfig):
  """Configurations for Testing, with a separate test database."""

  DEBUG = True
  MONGOENGINE_DATABASE_URI = 'mongodb://localhost/t3-test-db'
  TESTING = True


class StagingConfig(BaseConfig):
  """Configurations for Staging."""

  DEBUG = True


class ProductionConfig(BaseConfig):
  """Configurations for Production."""

  DEBUG = False
  TESTING = False


app_configs = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'stage': StagingConfig,
    'prod': ProductionConfig,
}