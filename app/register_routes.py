from app.about import about_bp
from app.blog import blog_bp
from app.contact import contact_bp
from app.pokemon import pokemon_bp
from app.authentication import auth_bp


def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/authentication")
    app.register_blueprint(pokemon_bp, url_prefix="/pokemon")
    app.register_blueprint(blog_bp, url_prefix="/blog")
    app.register_blueprint(about_bp, url_prefix="/")
    app.register_blueprint(contact_bp, url_prefix="/contact")
