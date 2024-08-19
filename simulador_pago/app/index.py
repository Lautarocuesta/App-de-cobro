# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging
import pymysql

# Inicializar las extensiones antes de crear la aplicación
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Crear la aplicación Flask
    app = Flask(__name__)
    
    # Configuración de la clave secreta y la base de datos en Clever Cloud
    app.config['SECRET_KEY'] = 'copa'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://uezytq7dxx48hp8w:s18HO1qr2Nw46fXbuHPg@bhyb1fa898t0ow9ufdlc-mysql.services.clever-cloud.com/bhyb1fa898t0ow9ufdlc'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {
            'connect_timeout': 60  # Aumenta el tiempo de espera a 60 segundos
        }
    }

    # Configurar logging para SQLAlchemy
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    logging.getLogger('pymysql').setLevel(logging.DEBUG)
    
    # Instalar pymysql como MySQLdb
    pymysql.install_as_MySQLdb()

    # Inicializar las extensiones con la aplicación
    db.init_app(app)
    login_manager.init_app(app)

    # Registrar los blueprints
    from app.routes import main
    app.register_blueprint(main)

    return app
