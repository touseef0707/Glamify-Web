from firebase_admin import auth, db
from flask import session
import pyrebase
import datetime

from auth_routes import config
firebase = pyrebase.initialize_app(config)
pyre_auth = firebase.auth()

def register_user(form):
    try:
        print("Registering user:", form.first_name.data, form.last_name.data, form.dob.data, form.email.data, form.phone.data, form.location.data, form.username.data, form.password.data)
        
        # Create user in Firebase Authentication
        user = auth.create_user(
            display_name=form.username.data,
            email=form.email.data,
            phone_number=form.phone.data
        )
        print("User created successfully:", user)

        # update display name
        user = auth.update_user(
            user.uid,
            display_name=form.username.data
        )
        
        # Update user data in Firebase Realtime Database
        db.reference('/users').update({
            form.username.data: {
                'first_name': form.first_name.data,
                'last_name': form.last_name.data,
                'dob': form.dob.data.strftime('%Y-%m-%d'),
                'location': form.location.data,
                'created_on': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    except Exception as e:
        print("User registration failed:", e)

def login_user(form):
    user = pyre_auth.sign_in_with_email_and_password(form.email.data, form.password.data)
    session['user'] = user
