# Import required libraries and modules
from firebase_admin import db, auth
from flask_recaptcha import ReCaptcha
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    Blueprint
)
from auth_forms import RegistrationForm, LoginForm, VerifyForm
from firebase_ops import register_user, login_user, sendOTP, delete_otp, verify_user
from firebase_admin.auth import UserNotFoundError

# Initialize Flask app Blue Print for routes
auth_blueprint = Blueprint(
    "auth", __name__, static_folder="static", template_folder="templates"
)

# Route for registration page
@auth_blueprint.route("/auth_register", methods=["GET", "POST"])
def auth_register():

    # Get Form data
    form_reg = RegistrationForm()   

    # Check if form is validated                           
    if form_reg.validate_on_submit():

        # register user and redirect to verify page
        try:
            register_user(form_reg)
            return redirect(url_for("auth.auth_verify"))
        
        # Catch exception if registration fails
        except Exception as e:
            print("Registration failed at auth_register:", e)
            flash("Registration failed: " + str(e), "error")

    return render_template("auth_register.html", form_reg=form_reg)


# Route for verification page 
@auth_blueprint.route("/auth_verify", methods=["GET", "POST"])
def auth_verify():

    # Get Form data
    form_ver = VerifyForm()
    # threading.Timer(30, delete_otp, args=(user_id,)).start()

    # Check if form is validated
    if form_ver.validate_on_submit():

        # Verify user and redirect to login page
        try:
            if verify_user(form_ver) == True:
                return redirect(url_for("auth.auth_login"))
            
        # Catch exception if verification fails
        except Exception as e:
            print("Verification failed at auth_verify:", e)
            flash("Verification failed: " + str(e), "error")
    
    # debug satements
    # print("this is his u id", session["user_id_reg"])
    # print("this is otp", session["verify"], form_ver.otp.data)

    return render_template("auth_verify.html", form_ver=form_ver)


# Route for login page
@auth_blueprint.route("/auth_login", methods=["GET", "POST"])
def auth_login():

    # Get Form data
    form_log = LoginForm()

    # Check if form is validated
    if form_log.validate_on_submit():

        # Attempt to Login user and redirect to home page
        try:
            if login_user(form_log) == True:
                return redirect(url_for("home"))
            
        # Catch exception if login fails 
        except Exception as e:
            print("Login failed: " + str(e), "error")
            return redirect(url_for("auth.auth_login"))
        
    return render_template("auth_login.html", form_log=form_log)


# Route for logout and clearing session
@auth_blueprint.route("/auth_logout")
def auth_logout():
    session.clear()
    return redirect(url_for("auth.auth_login"))


# Route to remove session if not verified
def session_remove_if_not_verified():

    # Check if session is verified
    if session.get("verify"):

        # Attempt to delete user session if not verified
        try:
            user = auth.get_user(session.get("verify"))
            if not user.email_verified:
                print("Deleting session verify of user", user.display_name)
                session.pop("verify", None)
        
        # Catch exception if user not found
        except UserNotFoundError:
            session.pop("verify", None)

    else:
        print("No session found.")
