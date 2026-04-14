"""Company profile management functionality."""

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user

from models import CompanyProfile, db
from utils.helpers import role_required


@role_required("company")
def company_profile():
    """Display and update company profile."""
    profile = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        profile = CompanyProfile(
            user_id=current_user.id,
            company_name=current_user.name,
        )
        db.session.add(profile)
        db.session.commit()

    if request.method == "POST":
        profile.company_name = (request.form.get("company_name") or "").strip() or profile.company_name
        profile.hr_contact = (request.form.get("hr_contact") or "").strip() or None
        profile.website = (request.form.get("website") or "").strip() or None
        profile.description = (request.form.get("description") or "").strip() or None
        current_user.name = (request.form.get("contact_name") or current_user.name).strip()
        current_user.contact = (request.form.get("contact") or "").strip() or current_user.contact
        db.session.commit()
        flash("Profile updated.", "success")
        return redirect(url_for("company_profile"))

    return render_template("company_profile.html", profile=profile)