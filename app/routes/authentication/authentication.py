from flask import render_template, redirect, url_for, flash
from flask_login import logout_user, login_required
from app.forms import LoginForm, RegisterForm
from app.database.authentication.authenticate_user import authenticate_user
from app.database.authentication.register_user import register_user


def login():
    form = LoginForm()
    if form.validate_on_submit():
        success, message = authenticate_user(form.email.data, form.password.data)
        flash(message, "success" if success else "danger")
        if success:
            return redirect(url_for("about"))
    return render_template("authentication/login.html", form=form, title="Login")

def register():
    form = RegisterForm()
    if form.validate_on_submit():
        success, message = register_user(
            form.username.data, form.email.data, form.password.data
        )
        flash(message, "success" if success else "danger")
        if success:
            return redirect(url_for("auth.login"))
    return render_template("authentication/register.html", form=form, title="Register")

@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
