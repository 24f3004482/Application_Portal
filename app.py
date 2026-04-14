"""Placement Portal — Flask application entry point."""

import os
from datetime import datetime
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from sqlalchemy import cast, or_
from sqlalchemy.types import String
from werkzeug.utils import secure_filename

from models import Application, CompanyProfile, PlacementDrive, User, db

# Load environment variables
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads", "resumes")
ALLOWED_RESUME_EXTENSIONS = {"pdf", "doc", "docx"}

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("PLACEMENT_SECRET_KEY", "dev-secret-change-in-production")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI", "sqlite:///" + os.path.join(BASE_DIR, "placement_portal.db"))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Import route handlers
from auth.login import login as login_handler
from auth.register import register as register_handler
from auth.logout import logout as logout_handler
from admin.dashboard import admin_dashboard as admin_dashboard_handler
from admin.companies import (
    admin_companies as admin_companies_handler,
    admin_company_approve as admin_company_approve_handler,
    admin_company_reject as admin_company_reject_handler,
    admin_company_blacklist as admin_company_blacklist_handler,
    admin_company_unblacklist as admin_company_unblacklist_handler,
)
from admin.students import (
    admin_students as admin_students_handler,
    admin_student_blacklist as admin_student_blacklist_handler,
    admin_student_unblacklist as admin_student_unblacklist_handler,
)
from admin.drives import (
    admin_drives as admin_drives_handler,
    admin_drive_approve as admin_drive_approve_handler,
    admin_drive_reject as admin_drive_reject_handler,
    admin_drive_close as admin_drive_close_handler,
)
from admin.applications import admin_applications as admin_applications_handler
from company.dashboard import company_dashboard as company_dashboard_handler
from company.profile import company_profile as company_profile_handler
from company.drives import (
    company_create_drive as company_create_drive_handler,
    company_edit_drive as company_edit_drive_handler,
    company_delete_drive as company_delete_drive_handler,
    company_close_drive as company_close_drive_handler,
)
from company.applications import (
    company_view_applications as company_view_applications_handler,
    company_application_status as company_application_status_handler,
)
from student.dashboard import student_dashboard as student_dashboard_handler
from student.profile import student_profile as student_profile_handler
from student.drives import student_drive_detail as student_drive_detail_handler
from student.history import student_history as student_history_handler
from utils.database import init_db


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        @login_required
        def wrapped(*args, **kwargs):
            if current_user.is_blacklisted:
                flash("Your account has been deactivated.", "danger")
                logout_user()
                return redirect(url_for("login"))
            if current_user.role not in roles:
                flash("You do not have access to this page.", "danger")
                return redirect(url_for("index"))
            return f(*args, **kwargs)

        return wrapped

    return decorator


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for(f"{current_user.role}_dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    return login_handler()


@app.route("/register/<role>", methods=["GET", "POST"])
def register(role):
    return register_handler(role)


@app.route("/logout")
@login_required
def logout():
    return logout_handler()


# --- Admin Routes ---
@app.route("/admin/dashboard")
def admin_dashboard():
    return admin_dashboard_handler()


@app.route("/admin/manage_users")
def admin_manage_users():
    return render_template("manage_users.html")


@app.route("/admin/companies")
def admin_companies():
    return admin_companies_handler()


@app.route("/admin/companies/<int:company_user_id>/approve", methods=["POST"])
def admin_company_approve(company_user_id):
    return admin_company_approve_handler(company_user_id)


@app.route("/admin/companies/<int:company_user_id>/reject", methods=["POST"])
def admin_company_reject(company_user_id):
    return admin_company_reject_handler(company_user_id)


@app.route("/admin/companies/<int:company_user_id>/blacklist", methods=["POST"])
def admin_company_blacklist(company_user_id):
    return admin_company_blacklist_handler(company_user_id)


@app.route("/admin/companies/<int:company_user_id>/unblacklist", methods=["POST"])
def admin_company_unblacklist(company_user_id):
    return admin_company_unblacklist_handler(company_user_id)


@app.route("/admin/students")
def admin_students():
    return admin_students_handler()


@app.route("/admin/students/<int:student_id>/blacklist", methods=["POST"])
def admin_student_blacklist(student_id):
    return admin_student_blacklist_handler(student_id)


@app.route("/admin/students/<int:student_id>/unblacklist", methods=["POST"])
def admin_student_unblacklist(student_id):
    return admin_student_unblacklist_handler(student_id)


@app.route("/admin/drives")
def admin_drives():
    return admin_drives_handler()


@app.route("/admin/drives/<int:drive_id>/approve", methods=["POST"])
def admin_drive_approve(drive_id):
    return admin_drive_approve_handler(drive_id)


@app.route("/admin/drives/<int:drive_id>/reject", methods=["POST"])
def admin_drive_reject(drive_id):
    return admin_drive_reject_handler(drive_id)


@app.route("/admin/drives/<int:drive_id>/close", methods=["POST"])
def admin_drive_close(drive_id):
    return admin_drive_close_handler(drive_id)


@app.route("/admin/applications")
def admin_applications():
    return admin_applications_handler()


# --- Company Routes ---
@app.route("/company/dashboard")
def company_dashboard():
    return company_dashboard_handler()


@app.route("/company/profile", methods=["GET", "POST"])
def company_profile():
    return company_profile_handler()


@app.route("/company/drives/new", methods=["GET", "POST"])
def company_create_drive():
    return company_create_drive_handler()


@app.route("/company/drives/<int:drive_id>/edit", methods=["GET", "POST"])
def company_edit_drive(drive_id):
    return company_edit_drive_handler(drive_id)


@app.route("/company/drives/<int:drive_id>/delete", methods=["POST"])
def company_delete_drive(drive_id):
    return company_delete_drive_handler(drive_id)


@app.route("/company/drives/<int:drive_id>/close", methods=["POST"])
def company_close_drive(drive_id):
    return company_close_drive_handler(drive_id)


@app.route("/company/drives/<int:drive_id>/applications")
def company_view_applications(drive_id):
    return company_view_applications_handler(drive_id)


@app.route("/company/applications/<int:application_id>/status", methods=["POST"])
def company_application_status(application_id):
    return company_application_status_handler(application_id)


# --- Student Routes ---
@app.route("/student/dashboard")
def student_dashboard():
    return student_dashboard_handler()


@app.route("/student/drive/<int:drive_id>", methods=["GET", "POST"])
def student_drive_detail(drive_id):
    return student_drive_detail_handler(drive_id)


@app.route("/student/profile", methods=["GET", "POST"])
def student_profile():
    return student_profile_handler()


@app.route("/student/history")
def student_history():
    return student_history_handler()


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(debug=True)
