"""Company drives management functionality."""

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user

from models import Application, PlacementDrive, db
from utils.helpers import role_required


@role_required("company")
def company_create_drive():
    """Create a new placement drive."""
    if current_user.approval_state != "approved":
        flash("Your company must be approved to create drives.", "danger")
        return redirect(url_for("company_dashboard"))

    if request.method == "POST":
        job_title = (request.form.get("job_title") or "").strip()
        job_description = (request.form.get("job_description") or "").strip()
        eligibility = (request.form.get("eligibility") or "").strip()
        deadline = (request.form.get("deadline") or "").strip()

        if not all([job_title, job_description, eligibility, deadline]):
            flash("All fields are required.", "danger")
            return render_template("create_drive.html")

        drive = PlacementDrive(
            company_id=current_user.id,
            job_title=job_title,
            job_description=job_description,
            eligibility=eligibility,
            deadline=deadline,
            status="Pending",
        )
        db.session.add(drive)
        db.session.commit()
        flash("Drive created and pending admin approval.", "success")
        return redirect(url_for("company_dashboard"))

    return render_template("create_drive.html")


@role_required("company")
def company_edit_drive(drive_id):
    """Edit an existing placement drive."""
    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.company_id != current_user.id:
        flash("You cannot edit this drive.", "danger")
        return redirect(url_for("company_dashboard"))

    if drive.status == "Closed":
        flash("This drive is closed and cannot be edited.", "danger")
        return redirect(url_for("company_dashboard"))

    if request.method == "POST":
        drive.job_title = (request.form.get("job_title") or "").strip()
        drive.job_description = (request.form.get("job_description") or "").strip()
        drive.eligibility = (request.form.get("eligibility") or "").strip()
        drive.deadline = (request.form.get("deadline") or "").strip()
        if not all([drive.job_title, drive.job_description, drive.eligibility, drive.deadline]):
            flash("All fields are required.", "danger")
            return render_template("edit_drive.html", drive=drive)
        if drive.status == "Rejected":
            drive.status = "Pending"
        db.session.commit()
        flash("Drive updated.", "success")
        return redirect(url_for("company_dashboard"))

    return render_template("edit_drive.html", drive=drive)


@role_required("company")
def company_delete_drive(drive_id):
    """Delete a placement drive."""
    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.company_id != current_user.id:
        flash("You cannot delete this drive.", "danger")
        return redirect(url_for("company_dashboard"))
    Application.query.filter_by(drive_id=drive.id).delete()
    db.session.delete(drive)
    db.session.commit()
    flash("Drive removed.", "success")
    return redirect(url_for("company_dashboard"))


@role_required("company")
def company_close_drive(drive_id):
    """Close a placement drive."""
    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.company_id != current_user.id:
        flash("You cannot modify this drive.", "danger")
        return redirect(url_for("company_dashboard"))
    drive.status = "Closed"
    db.session.commit()
    flash("Drive closed.", "success")
    return redirect(url_for("company_dashboard"))