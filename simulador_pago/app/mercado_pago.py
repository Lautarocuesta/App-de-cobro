import mercadopago


sdk = mercadopago.SDK("TEST-3727573019792359-082715-20105548c6dd3fd578d57c7c80bca7d8-1194947549")

# Datos del pago
payment_data = {
    "transaction_amount": 100.0,  # Monto de la transacción
    "token": "CARD_TOKEN",  # Reemplaza con el token de la tarjeta
    "description": "Descripción del producto o servicio",
    "installments": 1,  # Cantidad de cuotas
    "payment_method_id": "visa",  # Método de pago (visa, mastercard, etc.)
    "payer": {
        "email": "test_user_19653727@testuser.com"  # Correo del pagador
    }
}

# Crea el pago
try:
    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]
    print("Detalles del pago:", payment)
except mercadopago.exceptions.MercadoPagoError as e:
    print(f"Error al procesar el pago: {e}")

# Obtener detalles de un pago específico
payment_id = "123456789"  # Reemplaza con el ID real del pago

# Función para generar un QR para el cobro
def generar_qr_pago(amount, description, external_reference):
    # Crear la preferencia de pago
    preference_data = {
        "items": [
            {
                "title": description,
                "quantity": 1,
                "unit_price": amount,
            }
        ],
        "external_reference": external_reference
    }
    
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    
    # Generar la URL del código QR
    qr_url = f"https://api.mercadopago.com/instore/qr/{preference['id']}"
    
    return qr_url

# Ejemplo de uso de la función de QR
qr_url = generar_qr_pago(100.0, "Compra de Producto XYZ", "ORDER1234")
print(f"Escanea este código QR para pagar: {qr_url}")









try:
    payment_details = sdk.payment().get(payment_id)
    print("Detalles del pago por ID:", payment_details)
except mercadopago.exceptions.MercadoPagoError as e:
    print(f"Error al obtener los detalles del pago: {e}")
