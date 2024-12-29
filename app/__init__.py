from flask import Flask
from app.models import db
from app.routes import init_routes
from app.extensions import mail
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

login_manager = LoginManager()
login_manager.login_view = 'login'  # Redirect unauthenticated users to 'login'


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize database
    db.init_app(app)

    # Initialize LoginManager
    login_manager.init_app(app)

    # Register routes
    init_routes(app)

    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    mail.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # Assuming User model has this setup
        from app.models import User  # Import User model here
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)

    return app
