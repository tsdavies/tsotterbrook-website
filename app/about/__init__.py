from flask import Blueprint
from .routes.about import about

about_bp = Blueprint("about", __name__, template_folder="templates")
about_bp.add_url_rule("/", view_func=about, methods=["GET", "POST"])
about_bp.add_url_rule("/about", view_func=about, methods=["GET", "POST"])


__all__ = ["about_bp"]
