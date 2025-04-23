from flask import Flask
from .extensions import db, jwt
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')

    db.init_app(app)
    jwt.init_app(app)

    from .routes.pdf_routes import pdf_bp
    from .routes.auth_routes import auth_bp
    from .routes.file_routes import braille_bp
    from .routes.main_routes import main_bp

    app.register_blueprint(pdf_bp, url_prefix='/api/pdf')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(braille_bp, url_prefix='/api/braille')
    app.register_blueprint(main_bp)

    return app
