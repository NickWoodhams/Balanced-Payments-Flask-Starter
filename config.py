import os
basedir = os.path.abspath(os.path.dirname(__file__))


CSRF_ENABLED = True
SECRET_KEY = 'super_secret_key'

SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@127.0.0.1/marketplace'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

DEBUG = True
BALANCED_MARKETPLACE_URI = ''  # looks like: /v1/marketplaces/TEST-RANDOMSTRING
BALANCED_API_KEY = ''
