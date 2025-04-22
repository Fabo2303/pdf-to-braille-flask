import os
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.models.user_session import UserSession
from app.extensions import db


def list_braille_files():
    """
    Lista los archivos disponibles en la carpeta uploads/braille
    """
    braille_folder = os.path.join('uploads', 'braille')

    try:
        files = os.listdir(braille_folder)
        braille_files = [f for f in files if os.path.isfile(os.path.join(braille_folder, f))]
        return jsonify({'files': braille_files}), 200

    except FileNotFoundError:
        return jsonify({'error': 'Directorio no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def read_braille():
    user_id = get_jwt_identity()

    data = request.get_json()
    title = data.get('title')
    chunk_size = int(data.get('chunk_size', 1))

    if not title:
        return jsonify({"error": "Se requiere el campo 'title'"}), 400

    file_path = os.path.join('uploads', 'braille', title)

    if not os.path.exists(file_path):
        return jsonify({"error": f"No se encontró el archivo '{title}'"}), 404

    # Leer el archivo completo
    with open(file_path, 'r', encoding='utf-8') as f:
        braille_data = f.read().strip().split()

    # Buscar o crear la sesión del usuario
    session = UserSession.query.filter_by(user_id=user_id, title=title).first()
    if not session:
        session = UserSession(user_id=user_id, title=title, last_character=0)
        db.session.add(session)

    start = session.last_character
    end = min(start + chunk_size, len(braille_data))
    chunk = braille_data[start:end]

    # Actualizar el progreso del usuario
    session.last_character = end
    db.session.commit()

    return jsonify({
        "title": title,
        "start": start,
        "end": end,
        "chunk": chunk,
        "done": end >= len(braille_data)
    })