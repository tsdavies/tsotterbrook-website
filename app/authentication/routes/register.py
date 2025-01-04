from flask import flash, redirect, url_for, render_template

from app.authentication.database import register_user
from app.authentication.forms.register_form import RegisterForm


def register():
    form = RegisterForm()
    if form.validate_on_submit():
        success, message = register_user(
            form.username.data, form.email.data, form.password.data
        )
        flash(message, "success" if success else "danger")
        if success:
            return redirect(url_for("authentication.login"))
    return render_template("register.html", form=form, title="Register")
