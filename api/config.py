import os

from dotenv import load_dotenv


load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
  """Parent configuration class."""

  CSRF_ENABLED = True
  DEBUG = False
  MONGODB_HOST = os.getenv('DATABASE_URL')
  SECRET = os.getenv('SECRET')


class DefaultConfig(BaseConfig):
  """Parent configuration class."""

  CSRF_ENABLED = True
  DEBUG = False
  MONGODB_SETTINGS = {
    'host': os.getenv('DATABASE_URL')
  }
  SECRET = os.getenv('SECRET')


class DevelopmentConfig(BaseConfig):
  """Configurations for Development."""

  DEBUG = True


class TestingConfig(BaseConfig):
  """Configurations for Testing, with a separate test database."""

  DEBUG = True
  MONGOENGINE_DATABASE_URI = 'postgresql://localhost/test_db'
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