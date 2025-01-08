import bleach
import markdown
from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from app import db
from app.authentication.database import is_admin
from app.blog.forms.blog_post_form import BlogPostForm
from ..database.models import BlogPost


@login_required
def edit_post(post_id):
    if not is_admin():
        return render_template("forbidden.html")
    post = BlogPost.query.get_or_404(post_id)
    form = BlogPostForm(obj=post)

    if form.validate_on_submit():
        # Sanitise input fields
        post.title = bleach.clean(form.title.data)

        sanitized_markdown = bleach.clean(
            form.content.data,  # Raw markdown
            tags=[],  # Disallow all HTML tags in markdown
            attributes={},  # Disallow all HTML attributes in markdown
            strip=True,  # Strip any disallowed elements entirely
        )
        post.content = sanitized_markdown

        rendered_html = bleach.clean(
            markdown.markdown(
                sanitized_markdown, extensions=["fenced_code", "codehilite"]
            ),
            tags=[
                "p",
                "b",
                "i",
                "u",
                "em",
                "strong",
                "a",
                "ul",
                "ol",
                "li",
                "code",
                "pre",
                "blockquote",
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
                "img",
                "br",
                "hr",
            ],
            attributes={
                "a": ["href", "title"],
                "img": ["src", "alt", "title"],
                "code": ["class"],
            },
            strip=True,  # Strip disallowed tags and attributes
        )

        # Sanitise other fields
        post.summary = bleach.clean(form.summary.data)
        post.repository_url = bleach.clean(form.repository_url.data)
        post.live_demo_url = bleach.clean(form.live_demo_url.data)
        post.priority = form.priority.data  # Assuming priority is numeric and safe.

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
