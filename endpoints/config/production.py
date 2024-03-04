from datetime import timedelta
import os

DEBUG = False
TESTING = False
SECRET_KEY = 'rn2wui202n23iur90240j30flkfn23unofwpfeo'
JWT_SECRET_KEY = 'wejior34weWEW21hjroih20QW94h2d7s234ds'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'db/mydata.db')
SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
SQLALCHEMY_TRACK_MODIFICATIONS = False