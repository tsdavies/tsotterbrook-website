from flask import render_template

from ..database.models import BlogPost


def blog():
    posts = BlogPost.query.order_by(BlogPost.timestamp.desc()).all()
    return render_template("blogs.html", posts=posts)
