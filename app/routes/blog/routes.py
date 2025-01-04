import markdown
from markupsafe import Markup
from flask import render_template, request, redirect, url_for, flash, jsonify

from app.database.authentication import is_admin
from app.extensions import db

from app.database.blog.models import BlogPost, Comment
from app.forms import BlogPostForm, CommentForm

from flask_login import login_required, current_user


def blog():
    posts = BlogPost.query.order_by(BlogPost.timestamp.desc()).all()
    return render_template("blog/blogs.html", posts=posts)


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


@login_required
def markdown_preview():
    if not is_admin():
        return render_template("authentication/forbidden.html")

    raw_markdown = request.json.get("markdown", "")
    html_content = markdown.markdown(
        raw_markdown, extensions=["fenced_code", "codehilite"]
    )
    return jsonify({"html": html_content})


@login_required
def new_post():
    if not is_admin():
        return render_template("authentication/forbidden.html")

    form = BlogPostForm()
    if form.validate_on_submit():
        post = BlogPost(
            title=form.title.data,
            content=form.content.data,
            author=current_user.username,
            summary=form.summary.data,
            repository_url=form.repository_url.data,
            live_demo_url=form.live_demo_url.data,
        )
        db.session.add(post)
        db.session.commit()
        flash("Post created!", "success")
        return redirect(url_for("blog.blog"))
    return render_template(
        "blog/blog_post.html",
        form=form,
        preview_endpoint=url_for("blog.markdown_preview"),
    )


@login_required
def edit_post(post_id):
    if not is_admin():
        return render_template("authentication/forbidden.html")
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
        "blog/blog_post.html",
        form=form,
        post=post,
        edit=True,
        preview_endpoint=url_for("blog.markdown_preview"),
    )


@login_required
def delete_post(post_id):
    if not is_admin():
        return render_template("authentication/forbidden.html")
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully!", "success")
    return redirect(url_for("blog.blog"))


@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user.username and not is_admin():
        flash("You do not have permission to delete this comment.", "danger")
        return redirect(request.referrer or url_for("blog.blog"))
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted successfully!", "success")
    return redirect(request.referrer or url_for("blog.blog"))
