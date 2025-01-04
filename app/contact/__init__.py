from flask import Blueprint
from .routes import contact

# Define the blueprint
contact_bp = Blueprint("contact", __name__, template_folder="templates")

# Add the route
contact_bp.add_url_rule("/", view_func=contact, methods=["GET", "POST"])
