from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from app import db
from app.authentication.database import is_admin
from ..database.models import BlogPost
from app.forms import BlogPostForm


@login_required
def edit_post(post_id):
    if not is_admin():
        return render_template("forbidden.html")
    post = BlogPost.query.get_or_404(post_id)
    form = BlogPostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.summary = form.summary.data
        post.repository_url = form.repository_url.data
        post.live_demo_url = form.live_demo_url.data
        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for("blog.post_detail", post_id=post.id))
    return render_template(
        "blog_post.html",
        form=form,
        post=post,
        edit=True,
        preview_endpoint=url_for("blog.markdown_preview"),
    )
