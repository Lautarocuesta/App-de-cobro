from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://uezytq7dxx48hp8w:s18HO1qr2Nw46fXbuHPg@bhyb1fa898t0ow9ufdlc-mysql.services.clever-cloud.com/bhyb1fa898t0ow9ufdlc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import routes, models, forms

if __name__ == '__main__':
    app.run(debug=True)
