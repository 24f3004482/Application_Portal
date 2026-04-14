"""User registration routes and logic."""

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user

from models import CompanyProfile, User, db


def register(role):
    """Handle user registration."""
    if role not in ("student", "company"):
        flash("Invalid registration role.", "danger")
        return redirect(url_for("login"))

    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        contact = (request.form.get("contact") or "").strip()

        if not email or not password or not name:
            flash("Name, email, and password are required.", "danger")
            return render_template("register.html", role=role)

        if User.query.filter_by(email=email).first():
            flash("That email is already registered.", "danger")
            return render_template("register.html", role=role)

        approval_state = "approved" if role == "student" else "pending"

        user = User(
            name=name,
            email=email,
            role=role,
            contact=contact,
            approval_state=approval_state,
            is_blacklisted=False,
        )
        user.set_password(password)

        if role == "student":
            roll = (request.form.get("student_roll") or "").strip()
            if roll:
                if User.query.filter_by(student_roll=roll).first():
                    flash("That student roll number is already registered.", "danger")
                    return render_template("register.html", role=role)
                user.student_roll = roll

        db.session.add(user)
        db.session.flush()

        if role == "company":
            company_name = (request.form.get("company_name") or name).strip()
            hr_contact = (request.form.get("hr_contact") or "").strip()
            website = (request.form.get("website") or "").strip()
            description = (request.form.get("description") or "").strip()
            profile = CompanyProfile(
                user_id=user.id,
                company_name=company_name,
                hr_contact=hr_contact or None,
                website=website or None,
                description=description or None,
            )
            db.session.add(profile)

        db.session.commit()

        if role == "company":
            flash("Registration submitted. Wait for admin approval before logging in.", "success")
        else:
            flash("Registration successful. You can log in now.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", role=role)