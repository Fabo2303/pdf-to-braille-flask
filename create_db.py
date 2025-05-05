from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.user_session import UserSession

app = create_app()

with app.app_context():
    # Crea todas las tablas, incluida la tabla 'user'
    db.create_all()

    # Añadir un usuario inicial para pruebas (opcional)
    if not User.query.filter_by(username='admin').first():
        user = User(username='admin')
        user.set_password('123456')
        user.set_role('profesor')
        db.session.add(user)
        db.session.commit()

    print("Base de datos y tablas creadas con éxito.")
