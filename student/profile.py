"""Student profile management functionality."""

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename

from models import User, db
from utils.helpers import allowed_file, ensure_upload_folder, role_required


@role_required("student")
def student_profile():
    """Display and update student profile."""
    ensure_upload_folder()
    if request.method == "POST":
        current_user.name = (request.form.get("name") or current_user.name).strip()
        current_user.contact = (request.form.get("contact") or "").strip()
        roll = (request.form.get("student_roll") or "").strip()
        if roll and roll != (current_user.student_roll or ""):
            other = User.query.filter_by(student_roll=roll).first()
            if other and other.id != current_user.id:
                flash("That roll number is already used.", "danger")
                return render_template("profile.html")
            current_user.student_roll = roll
        elif not roll:
            current_user.student_roll = None

        f = request.files.get("resume")
        if f and f.filename:
            if not allowed_file(f.filename):
                flash("Resume must be a PDF or Word document (.pdf, .doc, .docx).", "danger")
                return render_template("profile.html")
            fn = secure_filename(f.filename)
            unique = f"{current_user.id}_{fn}"
            from utils.helpers import UPLOAD_FOLDER
            import os
            path = os.path.join(UPLOAD_FOLDER, unique)
            f.save(path)
            current_user.resume_filename = unique

        db.session.commit()
        flash("Profile updated.", "success")
        return redirect(url_for("student_profile"))

    return render_template("profile.html")