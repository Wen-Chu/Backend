from datetime import timedelta
import os

DEBUG = True
TESTING = True
SECRET_KEY = 'test-key'
JWT_SECRET_KEY = 'test-jwt-key'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'db/test_mydata.db')
SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
SQLALCHEMY_TRACK_MODIFICATIONS = False