from flask import Flask
from medic.settings import Config
import logging
from medic.models import db

def create_app():
    medic_app = Flask(__name__)
    medic_app.config.from_object(Config)
    from medic.route import api_bp
    medic_app.register_blueprint(api_bp, url_prefix='/api/v1')
    db.init_app(medic_app)
    
    return medic_app


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler('log/api.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()
