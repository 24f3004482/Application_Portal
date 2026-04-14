"""Admin drives management functionality."""

from flask import flash, redirect, render_template, url_for

from models import PlacementDrive, User, db
from utils.helpers import role_required


@role_required("admin")
def admin_drives():
    """Display all placement drives."""
    drives = PlacementDrive.query.order_by(PlacementDrive.created_at.desc()).all()
    return render_template("admin_drives.html", drives=drives)


@role_required("admin")
def admin_drive_approve(drive_id):
    """Approve a placement drive."""
    drive = PlacementDrive.query.get_or_404(drive_id)
    company = User.query.get(drive.company_id)
    if company and company.approval_state != "approved":
        flash("Approve the company before approving its drives.", "danger")
        return redirect(url_for("admin_drives"))
    drive.status = "Approved"
    db.session.commit()
    flash("Drive approved.", "success")
    return redirect(url_for("admin_drives"))


@role_required("admin")
def admin_drive_reject(drive_id):
    """Reject a placement drive."""
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = "Rejected"
    db.session.commit()
    flash("Drive rejected.", "info")
    return redirect(url_for("admin_drives"))


@role_required("admin")
def admin_drive_close(drive_id):
    """Close a placement drive."""
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = "Closed"
    db.session.commit()
    flash("Drive closed.", "success")
    return redirect(url_for("admin_drives"))