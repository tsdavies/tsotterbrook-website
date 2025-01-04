from flask import Blueprint
from .routes import (
    blog,
    post_detail,
    markdown_preview,
    new_post,
    edit_post,
    delete_post,
    delete_comment,
)


# Define the Blueprint
blog_bp = Blueprint("blog", __name__, template_folder="templates")

# Register routes with the Blueprint
blog_bp.add_url_rule("/", view_func=blog, endpoint="blog")
blog_bp.add_url_rule("/<int:post_id>", view_func=post_detail, methods=["GET", "POST"])
blog_bp.add_url_rule(
    "/markdown_preview", view_func=markdown_preview, methods=["POST"]
)
blog_bp.add_url_rule("/new", view_func=new_post, methods=["GET", "POST"])
blog_bp.add_url_rule("/<int:post_id>/edit", view_func=edit_post, methods=["GET", "POST"])
blog_bp.add_url_rule(
    "/<int:post_id>/delete", view_func=delete_post, methods=["POST", "GET"]
)
blog_bp.add_url_rule(
    "/comment/<int:comment_id>/delete",
    view_func=delete_comment,
    methods=["POST", "GET"],
)

__all__ = ["blog_bp"]
