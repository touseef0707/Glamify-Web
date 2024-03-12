import pyrebase
from firebase_admin import db, auth
from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
from auth_forms import RegistrationForm, LoginForm

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


@auth_blueprint.route('/signin')
def signin():
    form_reg = RegistrationForm()
    form_log = LoginForm()
    return render_template("signin.html", form_reg=form_reg, form_log=form_log)