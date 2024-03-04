from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from endpoints import config
from flask_jwt_extended import JWTManager

DB = SQLAlchemy()

def create_app():
    flask_app = Flask(__name__)
    flask_app.secret_key = config.SECRET_KEY
    flask_app.config.from_object('endpoints.config')
    jwt = JWTManager(flask_app)

    @jwt.unauthorized_loader
    def missing_authorization_header_callback(error_str):
        return {"error": error_str}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error_str):
        return {"error": error_str}, 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {"error": "Token has expired"}, 401

    DB.init_app(flask_app)
    Migrate(flask_app, DB)
    return flask_app