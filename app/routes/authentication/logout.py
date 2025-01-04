from flask import redirect, url_for, flash
from flask_login import logout_user, login_required


@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
