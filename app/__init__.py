from .routes import main
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db = SQLAlchemy()
    db.init_app(app)
    
    app.register_blueprint(main)

    return app