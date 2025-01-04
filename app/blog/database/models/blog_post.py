from datetime import datetime

from app.extensions import db


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    priority = db.Column(db.Integer, default=0)
    author = db.Column(db.String(50), nullable=False)
    summary = db.Column(db.String(255), nullable=True)
    repository_url = db.Column(db.String(255), nullable=True)
    live_demo_url = db.Column(db.String(255), nullable=True)
    comments = db.relationship(
        "Comment", backref="post", cascade="all, delete-orphan", lazy=True
    )
