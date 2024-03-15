# Import required libraries and modules
import pyrebase
from firebase_admin import db, auth
from flask_recaptcha import ReCaptcha
from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
from auth_forms import RegistrationForm, LoginForm
from firebase_ops import register_user, login_user
import datetime

# Initialize Flask app Blue Print for routes
auth_blueprint = Blueprint('auth', __name__, static_folder='static', template_folder='templates')

# Route for registration page
@auth_blueprint.route('/auth_register', methods=['GET','POST'])
def auth_register():
    form_reg = RegistrationForm()

    if form_reg.validate_on_submit():
        try:
            # call function to register user
            register_user(form_reg)
            return redirect(url_for('home'))
        except Exception as e:
            flash('Registration failed: ' + str(e), 'error')
    else:
        print(form_reg.errors)
        
    return render_template("auth_register.html", form_reg=form_reg)

# Route for login page
@auth_blueprint.route('/auth_login', methods=['GET','POST'])
def auth_login():
    form_log = LoginForm()

    # Print statements for debugging errors
    print(form_log.errors)
    print(form_log.validate_on_submit())
    print(form_log.validate())
    # print(form_log.username.data, form_log.password.data)

    if form_log.validate_on_submit():
        try:
            # call function to login user
            login_user(form_log)
            return redirect(url_for('home'))
        except Exception as e:
            print('Login failed: ' + str(e), 'error')
            return redirect(url_for('auth.auth_login'))


    return render_template("auth_login.html", form_log=form_log)