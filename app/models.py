from flask_login import logout_user, login_user, login_required, current_user
from app.pokemon_utils import pokemon_color
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegisterForm, BlogPostForm, CommentForm
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    @property
    def is_authenticated(self):
        return True


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String(50), nullable=False)
    summary = db.Column(db.String(255), nullable=True)
    repository_url = db.Column(db.String(255), nullable=True)
    live_demo_url = db.Column(db.String(255), nullable=True)
    comments = db.relationship(
        'Comment', backref='post', cascade="all, delete-orphan", lazy=True
    )


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'blog_post.id'), nullable=False)
