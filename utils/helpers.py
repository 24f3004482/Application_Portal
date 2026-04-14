"""Shared helper functions."""

import os
from datetime import datetime

from flask import flash, redirect, url_for
from flask_login import current_user, logout_user
from werkzeug.utils import secure_filename

from models import Application, PlacementDrive, User

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads", "resumes")
ALLOWED_RESUME_EXTENSIONS = {"pdf", "doc", "docx"}


def allowed_file(filename):
    """Check if file extension is allowed for resume uploads."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_RESUME_EXTENSIONS


def ensure_upload_folder():
    """Create upload folder if it doesn't exist."""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def role_required(*roles):
    """Decorator to require specific user roles."""
    def decorator(f):
        from functools import wraps
        from flask_login import login_required

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


def _parse_deadline(deadline_str):
    """Parse YYYY-MM-DD deadline; return date or None."""
    try:
        return datetime.strptime(deadline_str[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None