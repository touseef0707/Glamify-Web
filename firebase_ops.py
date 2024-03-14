# Import necessary modules and packages
from firebase_admin import auth, db
from flask import session, redirect, url_for
import pyrebase
import datetime

# Firebase configuration
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

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
pyre_auth = firebase.auth()
fdb = firebase.database()

# Function to register a new user
def register_user(form):
    try:
        # Create user in Firebase Authentication
        user = auth.create_user(
            display_name=form.username.data,
            email=form.email.data,
            phone_number=form.phone.data
        )
        # Update user display name
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
                'email': form.email.data,
                'location': form.location.data,
                'created_on': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    except Exception as e:
        print("User registration failed:", e)

# Function to check if user exists
def check_user(username):
    # Access user data from Firebase Realtime Database
    user = fdb.child('users').child(username)
    if user:
        return True
    else:
        return False

# Function to get user email from database
def get_email(username):
    if check_user(username):
        # Get email from user data in Firebase Realtime Database
        email = fdb.child('users').child(username).get().val().get('email')
        return email
    else:
        return None

# Function to login user
def login_user(form):
    try:
        # Get user email
        user_email = get_email(form.username.data)
        if user_email:
            # Sign in user with email and password
            user = pyre_auth.sign_in_with_email_and_password(user_email, form.password.data)
            print("User logged in successfully:", user['displayName'])
            session['user'] = user
        else:
            print("Email not found for user:", form.username.data)
    except Exception as e:
        print("Login failed:", str(e))
