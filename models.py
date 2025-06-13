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

    # Campos opcionales
    avatar_url = db.Column(db.String(255), default='images/defaults/default_avatar.png')
    segundo_apellido = db.Column(db.String(100), nullable=True)
    telefono_emergencia = db.Column(db.String(20), nullable=True)
    nombre_emergencia = db.Column(db.String(100), nullable=True)
    empresa = db.Column(db.String(100), nullable=True)
    cedula = db.Column(db.String(50), nullable=True)
    direccion = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    actividad = db.Column(db.String(50), nullable=True)
    capacidad = db.Column(db.String(50), nullable=True)
    participacion = db.Column(db.String(50), nullable=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.nombre}')"