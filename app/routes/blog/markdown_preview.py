import markdown
from flask import render_template, request, jsonify
from flask_login import login_required

from app.database.authentication import is_admin


@login_required
def markdown_preview():
    if not is_admin():
        return render_template("authentication/forbidden.html")

    raw_markdown = request.json.get("markdown", "")
    html_content = markdown.markdown(
        raw_markdown, extensions=["fenced_code", "codehilite"]
    )
    return jsonify({"html": html_content})
