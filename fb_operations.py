from firebase_admin import auth, db
from flask import session
import pyrebase
import datetime

from auth_routes import config
firebase = pyrebase.initialize_app(config)
pyre_auth = firebase.auth()

def register_user(form):
    user = auth.create_user(
        display_name=form.username.data,
        email=form.email.data,
        phone=form.phone.data,
        email_verified=False
    )

    auth.update_user(user.uid,
                     first_name=form.first_name.data,
                     last_name=form.last_name.data,
                     dob=form.dob.data.strftime('%Y-%m-%d'),
                     address=form.location.data)
    db.reference('/users').update({
        user.uid: {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'dob': form.dob.data.strftime('%Y-%m-%d'),
            'location': form.location.data,
            'created_on': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    })

def login_user(form):
    user = pyre_auth.sign_in_with_email_and_password(form.email.data, form.password.data)
    session['user'] = user
