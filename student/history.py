"""Student application history functionality."""

from flask import render_template
from flask_login import current_user

from models import Application
from utils.helpers import role_required


@role_required("student")
def student_history():
    """Display student's application history."""
    applications = (
        Application.query.filter_by(student_id=current_user.id).order_by(Application.date_applied.desc()).all()
    )
    return render_template("student_history.html", applications=applications)