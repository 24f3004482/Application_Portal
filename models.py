"""SQLAlchemy models for the Placement Portal."""

from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """Application user: admin, company, or student."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, index=True)
    contact = db.Column(db.String(100))

    # Company approval: pending / approved / rejected (students/admin use approved)
    approval_state = db.Column(db.String(20), default="approved", nullable=False)

    is_blacklisted = db.Column(db.Boolean, default=False, nullable=False)

    # Student-only: institute roll / ID for search
    student_roll = db.Column(db.String(50), unique=True, nullable=True, index=True)

    resume_filename = db.Column(db.String(255), nullable=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def is_company_approved(self) -> bool:
        return self.role == "company" and self.approval_state == "approved"

    def is_company_pending(self) -> bool:
        return self.role == "company" and self.approval_state == "pending"

    def is_company_rejected(self) -> bool:
        return self.role == "company" and self.approval_state == "rejected"


class CompanyProfile(db.Model):
    """Extended profile for registered companies."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    company_name = db.Column(db.String(150), nullable=False)
    hr_contact = db.Column(db.String(150))
    website = db.Column(db.String(255))
    description = db.Column(db.Text)

    user = db.relationship("User", backref=db.backref("company_profile", uselist=False))


class PlacementDrive(db.Model):
    """A placement drive (job posting) created by a company."""

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    eligibility = db.Column(db.String(500), nullable=False)
    deadline = db.Column(db.String(32), nullable=False)
    status = db.Column(db.String(50), default="Pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    company = db.relationship("User", backref=db.backref("drives", lazy="dynamic"))


class Application(db.Model):
    """Student application to a placement drive."""

    __table_args__ = (
        db.UniqueConstraint("student_id", "drive_id", name="uq_application_student_drive"),
    )

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drive.id"), nullable=False, index=True)
    status = db.Column(db.String(50), default="Applied", nullable=False)
    date_applied = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    student = db.relationship("User", backref=db.backref("applications", lazy="dynamic"))
    drive = db.relationship("PlacementDrive", backref=db.backref("applications", lazy="dynamic"))
