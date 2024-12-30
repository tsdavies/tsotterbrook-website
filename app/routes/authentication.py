from flask import render_template, redirect, url_for, flash

from app.routes.authentication_helper import is_admin
from app.models.user import db, User
from app.forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import logout_user, login_user, login_required


def register_authentication_routes(app):

    @app.context_processor
    def inject_user_utils():
        return dict(is_admin=is_admin)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Login successful!", "success")
                return redirect(url_for("about"))
            else:
                flash("Invalid email or password", "danger")
        return render_template("authentication/login.html", form=form, title="Login")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first():
                flash("Email already registered", "danger")
                return redirect(url_for("register"))
            hashed_password = generate_password_hash(
                form.password.data, method="pbkdf2:sha256"
            )
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("login"))
        return render_template(
            "authentication/register.html", form=form, title="Register"
        )

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out.", "success")
        return redirect(url_for("login"))
