from flask import Blueprint
from app.controllers.file_controller import list_braille_files, read_braille
from flask_jwt_extended import jwt_required

braille_bp = Blueprint('braille', __name__)

braille_bp.route('/files', methods=['GET'])(list_braille_files)

read_braille = jwt_required()(read_braille)
braille_bp.add_url_rule('/read', view_func=read_braille, methods=['POST'])
