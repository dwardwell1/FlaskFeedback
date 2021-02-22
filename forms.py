from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(
        min=1, max=20, message="Must be between 1 and 20 characters")])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email(), Length(
        min=1, max=50, message="Must be between 1 and 50 characters")])
    first_name = StringField("First Name", validators=[InputRequired(), Length(
        min=1, max=30, message="Must be between 1 and 30 characters")])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(
        min=1, max=30, message="Must be between 1 and 30 characters")])


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(
        min=1, max=20, message="Must be between 1 and 20 characters")])
    password = PasswordField("Password", validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(
        min=1, max=100, message="Must be between 1 and 100 characters")])
    content = StringField("Content", validators=[InputRequired()])
