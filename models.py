from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from datetime import datetime, date # Importar date para manejar fechas

# Instanciamos SQLAlchemy y Bcrypt aquí, pero no los asociamos aún a la app
# Esto se hará en app.py con db.init_app(app)
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate() # Instanciamos Migrate aquí también

# Tabla de asociación para la relación muchos-a-muchos entre Note y User
# para los usuarios autorizados a ver una nota.
note_viewers = db.Table('note_viewers',
    db.Column('note_id', db.Integer, db.ForeignKey('note.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


# Definición del modelo de usuario (existente)
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

# MODELO Project (existente)
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_proyecto = db.Column(db.String(255), nullable=False)
    imagen_proyecto_url = db.Column(db.String(255), nullable=True) # Para guardar la URL de la imagen

    # Relacionado con la propuesta
    propuesta_por = db.Column(db.String(100), nullable=True) # Jenny Ceciliano Cordoba, Kenneth Ruiz Matamoros, Otro
    
    # Campo para el invitado (relación con User)
    nombre_invitado_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    nombre_invitado = db.relationship('User', foreign_keys=[nombre_invitado_id]) # Relación con el modelo User

    provincia = db.Column(db.String(50), nullable=True)
    fecha_actividad_propuesta = db.Column(db.Date, nullable=True)
    dificultad = db.Column(db.String(50), nullable=True) # No Aplica, Iniciante, Básico, Intermedio, Avanzado, Técnico

    transporte_terrestre = db.Column(db.String(50), nullable=True) # Autobús, Buseta, Auto, Moto, 4x4
    transporte_acuatico = db.Column(db.String(2), nullable=True) # Si/No aplica
    transporte_aereo = db.Column(db.String(2), nullable=True) # Si/No aplica
    precio_entrada_aplica = db.Column(db.String(2), nullable=True) # Si/No aplica

    nombre_lugar = db.Column(db.String(255), nullable=True)
    contacto_lugar = db.Column(db.String(255), nullable=True)
    telefono_lugar = db.Column(db.String(20), nullable=True)
    tipo_terreno = db.Column(db.String(50), nullable=True) # No aplica, Asfalto, Acuatico, Lastre, Arena, Montañoso
    mas_tipo_terreno = db.Column(db.Text, nullable=True) # Campo adicional para especificar más tipos de terreno

    presupuesto_total = db.Column(db.Float, nullable=True)
    costo_entrada = db.Column(db.Float, nullable=True)
    costo_guia = db.Column(db.Float, nullable=True)
    costo_transporte = db.Column(db.Float, nullable=True)

    nombres_acompanantes = db.Column(db.Text, nullable=True) # Para múltiples nombres, separados por comas o similar
    recomendaciones = db.Column(db.Text, nullable=True)
    notas_adicionales = db.Column(db.Text, nullable=True)
    
    # Autofecha de creado de nota (fecha de creación del proyecto)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fecha_ultima_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=True)

    def __repr__(self):
        return f"Project('{self.nombre_proyecto}', '{self.propuesta_por}', '{self.fecha_actividad_propuesta}')"

# MODELO Note (existente, con nueva columna)
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=True) # URL de la imagen de la nota
    content = db.Column(db.Text, nullable=True) # Contenido de la nota con formato HTML

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=True)

    # Campo para indicar si la nota es pública
    is_public = db.Column(db.Boolean, default=False, nullable=False)

    # NUEVO CAMPO: Para almacenar el color de fondo de la nota
    background_color = db.Column(db.String(20), default='#FFFFFF', nullable=False) # Valor por defecto blanco

    # Relación con el usuario que crea la nota
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship('User', backref='created_notes', foreign_keys=[creator_id])

    # Relación muchos-a-muchos con usuarios que pueden ver la nota
    # secondary apunta a la tabla de asociación definida arriba
    authorized_viewers = db.relationship(
        'User', secondary=note_viewers, lazy='subquery',
        backref=db.backref('viewable_notes', lazy=True)
    )

    def __repr__(self):
        return f"Note('{self.title}', Creator ID: {self.creator_id}, Public: {self.is_public}, Color: {self.background_color})"

