"""Admin students management functionality."""

from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import cast, or_
from sqlalchemy.types import String

from models import User, db
from utils.helpers import role_required


@role_required("admin")
def admin_students():
    """Display and search students."""
    q = (request.args.get("q") or "").strip()
    query = User.query.filter_by(role="student")
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                User.name.ilike(like),
                User.email.ilike(like),
                User.contact.ilike(like),
                User.student_roll.ilike(like),
                cast(User.id, String).like(f"%{q}%"),
            )
        )
    students = query.order_by(User.id).all()
    return render_template("admin_students.html", students=students, q=q)


@role_required("admin")
def admin_student_blacklist(student_id):
    """Blacklist a student."""
    u = User.query.get_or_404(student_id)
    if u.role != "student":
        flash("Not a student account.", "danger")
        return redirect(url_for("admin_students"))
    u.is_blacklisted = True
    db.session.commit()
    flash("Student blacklisted.", "warning")
    return redirect(url_for("admin_students"))


@role_required("admin")
def admin_student_unblacklist(student_id):
    """Remove blacklist from a student."""
    u = User.query.get_or_404(student_id)
    if u.role != "student":
        flash("Not a student account.", "danger")
        return redirect(url_for("admin_students"))
    u.is_blacklisted = False
    db.session.commit()
    flash("Blacklist removed for this student.", "success")
    return redirect(url_for("admin_students"))