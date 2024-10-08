from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    username = 'upsdbxna2ziitiwo'
    password = '8ittRtvlqvMqqK239Ujl'
    hostname = 'bi6eeygebg4oqzyflcde-mysql.services.clever-cloud.com'
    database = 'bi6eeygebg4oqzyflcde'
    app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{username}:{password}@{hostname}/{database}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    # Importar y registrar las rutas
    from .routes import main
    app.register_blueprint(main)

    return app
