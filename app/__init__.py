from flask import Flask, render_template

from app.authentication.database import is_admin
from app.extensions import mail, login_manager, migrate, db
from app.routes import register_routes
from datetime import datetime
from flask_login import current_user
from markdown import markdown


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialise extensions
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Register custom template filter
    @app.template_filter("format_datetime")
    def format_datetime(value, format="%d %b %Y, %H:%M"):
        """Custom filter to format datetime objects."""
        return value.strftime(format) if isinstance(value, datetime) else value

    @app.template_filter("markdown")
    def markdown_filter(content):
        """Convert Markdown content to HTML."""
        return markdown(content)

    # Register all routes
    register_routes(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    # Configure Flask-Login user loader
    @login_manager.user_loader
    def load_user(user_id):
        from app.authentication.database.models import User

        return User.query.get(int(user_id))

    # Inject current_user into templates
    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)

    @app.context_processor
    def inject_user_utils():
        return dict(is_admin=is_admin)

    return app
