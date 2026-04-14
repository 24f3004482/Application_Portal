"""Admin companies management functionality."""

from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import cast, or_
from sqlalchemy.types import String

from models import CompanyProfile, User, db
from utils.helpers import role_required


@role_required("admin")
def admin_companies():
    """Display and search companies."""
    q = (request.args.get("q") or "").strip()
    query = User.query.filter_by(role="company")
    if q:
        like = f"%{q}%"
        query = query.join(CompanyProfile, CompanyProfile.user_id == User.id).filter(
            or_(
                User.name.ilike(like),
                User.email.ilike(like),
                User.contact.ilike(like),
                CompanyProfile.company_name.ilike(like),
                cast(User.id, String).like(f"%{q}%"),
            )
        )
    companies = query.order_by(User.id).all()
    return render_template("admin_companies.html", companies=companies, q=q)


@role_required("admin")
def admin_company_approve(company_user_id):
    """Approve a company registration."""
    u = User.query.get_or_404(company_user_id)
    if u.role != "company":
        flash("Not a company account.", "danger")
        return redirect(url_for("admin_companies"))
    u.approval_state = "approved"
    db.session.commit()
    flash("Company approved.", "success")
    return redirect(url_for("admin_companies"))


@role_required("admin")
def admin_company_reject(company_user_id):
    """Reject a company registration."""
    u = User.query.get_or_404(company_user_id)
    if u.role != "company":
        flash("Not a company account.", "danger")
        return redirect(url_for("admin_companies"))
    u.approval_state = "rejected"
    db.session.commit()
    flash("Company registration rejected.", "info")
    return redirect(url_for("admin_companies"))


@role_required("admin")
def admin_company_blacklist(company_user_id):
    """Blacklist a company."""
    u = User.query.get_or_404(company_user_id)
    if u.role != "company":
        flash("Not a company account.", "danger")
        return redirect(url_for("admin_companies"))
    u.is_blacklisted = True
    db.session.commit()
    flash("Company blacklisted.", "warning")
    return redirect(url_for("admin_companies"))


@role_required("admin")
def admin_company_unblacklist(company_user_id):
    """Remove blacklist from a company."""
    u = User.query.get_or_404(company_user_id)
    if u.role != "company":
        flash("Not a company account.", "danger")
        return redirect(url_for("admin_companies"))
    u.is_blacklisted = False
    db.session.commit()
    flash("Blacklist removed for this company.", "success")
    return redirect(url_for("admin_companies"))