from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import TextAreaField, URLField
from wtforms.validators import DataRequired
from wtforms.validators import Optional, URL


class BlogPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    summary = TextAreaField(
        "Summary",
        validators=[DataRequired(message="Please provide a summary for the post.")],
    )
    content = TextAreaField(
        "Content", validators=[DataRequired(message="Content cannot be empty.")]
    )
    repository_url = URLField(
        "Repository URL",
        validators=[Optional(), URL(message="Enter a valid URL")],
    )
    live_demo_url = URLField(
        "Live Demo URL", validators=[Optional(), URL(message="Enter a valid URL")]
    )
    submit = SubmitField("Submit")
