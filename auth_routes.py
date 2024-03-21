# Import required libraries and modules
import pyrebase
from firebase_admin import db, auth
from flask_recaptcha import ReCaptcha
from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
from auth_forms import RegistrationForm, LoginForm, VerifyForm
from firebase_ops import register_user, login_user, sendOTP, verify_user, delete_otp
import datetime
import threading
from firebase_admin.auth import UserNotFoundError
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
            return redirect(url_for('auth.auth_verify'))
        except Exception as e:
            print("Registration failed at auth_register:", e)
            flash('Registration failed: ' + str(e), 'error')
    else:
        print(form_reg.errors)

    return render_template("auth_register.html", form_reg=form_reg)

@auth_blueprint.route('/auth_verify', methods=['GET','POST'])
def auth_verify():
    form_ver = VerifyForm()
    
    # threading.Timer(30, delete_otp, args=(user_id,)).start()
    if form_ver.validate_on_submit():
        try:
            # call function to verify user
            print("trying to verify...")
            verify_user(form_ver)
        except Exception as e:
            print("Verification failed at auth_verify:", e)
            flash('Verification failed: ' + str(e), 'error')
    else:
        user_id = session['user_id_reg']
        print("this is his u id",user_id)
        print("this is otp", session['verify'], form_ver.otp.data)

    return render_template("auth_verify.html", form_ver=form_ver)

# Route for login page
@auth_blueprint.route('/auth_login', methods=['GET','POST'])
def auth_login():
    form_log = LoginForm()
    if form_log.validate_on_submit():
        try:
            # call function to login user
            login_user(form_log)
            return redirect(url_for('home'))
        except Exception as e:
            print('Login failed: ' + str(e), 'error')
            return redirect(url_for('auth.auth_login'))
        
    return render_template("auth_login.html", form_log=form_log)

# Route for logout
@auth_blueprint.route('/auth_logout')
def auth_logout():
    # Clear the user's session
    session.clear()
    return redirect(url_for('auth.auth_login'))


def session_remove_if_not_verified():
    if session.get('verify'):
        try:
            user = auth.get_user(session.get('verify'))
            if not user.email_verified:
                print("Deleting session verify of user", user.display_name)
                session.pop('verify', None)
        except UserNotFoundError:
            session.pop('verify', None)

    else:
        print("No session found.")
