from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from datetime import datetime

# Instanciamos SQLAlchemy y Bcrypt aquí, pero no los asociamos aún a la app
# Esto se hará en app.py con db.init_app(app)
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate() # Instanciamos Migrate aquí también

# Definición del modelo de usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Campos obligatorios
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    primer_apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=True)

    # Campos opcionales (existentes)
    avatar_url = db.Column(db.String(255), default='images/defaults/default_avatar.png')
    segundo_apellido = db.Column(db.String(100), nullable=True)
    telefono_emergencia = db.Column(db.String(20), nullable=True)
    nombre_emergencia = db.Column(db.String(100), nullable=True)
    empresa = db.Column(db.String(100), nullable=True)
    cedula = db.Column(db.String(50), nullable=True)
    direccion = db.Column(db.String(255), nullable=True) # Campo de Dirección existente
    email = db.Column(db.String(120), unique=True, nullable=True)
    actividad = db.Column(db.String(50), nullable=True)
    capacidad = db.Column(db.String(50), nullable=True)
    participacion = db.Column(db.String(50), nullable=True)

    # NUEVOS CAMPOS AÑADIDOS
    fecha_cumpleanos = db.Column(db.Date, nullable=True) # Para la fecha de cumpleaños
    tipo_sangre = db.Column(db.String(5), nullable=True) # Para el tipo de sangre (ej. A+, O-)
    poliza = db.Column(db.String(100), nullable=True) # Número o nombre de póliza
    aseguradora = db.Column(db.String(100), nullable=True) # Nombre de la aseguradora
    alergias = db.Column(db.Text, nullable=True) # Para alergias (texto largo)
    enfermedades_cronicas = db.Column(db.Text, nullable=True) # Para enfermedades crónicas (texto largo)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.nombre}')"
