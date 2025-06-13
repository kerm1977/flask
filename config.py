# config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'tu_clave_secreta_aqui'  # Cambia esto por una clave segura
    # La base de datos ahora se llamará 'db.db' y estará en la raíz de tu proyecto
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.db') # CAMBIO AQUÍ: 'site.db' a 'db.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False