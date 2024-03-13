import datetime
import pyrebase
from firebase_admin import db, auth
from flask_recaptcha import ReCaptcha
from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
from auth_forms import RegistrationForm, LoginForm
import datetime

auth_blueprint = Blueprint('auth', __name__, static_folder='static', template_folder='templates')

config = {
  'apiKey': "AIzaSyBq7bEWK8PNBYkMR3Mh3N7Vx74h8htl0A8",
  'authDomain': "glamify-0707.firebaseapp.com",
  'projectId': "glamify-0707",
  'storageBucket': "glamify-0707.appspot.com",
  'messagingSenderId': "207645995862",
  'appId': "1:207645995862:web:8d876324e21dca40429cf7",
  'measurementId': "G-GC6114YNP2",
  'databaseURL': "https://glamify-0707-default-rtdb.asia-southeast1.firebasedatabase.app/"
};

firebase = pyrebase.initialize_app(config)
pyre_auth = firebase.auth()

from flask import Blueprint, render_template, redirect, url_for, flash, session
from auth_forms import RegistrationForm, LoginForm
from fb_operations import register_user, login_user

auth_blueprint = Blueprint('auth', __name__, static_folder='static', template_folder='templates')

@auth_blueprint.route('/auth_register', methods=['GET','POST'])
def auth_register():
    print("-----auth_register-----")
    form_reg = RegistrationForm()
    print(form_reg.errors)
    print(form_reg.validate_on_submit())
    print(form_reg.first_name.data, form_reg.last_name.data, form_reg.dob.data, form_reg.email.data, form_reg.phone.data, form_reg.location.data, form_reg.username.data, form_reg.password.data, form_reg.confirm_password.data)
    if form_reg.validate_on_submit():
        print("validated")
        try:
            print("trying")
            register_user(form_reg)
            flash('Registration successful', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash('Registration failed: ' + str(e), 'error')
    return render_template("auth_register.html", form_reg=form_reg)

@auth_blueprint.route('/auth_login', methods=['GET','POST'])
def auth_login():
    form_log = LoginForm()
    if form_log.validate_on_submit():
        try:
            login_user(form_log)
            flash('Login successful', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash('Login failed: ' + str(e), 'error')

    return render_template("auth_login.html", form_log=form_log)
