from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'tu_clave_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    login_manager.init_app(app)

    # Importa tu modelo User después de inicializar db y login_manager
    from .models import User

    # Definir la función load_user para cargar el usuario desde la base de datos
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

        # Importa tus rutas aquí
        from .routes import home, register, login, logout

        app.add_url_rule('/', 'home', home)
        app.add_url_rule('/register', 'register', register)
        app.add_url_rule('/login', 'login', login)
        app.add_url_rule('/logout', 'logout', logout)

    return app
