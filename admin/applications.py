"""Admin applications management functionality."""

from flask import render_template

from models import Application
from utils.helpers import role_required


@role_required("admin")
def admin_applications():
    """Display all applications."""
    applications = Application.query.order_by(Application.date_applied.desc()).all()
    return render_template("admin_applications.html", applications=applications)