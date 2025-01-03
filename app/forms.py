from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import TextAreaField, URLField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.validators import Optional, URL


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
        validators=[Optional(), URL(message="Enter a valid URL")],
    )
    live_demo_url = URLField(
        "Live Demo URL", validators=[Optional(), URL(message="Enter a valid URL")]
    )
    submit = SubmitField("Submit")


class CommentForm(FlaskForm):
    content = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit")
