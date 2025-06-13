from flask import Blueprint, render_template, session, redirect, url_for, flash, current_app, request
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
        with current_app.app_context():
            avatar_url = url_for('static', filename=user.avatar_url)
    else:
        with current_app.app_context():
            avatar_url = url_for('static', filename='images/defaults/default_avatar.png')

    return render_template('detalle_contactos.html', user=user, avatar_url=avatar_url)

@contactos_bp.route('/eliminar_contacto/<int:user_id>', methods=['POST'])
def eliminar_contacto(user_id):
    if 'logged_in' not in session or not session['logged_in']:
        flash('Por favor, inicia sesión para realizar esta acción.', 'info')
        return redirect(url_for('login'))

    user_to_delete = User.query.get_or_404(user_id)

    # Opcional: Para evitar que un usuario se autoelimine o para control de roles
    # if user_to_delete.username == session['username']:
    #     flash('No puedes eliminar tu propia cuenta desde aquí.', 'warning')
    #     return redirect(url_for('contactos.ver_detalle', user_id=user_id))

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash(f'El usuario "{user_to_delete.username}" ha sido eliminado exitosamente.', 'success')
        return redirect(url_for('contactos.ver_contactos')) # Redirige a la lista de contactos
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el usuario: {e}', 'danger')
        return redirect(url_for('contactos.ver_detalle', user_id=user_id))