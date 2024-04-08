# Import necessary modules and packages
from firebase_admin import auth, db
from flask import session, redirect, url_for
import pyrebase, datetime, smtplib, random
import requests

# Firebase configuration
config = {
    "apiKey": "AIzaSyBq7bEWK8PNBYkMR3Mh3N7Vx74h8htl0A8",
    "authDomain": "glamify-0707.firebaseapp.com",
    "projectId": "glamify-0707",
    "storageBucket": "glamify-0707.appspot.com",
    "messagingSenderId": "207645995862",
    "appId": "1:207645995862:web:8d876324e21dca40429cf7",
    "measurementId": "G-GC6114YNP2",
    "databaseURL": "https://glamify-0707-default-rtdb.asia-southeast1.firebasedatabase.app/",
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
pyre_auth = firebase.auth()
fdb = firebase.database()


# Function to register a new user
def register_user(form):

    # Try to create user in Firebase Authentication
    try:
        user = auth.create_user(
            display_name=form.username.data,
            email=form.email.data,
            phone_number=form.phone.data,
            password=form.password.data,
        )

        # Update user display name
        user = auth.update_user(user.uid, display_name=form.username.data)

        # Send OTP to user email
        sendOTP(form.email.data)

        # Store user id in session
        session["user_id_reg"] = user.uid

        # Update user data in Firebase Realtime Database
        db.reference("/users").update(
            {
                form.username.data: {
                    "first_name": form.first_name.data,
                    "last_name": form.last_name.data,
                    "dob": form.dob.data.strftime("%Y-%m-%d"),
                    "email": form.email.data,
                    "location": form.location.data,
                    "created_on": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            }
        )

    # Catch exception if user creation fails
    except Exception as e:
        print("User registration failed:", e)


# Function to check if user exists in Firebase Realtime Database
def check_user(username):

    user = fdb.child("users").child(username)
    if user:
        print("User found:", user.get().val())
        return True
    else:
        return False


# Function to get user email from database
def get_email(username):

    user_ref = db.reference("/users")
    if user_ref:
        email = user_ref.child(username).child("email").get()
        return email
    else:
        return None


# Function to check if user entered OTP matches the session OTP
def verify_user(form):

    # Debugging statements
    print("form.otp.data:", form.otp.data, "session['verify']:", session["verify"])

    # Try to verify user OTP
    try:
        if form.otp.data == session["verify"]:
            session.pop("user_id_reg", None)
            return True

    # Catch exception if verification fails
    except Exception as e:
        print("Verification failed:", e)

    return False


# Function to check if user entered credentials matches the database
def login_user(form):

    try:
        user_email = get_email(form.username.data)
        return try_login(user_email, form.password.data)

    except Exception as e:
        print("normal Login failed:", str(e))


# Function to login user using email and password
def try_login(user_email, user_pass):

    # Try login
    try:

        # sign in with email and password
        pyre_auth.sign_in_with_email_and_password(user_email, user_pass)

        # get user id
        user_id = auth.get_user_by_email(user_email).uid

        # create session for user
        session["user_id"] = user_id

        # return True if login successful
        return True

    # Catch exception if login fails
    except:
        print("Incorrect username/email or password.")

    return False


# Function to send OTP to user email
def sendOTP(email):

    # Generate OTP
    otp = random.randint(109832, 999999)

    # Debugging statement
    print("OTP:", otp)

    # email subject and message
    subject = "Glamify - One Time Password"
    message = "Your OTP for login is: " + str(otp)

    # email sender details
    sender_email = "glamify0707@gmail.com"
    body = f"Subject: {subject}\n\n{message}"

    # Initialize SMTP connection with Gmail server
    smtp = smtplib.SMTP("smtp.gmail.com", 587)

    # Start TLS (Transport Layer Security) encryption for secure communication
    smtp.starttls()

    # Log into the SMTP server using sender's email and password
    smtp.login(sender_email, "aaicqolgqzyrjirk")

    # Send the email containing OTP
    smtp.sendmail(sender_email, email, body)

    # Close the SMTP connection
    smtp.quit()

    # Store the OTP in session for verification
    session["verify"] = str(otp)


# Function to delete OTP from session
def delete_otp(user_id):
    session.pop("verify", None)
    print("OTP deleted for user:", user_id)

# Function to delete user from Firebase Authentication and Realtime Database
def delete_user(user_id):
    try:
        user = auth.get_user(user_id)
        auth.delete_user(user_id)
        db.reference("/users").child(user.display_name)
        print("User deleted:", user_id)
    except Exception as e:
        print("User deletion failed:", e)


# delete_user('osEHFsfWFqcAogzMQxqJSwyzlzl1')
