from flask_mail import Mail
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

mail = Mail()
login_manager = LoginManager()
migrate = Migrate()
db = SQLAlchemy()
