from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    username = 'u227ypgl485hfs3b'
    password = 'v0Lovy3aFm6KSUcNphbi'
    hostname = 'bsaf3ulb51roa33cb86b-mysql.services.clever-cloud.com'
    database = 'bsaf3ulb51roa33cb86b'
    app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{username}:{password}@{hostname}/{database}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

        from .routes import home, register, login, logout, cobro

        app.add_url_rule('/', 'home', home)
        app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
        app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
        app.add_url_rule('/logout', 'logout', logout)
        app.add_url_rule('/cobro', 'cobro', cobro)

    return app
