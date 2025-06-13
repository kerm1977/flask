from flask import Blueprint, render_template, session, redirect, url_for, flash, current_app
from models import db, User # Importa db y User de models.py

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

@contactos_bp.route('/ver_detalle/<int:user_id>')
def ver_detalle(user_id):
    if 'logged_in' not in session or not session['logged_in']:
        flash('Por favor, inicia sesión para acceder a esta página.', 'info')
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id) # Busca el usuario por ID, o devuelve 404 si no lo encuentra

    # Si hay un avatar_url, construimos la URL estática
    avatar_url = None
    if user.avatar_url:
        # Usamos current_app para acceder a la configuración de la app en un blueprint
        # Esto es necesario porque url_for('static') requiere el contexto de la aplicación
        with current_app.app_context():
            avatar_url = url_for('static', filename=user.avatar_url)
    else:
        with current_app.app_context():
            avatar_url = url_for('static', filename='images/defaults/default_avatar.png')

    return render_template('detalle_contactos.html', user=user, avatar_url=avatar_url)