from flask import render_template, redirect, url_for, flash, request
from app import db
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required

def home():
    return render_template('home.html')

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

def logout():
    logout_user()
    return redirect(url_for('home'))

def cobro():
    return render_template('cobro.html')
