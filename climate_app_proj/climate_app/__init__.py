from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from climate_app.config import Config
from climate_app.app import app as capp


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # initialize the db
    db.init_app(app)
    db.reflect(app=app)
    # register blueprints
    register_blueprints(app)

    return app


def register_blueprints(app):
    app.register_blueprint(capp, url_prefix='/api/v1.0/')

