from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FloatField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Optional
from wtforms.widgets import TextArea



# WEB FORMS
# CREATE LOGIN FORM
class LoginForm(FlaskForm):
    username_email = StringField("Userame/Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    login = SubmitField("LOGIN")


# CREATE USER FORM
class UserForm(FlaskForm):
    name = StringField("Full name", validators=[DataRequired()])
    username = StringField("Userame", validators=[DataRequired()])
    email = StringField("Email address", validators=[DataRequired()])

    role = SelectField(
        "Role",
        choices=[("dashboard_user", "Dashboard User"), ("admin", "Admin")]
    )
    
    password_hash = PasswordField(
        "Password",
        validators=[Optional(), EqualTo('password_hash2', message="Password Doesn't Match!")]
    )
    password_hash2 = PasswordField(
        "Confirm Password",
        validators=[Optional()]
    )
    
    create = SubmitField("REGISTER")
    update = SubmitField("UPDATE")

# CREATE PASSWORD RESET FORM
class PasswordForm(FlaskForm):
    reset_password_hash = PasswordField("Password (Change)", validators=[DataRequired(), EqualTo('reset_password_hash2', message="Password Doesn't Match!")])
    reset_password_hash2 = PasswordField("Password (Confirm Change)", validators=[DataRequired()])
    reset = SubmitField("RESET")
