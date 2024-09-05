from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models import User
import mercadopago
from app.forms import RegistrationForm, LoginForm, ProductForm, PaymentForm

# MercadoPago SDK
sdk = mercadopago.SDK("TEST-3727573019792359-082715-20105548c6dd3fd578d57c7c80bca7d8-1194947549")

# Datos de productos de ejemplo
products = [
    {'id': 1, 'name': 'Producto 1', 'price': 50.0, 'stock': 10},
    {'id': 2, 'name': 'Producto 2', 'price': 100.0, 'stock': 5}
]

# Datos de pedidos de ejemplo
orders = [
    {'id': 1, 'total': 100.0, 'products': products},
    {'id': 2, 'total': 150.0, 'products': products}
]

main = Blueprint('main', __name__)
webhook = Blueprint('webhook', __name__)

@main.route('/')
def home():
    return render_template('home.html')

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
        return redirect(url_for('main.cobro'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            next_page = request.args.get('next')
            print(f"Next page: {next_page}")  # Imprime el valor de next
            if next_page and next_page != url_for('main.login'):
                return redirect(next_page)
            else:
                return redirect(url_for('main.cobro'))
        else:
            flash('Error al iniciar sesión. Verifica tu correo y contraseña.', 'danger')
    return render_template('login.html', title='Iniciar Sesión', form=form)


@main.route('/cobro', methods=['GET', 'POST'])
@login_required
def cobro():
    form = PaymentForm()
    if form.validate_on_submit():
        # Aquí podrías manejar el proceso de pago, por ejemplo, crear un token con MercadoPago
        token = sdk
        # Puedes agregar más lógica para manejar el pago

        flash('Pago procesado con éxito', 'success')
        return redirect(url_for('main.home'))

    orders_with_preferences = []
    for order in orders:
        preference_id = crear_preferencia(order['total'], f"Compra de Producto {order['id']}", f"ORDER{order['id']}")
        if preference_id:
            orders_with_preferences.append({
                'id': order['id'],
                'total': order['total'],
                'preference_id': preference_id
            })
    return render_template('cobro.html', orders=orders_with_preferences, form=form)




@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/test_redirect')
def test_redirect():
    return redirect(url_for('main.home'))


@main.route('/process_payment', methods=['POST'])
@login_required
def process_payment():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    data = request.get_json()

    payment_data = {
        "transaction_amount": data.get('transaction_amount'),
        "token": data.get('token'),
        "description": data.get('description'),
        "installments": data.get('installments'),
        "payment_method_id": data.get('payment_method_id'),
        "issuer_id": data.get('issuer_id'),
        "payer": {
            "email": data.get('payer', {}).get('email'),
            "identification": {
                "type": data.get('payer', {}).get('identification', {}).get('type'),
                "number": data.get('payer', {}).get('identification', {}).get('number')
            }
        }
    }

    try:
        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {
            'x-idempotency-key': 'UNIQUE_KEY'  # Genera una clave única para evitar duplicados
        }
        
        payment_response = sdk.payment().create(payment_data, request_options)
        return jsonify(payment_response['response'])
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
        return preference_response['response'].get('id')
    except Exception as e:
        print(f"Error al crear la preferencia: {e}")
        return None
    
def verificar_preferencia(preference_id):
    try:
        preference_response = sdk.preference().get(preference_id)
        return preference_response['response']
    except Exception as e:
        print(f"Error al verificar la preferencia: {e}")
        return None

def verificar_pago(payment_id):
    try:
        payment_response = sdk.payment().get(payment_id)
        return payment_response['response']
    except Exception as e:
        print(f"Error al verificar el pago: {e}")
        return None
    