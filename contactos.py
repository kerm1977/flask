from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import db, User # ¡CAMBIO AQUÍ! Importa de models.py

# Creamos un Blueprint para organizar las rutas relacionadas con contactos
contactos_bp = Blueprint('contactos', __name__, url_prefix='/contactos')

@contactos_bp.route('/ver_contactos')
def ver_contactos():
    if 'logged_in' not in session or not session['logged_in']:
        flash('Por favor, inicia sesión para acceder a esta página.', 'info')
        return redirect(url_for('login'))

    try:
        all_users = User.query.all()
        return render_template('ver_contactos.html', users=all_users)
    except Exception as e:
        flash(f'Error al cargar los contactos: {e}', 'danger')
        return redirect(url_for('home'))