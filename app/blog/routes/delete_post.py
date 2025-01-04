from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from app import db
from app.authentication.database import is_admin
from ..database.models import BlogPost


@login_required
def delete_post(post_id):
    if not is_admin():
        return render_template("forbidden.html")
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully!", "success")
    return redirect(url_for("blog.blog"))
