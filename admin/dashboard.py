"""Admin dashboard functionality."""

from flask import render_template

from models import Application, PlacementDrive, User
from utils.helpers import role_required


@role_required("admin")
def admin_dashboard():
    """Display admin dashboard with statistics."""
    stats = {
        "students": User.query.filter_by(role="student").count(),
        "companies": User.query.filter_by(role="company").count(),
        "drives": PlacementDrive.query.count(),
        "applications": Application.query.count(),
    }
    return render_template("admin_dashboard.html", stats=stats)