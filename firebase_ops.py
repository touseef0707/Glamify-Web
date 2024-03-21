# Import necessary modules and packages
from firebase_admin import auth, db
from flask import session, redirect, url_for
import pyrebase, datetime, smtplib, random

import requests

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
            phone_number=form.phone.data,
            password=form.password.data
        )
        # Update user display name
        user = auth.update_user(
            user.uid,
            display_name=form.username.data
        )
        print("sending email...")
        sendOTP(form.email.data)

        session['user_id_reg'] = user.uid
        print(session['user_id_reg'])
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
        print("user reference temporarily updated...")
    except Exception as e:
        print("User registration failed:", e)

# Function to check if user exists
def check_user(username):
    user = fdb.child('users').child(username)
    if user:
        print("User found:", user.get().val())
        return True
    else:
        return False

# Function to get user email from database
def get_email(username):
    user_ref = db.reference('/users')
    if user_ref:
        # Get email from user data in Firebase Realtime Database
        email = user_ref.child(username).child('email').get()
        return email
    else:
        return None
    
# Function to login user
def login_user(form):
    try:    
        user_email = get_email(form.username.data)
        try_login(user_email, form.password.data)
    except Exception as e:
        print("normal Login failed:", str(e))

def try_login(user_email, user_pass):
    try:
        pyre_auth.sign_in_with_email_and_password(user_email, user_pass)
        user_id = auth.get_user_by_email(user_email).uid
        session['user_id'] = user_id
        print("SUCCESSFULLY LOGGED IN!")
    except:
        print("Incorrect username/email or password.")


def sendOTP(email):
    otp = random.randint(109832, 999999)
    print("OTP:", otp)
    subject = "Glamify - One Time Password"
    message = "Your OTP for login is: " + str(otp)

    sender_email = "glamify0707@gmail.com"
    body = f"Subject: {subject}\n\n{message}"

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(sender_email, "aaicqolgqzyrjirk")
    smtp.sendmail(sender_email, email, body)
    smtp.quit()
    session['verify'] = otp

def verify_user(form):
    print("verifying user function entered...")
    if form.otp.data == session['verify']:
        session.pop('user_id_reg', None)
        print("verified successfully!")
        delete_otp(session['user_id_reg'])
        return redirect(url_for('auth.auth_login'))
    else:
        delete_otp(session['user_id_reg'])
        print("verification failed!")
        return redirect(url_for('auth.auth_verify'))
    

def delete_otp(user_id):
    session.pop('verify', None)
    print("OTP deleted for user:", user_id)

def delete_user(user_id):
    try:
        auth.delete_user(user_id)
        print("User deleted:", user_id)
    except Exception as e:
        print("User deletion failed:", e)
