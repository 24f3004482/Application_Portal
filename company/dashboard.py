"""Company dashboard functionality."""

from flask import flash, redirect, render_template, url_for
from flask_login import current_user

from models import CompanyProfile, PlacementDrive
from utils.helpers import role_required


@role_required("company")
def company_dashboard():
    """Display company dashboard."""
    if current_user.approval_state != "approved":
        flash("Your company account is not approved.", "danger")
        return redirect(url_for("logout"))
    profile = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    drives = PlacementDrive.query.filter_by(company_id=current_user.id).order_by(
        PlacementDrive.created_at.desc()
    ).all()
    return render_template(
        "company_dashboard.html",
        company=current_user,
        profile=profile,
        drives=drives,
    )