from flask import Flask
from app.models import db
from app.routes import init_routes
from app.extensions import mail
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize database
    db.init_app(app)

    # Register routes
    init_routes(app)

    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    mail.init_app(app)

    return app
