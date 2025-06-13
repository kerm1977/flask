from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
import os
from werkzeug.utils import secure_filename # Para nombres de archivo seguros

# Importa db, bcrypt, migrate y User desde el nuevo archivo models.py
from models import db, bcrypt, migrate, User 
from contactos import contactos_bp # Esta línea sigue igual

app = Flask(__name__)
app.config.from_object(Config)

# Configuración para subida de archivos
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads', 'avatars')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Asegúrate de que la carpeta de subidas exista
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Inicializa db, bcrypt y migrate con la instancia de la aplicación
db.init_app(app)
bcrypt.init_app(app)
migrate.init_app(app, db) # Esto conecta tu app Flask y tu instancia de SQLAlchemy con Migrate

# Función para verificar extensiones de archivo permitidas
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rutas de la aplicación (mantenidas igual)
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    actividad_opciones = ["No Aplica", "La Tribu", "Senderista", "Enfermería", "Cocina", "Confección y Diseño", "Restaurante", "Transporte Terrestre", "Transporte Acuatico", "Transporte Aereo", "Migración", "Parque Nacional", "Refugio Silvestre", "Centro de Atracción", "Lugar para Caminata", "Acarreo", "Oficina de trámite", "Primeros Auxilios", "Farmacia", "Taller", "Abogado", "Mensajero", "Tienda", "Polizas", "Aerolínea", "Guía", "Banco", "Otros"]
    capacidad_opciones = ["Seleccionar Capacidad", "Rápido", "Intermedio", "Básico", "Iniciante"]
    participacion_opciones = ["No Aplica", "Solo de La Tribu", "Constante", "Inconstante", "El Camino de Costa Rica", "Parques Nacionales", "Paseo | Recreativo", "Revisar/Eliminar"]

    if request.method == 'POST':
        username = request.form['username_registro']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        nombre = request.form['nombre']
        primer_apellido = request.form['primer_apellido']
        telefono = request.form['telefono']

        segundo_apellido = request.form.get('segundo_apellido')
        telefono_emergencia = request.form.get('telefono_emergencia')
        nombre_emergencia = request.form.get('nombre_emergencia')
        empresa = request.form.get('empresa')
        cedula = request.form.get('cedula')
        direccion = request.form.get('notas')
        email = request.form.get('email')
        actividad = request.form.get('actividad')
        capacidad = request.form.get('capacidad')
        participacion = request.form.get('participacion')
        
        if not all([username, password, confirm_password, nombre, primer_apellido, telefono]):
            flash('Por favor, completa todos los campos obligatorios (*).', 'danger')
            return render_template('register.html', actividad_opciones=actividad_opciones, capacidad_opciones=capacidad_opciones, participacion_opciones=participacion_opciones)

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return render_template('register.html', actividad_opciones=actividad_opciones, capacidad_opciones=capacidad_opciones, participacion_opciones=participacion_opciones)

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Ese nombre de usuario ya está en uso. Por favor, elige otro.', 'danger')
            return render_template('register.html', actividad_opciones=actividad_opciones, capacidad_opciones=capacidad_opciones, participacion_opciones=participacion_opciones)
        
        if email:
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                flash('Ese correo electrónico ya está registrado. Por favor, usa otro.', 'danger')
                return render_template('register.html', actividad_opciones=actividad_opciones, capacidad_opciones=capacidad_opciones, participacion_opciones=participacion_opciones)

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        avatar_filename = None

        if 'avatar' in request.files:
            avatar_file = request.files['avatar']
            if avatar_file and allowed_file(avatar_file.filename):
                filename = secure_filename(avatar_file.filename)
                avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                avatar_file.save(avatar_path)
                avatar_filename = 'uploads/avatars/' + filename
            elif avatar_file.filename != '':
                flash('Tipo de archivo de avatar no permitido. Solo se aceptan PNG, JPG, JPEG, GIF.', 'warning')
                return render_template('register.html', actividad_opciones=actividad_opciones, capacidad_opciones=capacidad_opciones, participacion_opciones=participacion_opciones)
        
        if not avatar_filename:
            avatar_filename = 'images/defaults/default_avatar.png'

        new_user = User(
            username=username,
            password=hashed_password,
            nombre=nombre,
            primer_apellido=primer_apellido,
            telefono=telefono,
            avatar_url=avatar_filename,
            segundo_apellido=segundo_apellido,
            telefono_emergencia=telefono_emergencia,
            nombre_emergencia=nombre_emergencia,
            empresa=empresa,
            cedula=cedula,
            direccion=direccion,
            email=email,
            actividad=actividad if actividad != "No Aplica" else None,
            capacidad=capacidad if capacidad != "Seleccionar Capacidad" else None,
            participacion=participacion if participacion != "No Aplica" else None
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar usuario: {e}', 'danger')
            return render_template('register.html', actividad_opciones=actividad_opciones, capacidad_opciones=capacidad_opciones, participacion_opciones=participacion_opciones)

    return render_template('register.html', actividad_opciones=actividad_opciones, capacidad_opciones=capacidad_opciones, participacion_opciones=participacion_opciones)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        user = User.query.filter_by(username=username_or_email).first()

        if not user:
            user = User.query.filter_by(email=username_or_email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['logged_in'] = True
            session['username'] = user.username
            session['email'] = user.email
            flash('¡Sesión iniciada correctamente!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Nombre de usuario/correo electrónico o contraseña incorrectos.', 'danger')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/home')
def home():
    if 'logged_in' in session and session['logged_in']:
        user = User.query.filter_by(username=session['username']).first()
        avatar_url = None
        if user and user.avatar_url:
            avatar_url = url_for('static', filename=user.avatar_url)
        else:
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

# Registra el Blueprint después de que la app haya sido inicializada
app.register_blueprint(contactos_bp)

if __name__ == '__main__':
    app.run(debug=True, port=3030)