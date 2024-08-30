from flask import Flask, render_template, redirect, url_for, request, jsonify
import mercadopago

app = Flask(__name__)

sdk = mercadopago.SDK("TEST-3727573019792359-082715-20105548c6dd3fd578d57c7c80bca7d8-1194947549")

# Datos de pedidos de ejemplo
orders = [
    {'id': 1, 'total': 100.0},
    {'id': 2, 'total': 150.0}
]

@app.route('/')
def index():
    # Crear preferencias de pago y devolver los IDs
    for order in orders:
        order['preference_id'] = crear_preferencia(order['total'], f"Compra de Producto {order['id']}", f"ORDER{order['id']}")
    return render_template('cobro.html', orders=orders)

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

if __name__ == '__main__':
    app.run(debug=True)


