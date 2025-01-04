from flask import flash, redirect, url_for, render_template

from app.authentication.database import authenticate_user
from app.forms import LoginForm


def login():
    form = LoginForm()
    if form.validate_on_submit():
        success, message = authenticate_user(form.email.data, form.password.data)
        flash(message, "success" if success else "danger")
        if success:
            return redirect(url_for("about"))
    return render_template("login.html", form=form, title="Login")
