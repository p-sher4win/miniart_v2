from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify, current_app
from .webforms import UserForm, LoginForm, PasswordForm
from .models import Users, AuthMethods
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from mongoengine.errors import DoesNotExist
from bson import ObjectId
from firebase_admin import auth as firebase_auth
from datetime import datetime


auth = Blueprint('auth', __name__)

@auth.route("/verify-token", methods=["POST"])
def verify_token():
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"error": "Token missing"}), 400 # Bad request error for token

    try:
        # Verify Google/Firebase token
        decoded = firebase_auth.verify_id_token(token, clock_skew_seconds=5)
        email = decoded["email"].lower()
        name = decoded.get("name", "")
        google_uid = decoded["uid"]

        # Determine role
        admin_email = current_app.config["ADMIN_EMAIL"]
        role = "admin" if email == admin_email else "operator"

        # Find or create user in Users collection
        user = Users.objects(email=email).first()
        if not user:
            user = Users(
                name=name,
                email = email,
                role=role
            )
            user.save()
        else:
            # update name/role if changed
            updated = False
            if user.name != name:
                user.name = name
                updated = True
            if user.role != role:
                user.role = role
                updated = True
            if updated:
                user.save()

        # Ensure AuthMethods entry exists for Google
        auth_method = AuthMethods.objects(user_id=user, provider="google").first()
        if not auth_method:
            auth_method = AuthMethods(
                user_id=user,
                provider="google",
                provider_uid=google_uid
            )
            auth_method.save()
        else:
            # Update provider_uid if missing
            if auth_method.provider_uid != google_uid:
                auth_method.provider_uid = google_uid
                auth_method.save()

        # Login user via Flask-Login
        login_user(user)

        return jsonify({
            "status": "success",
            "role": user.role,
            "user_id": str(user.id)
        })

    except Exception as e:
        print("❌ VERIFY TOKEN ERROR:", e)
        return jsonify({"error": str(e)}), 401 # Unauthorized error for token
    

@auth.route("/mauth")
def login():
    return render_template(
        "pages/login.html",
        firebase_api_key=current_app.config["FIREBASE_API_KEY"],
        firebase_auth_domain=current_app.config["FIREBASE_AUTH_DOMAIN"]
    )
    # return "works"