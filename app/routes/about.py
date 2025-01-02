from datetime import datetime
from flask import render_template


def register_about_routes(app):

    @app.route("/")
    @app.route("/about")
    def about():
        return render_template("about.html", title="About Me")
