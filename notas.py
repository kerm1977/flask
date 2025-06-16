from flask import Blueprint, render_template, session, redirect, url_for, flash, current_app, request, send_file, abort
from models import db, Note, User # Importa db, Note y User de models.py
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import io # Para manejar archivos en memoria
from sqlalchemy import or_

# Carpeta donde se guardarán las imágenes de las notas (relativa a 'static')
NOTE_IMAGE_UPLOAD_FOLDER_RELATIVE = os.path.join('uploads', 'note_images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """
    Verifica si la extensión del archivo está permitida.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Creamos un Blueprint para organizar las rutas relacionadas con notas
notas_bp = Blueprint('notas', __name__, url_prefix='/notas')

@notas_bp.route('/crear_nota', methods=['GET', 'POST'])
def crear_nota():
    """
    Muestra y procesa el formulario para crear una nueva nota.
    Requiere que el usuario esté logueado.
    """
    if 'logged_in' not in session or not session['logged_in']:
        flash('Por favor, inicia sesión para crear notas.', 'info')
        return redirect(url_for('login'))

    current_user_id = session.get('user_id')
    if not current_user_id:
        flash('No se pudo identificar al usuario actual.', 'danger')
        return redirect(url_for('login'))

    # Obtener todos los usuarios para el multiselector de "quién puede ver la nota"
    all_users = User.query.all()
    
    if request.method == 'POST':
        try:
            title = request.form['title']
            # El contenido del editor de texto enriquecido se recibirá como HTML
            content = request.form.get('content') 
            
            # NUEVO: Obtener el estado de is_public del formulario
            is_public = 'is_public' in request.form # Si el checkbox está marcado, estará en request.form
            
            # Manejo de la imagen de la nota
            image_url = None
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"{current_user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                    # Asegurarse de que la carpeta exista
                    upload_folder = os.path.join(current_app.root_path, 'static', NOTE_IMAGE_UPLOAD_FOLDER_RELATIVE)
                    os.makedirs(upload_folder, exist_ok=True)
                    file_path = os.path.join(upload_folder, filename)
                    file.save(file_path)
                    image_url = os.path.join(NOTE_IMAGE_UPLOAD_FOLDER_RELATIVE, filename).replace('\\', '/')
            
            # Obtener los IDs de los usuarios seleccionados para ver la nota
            # request.form.getlist() se usa para select múltiple
            authorized_viewer_ids = request.form.getlist('authorized_viewers')
            authorized_viewers = []
            for user_id in authorized_viewer_ids:
                user = User.query.get(int(user_id))
                if user:
                    authorized_viewers.append(user)
            
            # Añadir al propio creador si no está ya en la lista de viewers
            creator_user = User.query.get(current_user_id)
            if creator_user and creator_user not in authorized_viewers:
                authorized_viewers.append(creator_user)


            new_note = Note(
                title=title,
                image_url=image_url,
                content=content,
                creator_id=current_user_id, # Asigna el ID del usuario logueado como creador
                is_public=is_public # NUEVO: Asigna el estado público
            )
            
            # Asigna los usuarios autorizados
            new_note.authorized_viewers = authorized_viewers

            db.session.add(new_note)
            db.session.commit()
            flash('¡Nota creada exitosamente!', 'success')
            return redirect(url_for('notas.ver_notas'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la nota: {e}', 'danger')
            current_app.logger.error(f"Error creating note: {e}") # Log the error
            return render_template('crear_nota.html', all_users=all_users)

    return render_template('crear_nota.html', all_users=all_users)

@notas_bp.route('/ver_notas')
def ver_notas():
    """
    Muestra una lista de notas. Solo las notas que el usuario actual puede ver o son públicas.
    Requiere que el usuario esté logueado.
    """
    if 'logged_in' not in session or not session['logged_in']:
        flash('Por favor, inicia sesión para ver las notas.', 'info')
        return redirect(url_for('login'))

    current_user_id = session.get('user_id')
    if not current_user_id:
        flash('No se pudo identificar al usuario actual.', 'danger')
        return redirect(url_for('login'))

    try:
        # Obtener las notas que el usuario actual puede ver:
        # 1. Notas creadas por el usuario actual.
        # 2. Notas donde el usuario actual es un visor autorizado.
        # 3. NUEVO: Notas que están marcadas como is_public=True.
        all_notes = db.session.query(Note).filter(
            or_(
                Note.creator_id == current_user_id,
                Note.authorized_viewers.any(User.id == current_user_id),
                Note.is_public == True # Incluir notas públicas
            )
        ).order_by(Note.created_at.desc()).all()

        return render_template('ver_notas.html', notes=all_notes)
    except Exception as e:
        flash(f'Error al cargar las notas: {e}', 'danger')
        current_app.logger.error(f"Error loading notes for user {current_user_id}: {e}")
        return redirect(url_for('home'))


@notas_bp.route('/detalle_nota/<int:note_id>')
def detalle_nota(note_id):
    """
    Muestra los detalles completos de una nota específica.
    Solo accesible si el usuario actual es el creador, un visor autorizado, o si la nota es pública.
    """
    if 'logged_in' not in session or not session['logged_in']:
        flash('Por favor, inicia sesión para acceder a esta página.', 'info')
        return redirect(url_for('login'))

    current_user_id = session.get('user_id')
    if not current_user_id:
        flash('No se pudo identificar al usuario actual.', 'danger')
        return redirect(url_for('login'))

    note = Note.query.get_or_404(note_id)

    # Verificar si el usuario actual está autorizado para ver la nota
    # O si la nota es pública
    is_authorized = (note.creator_id == current_user_id) or \
                    any(user.id == current_user_id for user in note.authorized_viewers) or \
                    note.is_public # NUEVO: Si la nota es pública, cualquier logueado puede verla
    
    if not is_authorized:
        flash('No tienes permiso para ver esta nota.', 'danger')
        abort(403) # Prohibido

    # Si hay una imagen, construye la URL estática
    image_url = None
    if note.image_url:
        with current_app.app_context():
            image_url = url_for('static', filename=note.image_url)
    
    return render_template('detalle_nota.html', note=note, image_url=image_url, is_authorized=is_authorized)


@notas_bp.route('/editar_nota/<int:note_id>', methods=['GET', 'POST'])
def editar_nota(note_id):
    """
    Muestra y procesa el formulario para editar una nota.
    Solo accesible si el usuario actual es el creador de la nota.
    """
    if 'logged_in' not in session or not session['logged_in']:
        flash('Por favor, inicia sesión para editar notas.', 'info')
        return redirect(url_for('login'))

    current_user_id = session.get('user_id')
    if not current_user_id:
        flash('No se pudo identificar al usuario actual.', 'danger')
        return redirect(url_for('login'))

    note = Note.query.get_or_404(note_id)

    # Solo el creador puede editar la nota
    if note.creator_id != current_user_id:
        flash('No tienes permiso para editar esta nota.', 'danger')
        abort(403) # Prohibido

    all_users = User.query.all() # Para el multiselector

    if request.method == 'POST':
        try:
            note.title = request.form['title']
            note.content = request.form.get('content')
            
            # NUEVO: Actualizar el estado de is_public
            note.is_public = 'is_public' in request.form
            
            # Manejo de la imagen
            if 'image' in request.files:
                file = request.files['image']
                if file.filename != '' and allowed_file(file.filename):
                    # Eliminar la imagen anterior si existe
                    if note.image_url:
                        upload_folder = os.path.join(current_app.root_path, 'static', NOTE_IMAGE_UPLOAD_FOLDER_RELATIVE)
                        old_image_path = os.path.join(upload_folder, os.path.basename(note.image_url))
                        if os.path.exists(old_image_path):
                            os.unlink(old_image_path)
                    
                    filename = secure_filename(f"{current_user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                    upload_folder = os.path.join(current_app.root_path, 'static', NOTE_IMAGE_UPLOAD_FOLDER_RELATIVE)
                    os.makedirs(upload_folder, exist_ok=True) # Asegurarse de que la carpeta exista
                    file_path = os.path.join(upload_folder, filename)
                    file.save(file_path)
                    note.image_url = os.path.join(NOTE_IMAGE_UPLOAD_FOLDER_RELATIVE, filename).replace('\\', '/')
                elif file.filename == '' and request.form.get('clear_image'): # Si se marca la casilla para borrar
                    if note.image_url:
                        upload_folder = os.path.join(current_app.root_path, 'static', NOTE_IMAGE_UPLOAD_FOLDER_RELATIVE)
                        old_image_path = os.path.join(upload_folder, os.path.basename(note.image_url))
                        if os.path.exists(old_image_path):
                            os.unlink(old_image_path)
                        note.image_url = None # Borrar la URL de la DB
            
            # Actualizar usuarios autorizados
            selected_viewer_ids = request.form.getlist('authorized_viewers')
            new_authorized_viewers = []
            for user_id in selected_viewer_ids:
                user = User.query.get(int(user_id))
                if user:
                    new_authorized_viewers.append(user)
            
            # Asegurarse de que el creador siempre esté en la lista de authorized_viewers
            creator_user = User.query.get(current_user_id)
            if creator_user and creator_user not in new_authorized_viewers:
                new_authorized_viewers.append(creator_user)

            note.authorized_viewers = new_authorized_viewers

            note.updated_at = datetime.utcnow() # Actualiza la fecha de edición

            db.session.commit()
            flash('¡Nota actualizada exitosamente!', 'success')
            return redirect(url_for('notas.detalle_nota', note_id=note.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la nota: {e}', 'danger')
            current_app.logger.error(f"Error updating note {note_id}: {e}")
            return render_template('editar_nota.html', note=note, all_users=all_users)

    # Si es GET request
    image_url = None
    if note.image_url:
        with current_app.app_context():
            image_url = url_for('static', filename=note.image_url)

    # Obtener los IDs de los usuarios autorizados actualmente para precargar el multiselector
    current_authorized_viewer_ids = [user.id for user in note.authorized_viewers]

    return render_template('editar_nota.html', note=note, image_url=image_url, 
                           all_users=all_users, 
                           current_authorized_viewer_ids=current_authorized_viewer_ids)

@notas_bp.route('/eliminar_nota/<int:note_id>', methods=['POST'])
def eliminar_nota(note_id):
    """
    Elimina una nota de la base de datos.
    Solo el creador de la nota puede eliminarla.
    """
    if 'logged_in' not in session or not session['logged_in']:
        flash('Por favor, inicia sesión para realizar esta acción.', 'info')
        return redirect(url_for('login'))

    current_user_id = session.get('user_id')
    if not current_user_id:
        flash('No se pudo identificar al usuario actual.', 'danger')
        return redirect(url_for('login'))

    note_to_delete = Note.query.get_or_404(note_id)

    # Solo el creador puede eliminar la nota
    if note_to_delete.creator_id != current_user_id:
        flash('No tienes permiso para eliminar esta nota.', 'danger')
        abort(403) # Prohibido

    try:
        # Eliminar el archivo de imagen de la nota si existe
        if note_to_delete.image_url:
            upload_folder = os.path.join(current_app.root_path, 'static', NOTE_IMAGE_UPLOAD_FOLDER_RELATIVE)
            file_path = os.path.join(upload_folder, os.path.basename(note_to_delete.image_url))
            if os.path.exists(file_path):
                os.unlink(file_path)

        db.session.delete(note_to_delete)
        db.session.commit()
        flash(f'La nota "{note_to_delete.title}" ha sido eliminada exitosamente.', 'success')
        return redirect(url_for('notas.ver_notas'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la nota: {e}', 'danger')
        current_app.logger.error(f"Error deleting note {note_id}: {e}")
        return redirect(url_for('notas.detalle_nota', note_id=note_id))

# --- Rutas de Exportación para Notas ---

@notas_bp.route('/exportar_nota_txt/<int:note_id>')
def exportar_nota_txt(note_id):
    """
    Exporta el contenido de una nota individual a un archivo de texto plano (.txt).
    """
    if 'logged_in' not in session or not session['logged_in']:
        flash('Por favor, inicia sesión para exportar notas.', 'info')
        return redirect(url_for('login'))
    
    current_user_id = session.get('user_id')
    note = Note.query.get_or_404(note_id)

    # Verificar autorización para exportar: creador, visor autorizado o nota pública
    is_authorized = (note.creator_id == current_user_id) or \
                    any(user.id == current_user_id for user in note.authorized_viewers) or \
                    note.is_public
    
    if not is_authorized:
        flash('No tienes permiso para exportar esta nota.', 'danger')
        abort(403) # Prohibido

    # Para TXT, stripteamos el HTML para obtener texto plano
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(note.content if note.content else '', 'html.parser')
    plain_content = soup.get_text(separator='\n', strip=True)

    content = f"""
Título de la Nota: {note.title}
--------------------------------------------------
Creado por: {note.creator.nombre} {note.creator.primer_apellido} ({note.creator.username})
Fecha de Creación: {note.created_at.strftime('%d/%m/%Y %H:%M:%S')}
Última Actualización: {note.updated_at.strftime('%d/%m/%Y %H:%M:%S') if note.updated_at else 'N/A'}
Nota Pública: {'Sí' if note.is_public else 'No'}

Contenido:
{plain_content}

Usuarios Autorizados para Ver:
"""
    if note.is_public:
        content += "- Esta nota es pública y puede ser vista por todos los usuarios logueados.\n"
    elif note.authorized_viewers:
        for viewer in note.authorized_viewers:
            content += f"- {viewer.nombre} {viewer.primer_apellido} ({viewer.username})\n"
    else:
        content += "- Ninguno (solo el creador)\n"

    buffer = io.BytesIO(content.encode('utf-8'))

    return send_file(
        buffer,
        mimetype='text/plain',
        as_attachment=True,
        download_name=f'{note.title.replace(" ", "_")}.txt'
    )

@notas_bp.route('/exportar_nota_jpg/<int:note_id>')
def exportar_nota_jpg(note_id):
    """
    Simula la exportación de la nota a JPG. 
    Dado que la conversión de HTML a JPG en el servidor es compleja,
    se recomienda al usuario tomar una captura de pantalla.
    """
    if 'logged_in' not in session or not session['logged_in']:
        flash('Por favor, inicia sesión para exportar notas.', 'info')
        return redirect(url_for('login'))
    
    current_user_id = session.get('user_id')
    note = Note.query.get_or_404(note_id)

    # Verificar autorización para exportar: creador, visor autorizado o nota pública
    is_authorized = (note.creator_id == current_user_id) or \
                    any(user.id == current_user_id for user in note.authorized_viewers) or \
                    note.is_public
    
    if not is_authorized:
        flash('No tienes permiso para exportar esta nota.', 'danger')
        abort(403) # Prohibido

    flash("La exportación a JPG no está disponible directamente desde el servidor. Por favor, utiliza la función de captura de pantalla de tu dispositivo para obtener una imagen de la nota.", "info")
    return redirect(url_for('notas.detalle_nota', note_id=note_id))

