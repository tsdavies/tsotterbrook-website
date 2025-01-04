from flask import Blueprint, render_template

# Define the blueprint
about_bp = Blueprint('about', __name__, template_folder='../templates')

@about_bp.route("/")
@about_bp.route("/about")
def about():
    return render_template("about.html", title="About Me")
