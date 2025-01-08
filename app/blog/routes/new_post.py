import bleach
import markdown
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
        # Step 1: Sanitise the raw markdown input
        sanitized_markdown = bleach.clean(
            form.content.data,  # Raw markdown
            tags=[],  # Disallow all HTML tags in markdown
            attributes={},  # Disallow all HTML attributes in markdown
            strip=True,  # Strip any disallowed elements entirely
        )

        # Step 2: Sanitise the rendered HTML for preview/display
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

        # Create the new post using sanitized markdown content
        post = BlogPost(
            title=bleach.clean(form.title.data),
            content=sanitized_markdown,  # Store sanitized markdown
            author=current_user.username,
            summary=bleach.clean(form.summary.data),
            repository_url=bleach.clean(form.repository_url.data),
            live_demo_url=bleach.clean(form.live_demo_url.data),
            priority=form.priority.data,  # Assuming priority is numeric and safe.
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
