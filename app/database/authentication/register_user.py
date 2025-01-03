from werkzeug.security import generate_password_hash

from app.database.authentication.models import User


def register_user(username, email, password):
    if User.query.filter_by(email=email).first():
        return False, "Email already registered"
    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return True, "Registration successful! You can now log in."
