from flask import render_template

from app.database.blog.models import BlogPost


def blog():
    posts = BlogPost.query.order_by(BlogPost.timestamp.desc()).all()
    return render_template("blog/blogs.html", posts=posts)


