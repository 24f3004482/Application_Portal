"""Student drives functionality (applying to drives)."""

from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user

from models import Application, CompanyProfile, PlacementDrive, User, db
from utils.helpers import _parse_deadline, role_required


@role_required("student")
def student_drive_detail(drive_id):
    """Display drive details and handle applications."""
    drive = PlacementDrive.query.get_or_404(drive_id)
    company = User.query.get(drive.company_id)
    profile = CompanyProfile.query.filter_by(user_id=drive.company_id).first()

    if drive.status != "Approved":
        flash("This drive is not available.", "danger")
        return redirect(url_for("student_dashboard"))
    if not company or company.approval_state != "approved" or company.is_blacklisted:
        flash("This drive is not available.", "danger")
        return redirect(url_for("student_dashboard"))

    dl = _parse_deadline(drive.deadline)
    if dl is not None and dl < datetime.utcnow().date():
        flash("The application deadline has passed.", "warning")

    existing = Application.query.filter_by(student_id=current_user.id, drive_id=drive.id).first()

    if request.method == "POST":
        if dl is not None and dl < datetime.utcnow().date():
            flash("The application deadline has passed.", "danger")
            return redirect(url_for("student_drive_detail", drive_id=drive.id))
        if existing:
            flash("You have already applied to this drive.", "warning")
            return redirect(url_for("student_drive_detail", drive_id=drive.id))

        app_row = Application(student_id=current_user.id, drive_id=drive.id, status="Applied")
        db.session.add(app_row)
        db.session.commit()
        flash("Application submitted.", "success")
        return redirect(url_for("student_drive_detail", drive_id=drive.id))

    deadline_passed = dl is not None and dl < datetime.utcnow().date()

    return render_template(
        "student_drive_detail.html",
        drive=drive,
        company=company,
        company_profile=profile,
        existing_application=existing,
        deadline_passed=deadline_passed,
    )