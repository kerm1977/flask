from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate # ¡NUEVA IMPORTACIÓN!
from config import Config
import os
from datetime import datetime
from werkzeug.utils import secure_filename # Para nombres de archivo seguros

app = Flask(__name__)
app.config.from_object(Config)

# Configuración para subida de archivos
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads', 'avatars')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Asegúrate de que la carpeta de subidas exista
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ¡NUEVA LÍNEA! Inicializar Flask-Migrate
migrate = Migrate(app, db) # Esto conecta tu app Flask y tu instancia de SQLAlchemy con Migrate

# Función para verificar extensiones de archivo permitidas
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Definición del modelo de usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Campos obligatorios
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    primer_apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False) # Ahora obligatorio
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) # Fecha automática

    # Campos opcionales
    avatar_url = db.Column(db.String(255), default='images/defaults/default_avatar.png') # Ruta por defecto
    segundo_apellido = db.Column(db.String(100), nullable=True)
    telefono_emergencia = db.Column(db.String(20), nullable=True)
    nombre_emergencia = db.Column(db.String(100), nullable=True)
    empresa = db.Column(db.String(100), nullable=True)
    cedula = db.Column(db.String(50), nullable=True)
    direccion = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True) # Ahora opcional, pero único si se proporciona
    actividad = db.Column(db.String(50), nullable=True)
    capacidad = db.Column(db.String(50), nullable=True)
    participacion = db.Column(db.String(50), nullable=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.nombre}')"

# Rutas de la aplicación

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Opciones para los selectores
    actividad_opciones = ["No Aplica", "La Tribu", "Senderista", "Enfermería", "Cocina", "Confección y Diseño", "Restaurante", "Transporte Terrestre", "Transporte Acuatico", "Transporte Aereo", "Migración", "Parque Nacional", "Refugio Silvestre", "Centro de Atracción", "Lugar para Caminata", "Acarreo", "Oficina de trámite", "Primeros Auxilios", "Farmacia", "Taller", "Abogado", "Mensajero", "Tienda", "Polizas", "Aerolínea", "Guía", "Banco", "Otros"]
    capacidad_opciones = ["Seleccionar Capacidad", "Rápido", "Intermedio", "Básico", "Iniciante"]
    participacion_opciones = ["No Aplica", "Solo de La Tribu", "Constante", "Inconstante", "El Camino de Costa Rica", "Parques Nacionales", "Paseo | Recreativo", "Revisar/Eliminar"]

    if request.method == 'POST':
        # Campos obligatorios
        username = request.form['username_registro'] # Cambiado el nombre para evitar conflictos si se usa el mismo en login
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        nombre = request.form['nombre']
        primer_apellido = request.form['primer_apellido']
        telefono = request.form['telefono']

        # Campos opcionales
        segundo_apellido = request.form.get('segundo_apellido')
        telefono_emergencia = request.form.get('telefono_emergencia')
        nombre_emergencia = request.form.get('nombre_emergencia')
        empresa = request.form.get('empresa')
        cedula = request.form.get('cedula')
        direccion = request.form.get('direccion')
        email = request.form.get('email')
        actividad = request.form.get('actividad')
        capacidad = request.form.get('capacidad')
        participacion = request.form.get('participacion')
        
        # Validaciones básicas de campos obligatorios
        if not all([username, password, confirm_password, nombre, primer_apellido, telefono]):
            flash('Por favor, completa todos los campos obligatorios (*).', 'danger')
            return render_template('register.html', actividad_opciones=actividad_opciones, capacidad_opciones=capacidad_opciones, participacion_opciones=participacion_opciones)

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return render_template('register.html', actividad_opciones=actividad_opciones, capacidad_opciones=capacidad_opciones, participacion_opciones=participacion_opciones)

        # Verificar si el usuario ya existe
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Ese nombre de usuario ya está en uso. Por favor, elige otro.', 'danger')
            return render_template('register.html', actividad_opciones=actividad_opciones, capacidad_opciones=capacidad_opciones, participacion_opciones=participacion_opciones)
        
        # Verificar si el email existe SOLO SI SE PROPORCIONA (es opcional pero único si se da)
        if email:
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                flash('Ese correo electrónico ya está registrado. Por favor, usa otro.', 'danger')
                return render_template('register.html', actividad_opciones=actividad_opciones, capacidad_opciones=capacidad_opciones, participacion_opciones=participacion_opciones)


        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        avatar_filename = None

        # Manejo de la subida de imagen de avatar
        if 'avatar' in request.files:
            avatar_file = request.files['avatar']
            if avatar_file and allowed_file(avatar_file.filename):
                filename = secure_filename(avatar_file.filename)
                avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                avatar_file.save(avatar_path)
                avatar_filename = 'uploads/avatars/' + filename # Guardar la ruta relativa para la DB
            elif avatar_file.filename != '': # Si se subió un archivo pero no es permitido
                flash('Tipo de archivo de avatar no permitido. Solo se aceptan PNG, JPG, JPEG, GIF.', 'warning')
                return render_template('register.html', actividad_opciones=actividad_opciones, capacidad_opciones=capacidad_opciones, participacion_opciones=participacion_opciones)
        
        # Si no se subió ningún avatar o no se especificó, usa el por defecto
        if not avatar_filename:
            avatar_filename = 'images/defaults/default_avatar.png'


        new_user = User(
            username=username,
            password=hashed_password,
            nombre=nombre,
            primer_apellido=primer_apellido,
            telefono=telefono,
            avatar_url=avatar_filename, # Se guarda la ruta del avatar
            segundo_apellido=segundo_apellido,
            telefono_emergencia=telefono_emergencia,
            nombre_emergencia=nombre_emergencia,
            empresa=empresa,
            cedula=cedula,
            direccion=direccion,
            email=email,
            actividad=actividad if actividad != "No Aplica" else None, # Guardar None si es "No Aplica"
            capacidad=capacidad if capacidad != "Seleccionar Capacidad" else None, # Guardar None si es "Seleccionar Capacidad"
            participacion=participacion if participacion != "No Aplica" else None # Guardar None si es "No Aplica"
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            # Un error más específico si ocurre, por ejemplo, por unicidad (aunque ya se validó antes)
            flash(f'Error al registrar usuario: {e}', 'danger')
            return render_template('register.html', actividad_opciones=actividad_opciones, capacidad_opciones=capacidad_opciones, participacion_opciones=participacion_opciones)

    # Si el método es GET (primera vez que se carga la página)
    return render_template('register.html', actividad_opciones=actividad_opciones, capacidad_opciones=capacidad_opciones, participacion_opciones=participacion_opciones)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Recuperamos el 'username_or_email' del formulario
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        # Buscamos al usuario por su 'username'
        user = User.query.filter_by(username=username_or_email).first()

        # Si no se encuentra por nombre de usuario, intenta por email
        if not user:
            user = User.query.filter_by(email=username_or_email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['logged_in'] = True
            session['username'] = user.username # Aseguramos que guardamos el username
            session['email'] = user.email # Guardar el email en la sesión también
            flash('¡Sesión iniciada correctamente!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Nombre de usuario/correo electrónico o contraseña incorrectos.', 'danger')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/home')
def home():
    if 'logged_in' in session and session['logged_in']:
        # Recuperar el usuario de la DB para obtener el avatar_url
        user = User.query.filter_by(username=session['username']).first()
        avatar_url = None
        if user and user.avatar_url:
            avatar_url = url_for('static', filename=user.avatar_url)
        else:
            # Si no hay avatar definido o usuario no encontrado, usar el por defecto
            avatar_url = url_for('static', filename='images/defaults/default_avatar.png')

        return render_template('home.html', username=session['username'], avatar_url=avatar_url)
    else:
        flash('Por favor, inicia sesión para acceder a esta página.', 'info')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    # ¡IMPORTANTE! Eliminamos db.create_all() de aquí.
    # Flask-Migrate se encargará de crear y actualizar la base de datos.
    app.run(debug=True, port=3030) # Puerto lo dejé como entero