from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import DataRequired, Optional, URL, Regexp
from wtforms import StringField, TextAreaField, URLField, SubmitField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    submit = SubmitField("Register")


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
        validators=[
            Optional(),
            URL(message="Enter a valid URL"),
            Regexp(
                r"^(https:\/\/github\.com\/|https:\/\/gitlab\.com\/)",
                message="Must be a valid GitHub or GitLab URL",
            ),
        ],
    )
    live_demo_url = URLField(
        "Live Demo URL", validators=[Optional(), URL(message="Enter a valid URL")]
    )
    submit = SubmitField("Submit")


class CommentForm(FlaskForm):
    content = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit")
