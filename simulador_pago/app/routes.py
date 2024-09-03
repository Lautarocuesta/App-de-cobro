from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.forms import RegistrationForm, LoginForm
from app.models import User
import mercadopago

# MercadoPago SDK
sdk = mercadopago.SDK("YOUR_ACCESS_TOKEN")

# Datos de pedidos de ejemplo
orders = [
    {'id': 1, 'total': 100.0},
    {'id': 2, 'total': 150.0}
]

main = Blueprint('main', __name__)

@main.route('/')
def home():
    # Crear preferencias de pago y devolver los IDs
    for order in orders:
        order['preference_id'] = crear_preferencia(order['total'], f"Compra de Producto {order['id']}", f"ORDER{order['id']}")
    return render_template('cobro.html', orders=orders)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Tu cuenta ha sido creada, ¡ahora puedes iniciar sesión!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Registro', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Error al iniciar sesión. Verifica tu correo y contraseña.', 'danger')
    return render_template('login.html', title='Iniciar Sesión', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/cobro')
def cobro():
    return render_template('cobro.html')

@main.route('/process_payment', methods=['POST'])
def process_payment():
    data = request.get_json()
    request_options = mercadopago.config.RequestOptions()
    request_options.custom_headers = {
        'x-idempotency-key': 'UNIQUE_KEY'  # Genera una clave única para evitar duplicados
    }

    payment_data = {
        "transaction_amount": data['transaction_amount'],
        "token": data['token'],
        "description": data['description'],
        "installments": data['installments'],
        "payment_method_id": data['payment_method_id'],
        "payer": {
            "email": data['payer']['email'],
            "identification": {
                "type": data['payer']['identification']['type'],
                "number": data['payer']['identification']['number']
            }
        }
    }

    try:
        payment_response = sdk.payment().create(payment_data, request_options)
        return jsonify(payment_response["response"])
    except Exception as e:
        print(f"Error al procesar el pago: {e}")
        return jsonify({'error': 'Error al procesar el pago'}), 500

def crear_preferencia(amount, description, external_reference):
    preference_data = {
        "items": [
            {
                "title": description,
                "quantity": 1,
                "unit_price": amount
            }
        ],
        "external_reference": external_reference
    }
    
    try:
        preference_response = sdk.preference().create(preference_data)
        return preference_response['response']['id']
    except mercadopago.exceptions.MercadoPagoError as e:
        print(f"Error al crear la preferencia: {e}")
        return None
