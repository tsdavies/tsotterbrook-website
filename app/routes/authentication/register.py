from flask import flash, redirect, url_for, render_template

from app.database.authentication import register_user
from app.forms import RegisterForm


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
