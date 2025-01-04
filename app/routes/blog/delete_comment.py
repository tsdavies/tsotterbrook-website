from flask import flash, redirect, request, url_for
from flask_login import login_required, current_user

from app import db
from app.database.authentication import is_admin
from app.database.blog.models import Comment


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
