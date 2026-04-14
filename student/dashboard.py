"""Student dashboard functionality."""

from datetime import datetime

from flask import render_template
from flask_login import current_user

from models import Application, PlacementDrive, User
from utils.helpers import _parse_deadline, role_required


@role_required("student")
def student_dashboard():
    """Display student dashboard with available drives and applications."""
    available = PlacementDrive.query.filter_by(status="Approved").all()
    open_drives = []
    today = datetime.utcnow().date()
    for d in available:
        company = User.query.get(d.company_id)
        if not company or company.is_blacklisted or company.approval_state != "approved":
            continue
        dl = _parse_deadline(d.deadline)
        if dl is not None and dl < today:
            continue
        open_drives.append(d)

    my_apps = (
        Application.query.filter_by(student_id=current_user.id).order_by(Application.date_applied.desc()).all()
    )
    return render_template(
        "student_dashboard.html",
        available_drives=open_drives,
        applications=my_apps,
    )