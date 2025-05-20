from .routes import main
from flask import Flask
from config import DevelopmentConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    
    app.register_blueprint(main)

    return app