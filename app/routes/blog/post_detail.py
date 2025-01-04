import markdown
from flask import flash, redirect, url_for, render_template
from flask_login import current_user
from markupsafe import Markup

from app import db
from app.database.blog.models import BlogPost, Comment
from app.forms import CommentForm


def post_detail(post_id):
    post = BlogPost.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        try:
            comment = Comment(
                content=form.content.data,
                author=current_user.username,
                post_id=post.id,
            )
            db.session.add(comment)
            db.session.commit()
            flash("Comment added!", "success")
            return redirect(url_for("blog.post_detail", post_id=post_id))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while adding your comment.", "danger")

    comments = (
        Comment.query.filter_by(post_id=post.id)
        .order_by(Comment.timestamp.desc())
        .all()
    )
    rendered_content = Markup(
        markdown.markdown(post.content, extensions=["fenced_code", "codehilite"])
    )

    return render_template(
        "blog/blog_post_detail.html",
        post=post,
        content=rendered_content,
        form=form,
        comments=comments,
    )
