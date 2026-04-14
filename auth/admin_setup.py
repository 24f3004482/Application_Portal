"""Admin user setup utilities."""

import os

from models import User, db


def create_default_admin():
    """Create the default admin user if it doesn't exist."""
    if not User.query.filter_by(role="admin").first():
        admin = User(
            email=os.environ.get("ADMIN_EMAIL", "admin@institute.edu"),
            name="Admin User",
            role="admin",
            contact="",
            approval_state="approved",
            is_blacklisted=False,
        )
        admin.set_password(os.environ.get("ADMIN_PASSWORD", "adminpassword"))
        db.session.add(admin)
        db.session.commit()