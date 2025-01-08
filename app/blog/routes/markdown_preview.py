import bleach
import markdown
from flask import render_template, request, jsonify
from flask_login import login_required

from app.authentication.database import is_admin


@login_required
def markdown_preview():
    if not is_admin():
        return render_template("forbidden.html")

    raw_markdown = request.json.get("markdown", "")

    # Convert markdown to HTML using markdown library
    html_content = markdown.markdown(
        raw_markdown, extensions=["fenced_code", "codehilite"]
    )

    # Define a whitelist of allowed tags and attributes for preview
    allowed_tags = [
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
    ]
    allowed_attributes = {
        "a": ["href", "title"],
        "img": ["src", "alt", "title"],
        "code": ["class"],
    }

    # Sanitise the rendered HTML to allow only the defined tags and attributes
    sanitized_html = bleach.clean(
        html_content,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True,  # Remove disallowed tags entirely
    )

    return jsonify({"html": sanitized_html})
