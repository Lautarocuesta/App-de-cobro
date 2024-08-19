from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import RegistrationForm, LoginForm, ProductForm
from app.models import User, Product, Order, Payment
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

### Rutas de Autenticación ###

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Tu cuenta ha sido creada, ¡ahora puedes iniciar sesión!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registro', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Error al iniciar sesión. Verifica tu correo y contraseña.', 'danger')
    return render_template('login.html', title='Iniciar Sesión', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

### Rutas de Gestión de Productos ###

@app.route('/product/new', methods=['GET', 'POST'])
@login_required
def new_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, price=form.price.data, stock=form.stock.data)
        db.session.add(product)
        db.session.commit()
        flash('El producto ha sido creado exitosamente', 'success')
        return redirect(url_for('home'))
    return render_template('create_product.html', title='Nuevo Producto', form=form)

@app.route('/product/<int:product_id>/update', methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm()
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.stock = form.stock.data
        db.session.commit()
        flash('El producto ha sido actualizado', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.name.data = product.name
        form.price.data = product.price
        form.stock.data = product.stock
    return render_template('create_product.html', title='Actualizar Producto', form=form)

@app.route('/product/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('El producto ha sido eliminado', 'success')
    return redirect(url_for('home'))

### Rutas de Gestión de Pedidos ###

@app.route('/order/new', methods=['GET', 'POST'])
@login_required
def new_order():
    # Aquí puedes implementar la lógica para crear un nuevo pedido
    # como agregar productos al carrito, calcular el total, etc.
    return render_template('create_order.html', title='Nuevo Pedido')

### Simulador de Pago/Cobro ###

@app.route('/order/<int:order_id>/pay', methods=['GET', 'POST'])
@login_required
def pay_order(order_id):
    order = Order.query.get_or_404(order_id)
    if request.method == 'POST':
        amount = request.form.get('amount')
        payment = Payment(order_id=order.id, amount=amount)
        db.session.add(payment)
        order.payment_status = 'Paid'
        db.session.commit()
        flash('El pago ha sido realizado exitosamente', 'success')
        return redirect(url_for('home'))
    return render_template('pay_order.html', title='Pagar Pedido', order=order)

@app.route('/order/<int:order_id>/collect', methods=['GET', 'POST'])
@login_required
def collect_order(order_id):
    order = Order.query.get_or_404(order_id)
    if request.method == 'POST':
        amount = request.form.get('amount')
        payment = Payment(order_id=order.id, amount=amount)
        db.session.add(payment)
        order.payment_status = 'Collected'
        db.session.commit()
        flash('El cobro ha sido realizado exitosamente', 'success')
        return redirect(url_for('home'))
    return render_template('collect_order.html', title='Cobrar Pedido', order=order)
