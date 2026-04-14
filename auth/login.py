"""Authentication routes and logic."""

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user

from models import User


def login():
    """Handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for(f"{current_user.role}_dashboard"))

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html")

        if user.is_blacklisted:
            flash("Your account has been deactivated or blacklisted.", "danger")
            return render_template("login.html")

        if user.role == "company":
            if user.approval_state == "pending":
                flash("Your company account is pending admin approval.", "warning")
                return render_template("login.html")
            if user.approval_state == "rejected":
                flash("Your company registration was rejected.", "danger")
                return render_template("login.html")

        login_user(user)
        flash("Logged in successfully.", "success")
        return redirect(url_for(f"{user.role}_dashboard"))

    return render_template("login.html")