from app.routes.contact import register_contact_routes
from app.routes.about import register_about_routes
from app.routes.blog import register_blog_routes
from app.routes.pokemon import register_pokemon_routes

from app.routes.authentication import auth_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    register_pokemon_routes(app)
    register_about_routes(app)
    register_blog_routes(app)
    register_contact_routes(app)
