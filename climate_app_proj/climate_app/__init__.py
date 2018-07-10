from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from climate_app.config import Config
from climate_app.app import app as capp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # register blueprints
    register_blueprints(app)
    return app


def init_db():
    app = create_app()
    db = SQLAlchemy()
    # initialize the db
    db.init_app(app)
    db.reflect(app=app)
    return db


def register_blueprints(app):
    app.register_blueprint(capp, url_prefix='/api/v1.0/')


db = init_db()
