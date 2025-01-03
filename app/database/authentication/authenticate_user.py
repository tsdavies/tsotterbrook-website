from flask_login import login_user
from werkzeug.security import check_password_hash

from app.database.authentication.models import User


def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return True, "Login successful!"
    return False, "Invalid email or password"
