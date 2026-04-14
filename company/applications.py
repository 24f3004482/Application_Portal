"""Company applications management functionality."""

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user

from models import Application, PlacementDrive, db
from utils.helpers import role_required


@role_required("company")
def company_view_applications(drive_id):
    """View applications for a specific drive."""
    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.company_id != current_user.id:
        flash("You cannot view these applications.", "danger")
        return redirect(url_for("company_dashboard"))
    applications = Application.query.filter_by(drive_id=drive.id).order_by(Application.date_applied).all()
    return render_template("view_applications.html", drive=drive, applications=applications)


@role_required("company")
def company_application_status(application_id):
    """Update application status."""
    application = Application.query.get_or_404(application_id)
    drive = PlacementDrive.query.get_or_404(application.drive_id)
    if drive.company_id != current_user.id:
        flash("Invalid application.", "danger")
        return redirect(url_for("company_dashboard"))

    new_status = (request.form.get("status") or "").strip()
    allowed = {"Shortlisted", "Selected", "Rejected", "Applied"}
    if new_status not in allowed:
        flash("Invalid status.", "danger")
        return redirect(url_for("company_view_applications", drive_id=drive.id))

    application.status = new_status
    db.session.commit()
    flash("Application status updated.", "success")
    return redirect(url_for("company_view_applications", drive_id=drive.id))