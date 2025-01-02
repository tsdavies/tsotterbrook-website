from app.routes.contact import register_contact_routes
from app.routes.about import register_about_routes
from app.routes.authentication import register_authentication_routes
from app.routes.blog import register_blog_routes
from app.routes.pokemon import register_pokemon_routes


def register_routes(app):
    register_authentication_routes(app)
    register_pokemon_routes(app)
    register_about_routes(app)
    register_blog_routes(app)
    register_contact_routes(app)
