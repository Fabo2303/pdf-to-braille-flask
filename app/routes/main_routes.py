from flask import Blueprint
from app.controllers.main_controller import index, public, brailletest

main_bp = Blueprint('main', __name__)

main_bp.route('/', methods=['GET'])(index)
main_bp.route('/brailletest', methods=['GET'])(brailletest)
main_bp.route('/public', methods=['GET'])(public)