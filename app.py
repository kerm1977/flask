# app.py

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Definición del modelo de usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# Rutas de la aplicación

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not username or not email or not password or not confirm_password:
            flash('Por favor, completa todos los campos.', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return render_template('register.html')

        # Verificar si el usuario o el email ya existen
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            flash('Ese nombre de usuario ya está en uso. Por favor, elige otro.', 'danger')
            return render_template('register.html')
        if existing_email:
            flash('Ese correo electrónico ya está registrado. Por favor, inicia sesión o usa otro.', 'danger')
            return render_template('register.html')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback() # En caso de error, deshaz la transacción
            flash(f'Error al registrar usuario: {e}', 'danger')
            return render_template('register.html')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # CAMBIO AQUÍ: Recuperamos el 'username' del formulario en lugar del 'email'
        username_or_email = request.form['username_or_email'] # Usaremos un campo genérico en el HTML
        password = request.form['password']

        # CAMBIO AQUÍ: Buscamos al usuario por su 'username'
        user = User.query.filter_by(username=username_or_email).first()

        # Si no se encuentra por nombre de usuario, intenta por email (opcional, para flexibilidad)
        if not user:
            user = User.query.filter_by(email=username_or_email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['logged_in'] = True
            session['username'] = user.username # Aseguramos que guardamos el username
            session['email'] = user.email
            flash('¡Sesión iniciada correctamente!', 'success')
            return redirect(url_for('home'))
        else:
            # Mensaje más genérico ya que puede ser usuario o email
            flash('Nombre de usuario/correo electrónico o contraseña incorrectos.', 'danger')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/home')
def home():
    if 'logged_in' in session and session['logged_in']:
        return render_template('home.html', username=session['username'])
    else:
        flash('Por favor, inicia sesión para acceder a esta página.', 'info')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Esto creará la base de datos y las tablas si no existen
    with app.app_context():
        db.create_all()
    app.run(debug=True, port="3030")