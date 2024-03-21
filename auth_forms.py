# Import necessary modules
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# Registration Form
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    location = StringField('Street Address', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    # recaptcha = RecaptchaField()

# Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    recaptcha = RecaptchaField()

class VerifyForm(FlaskForm):
    otp = StringField('OTP', validators=[DataRequired()])