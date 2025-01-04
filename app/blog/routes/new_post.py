from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.authentication.database import is_admin
from app.blog.database.models import BlogPost
from app.blog.forms.blog_post_form import BlogPostForm


@login_required
def new_post():
    if not is_admin():
        return render_template("forbidden.html")

    form = BlogPostForm()
    if form.validate_on_submit():
        post = BlogPost(
            title=form.title.data,
            content=form.content.data,
            author=current_user.username,
            summary=form.summary.data,
            repository_url=form.repository_url.data,
            live_demo_url=form.live_demo_url.data,
            priority=form.priority.data,
        )
        db.session.add(post)
        db.session.commit()
        flash("Post created!", "success")
        return redirect(url_for("blog.blog"))
    return render_template(
        "blog_post.html",
        form=form,
        preview_endpoint=url_for("blog.markdown_preview"),
    )
