"""Database initialization and utilities."""

from models import db


def init_db():
    """Create tables and seed default admin."""
    from utils.helpers import ensure_upload_folder
    ensure_upload_folder()
    db.create_all()
    # Check if admin user exists
    try:
        from models import User
        if not User.query.filter_by(role="admin").first():
            from auth.admin_setup import create_default_admin
            create_default_admin()
    except:
        # If there's any issue with the query, try to create admin anyway
        try:
            from auth.admin_setup import create_default_admin
            create_default_admin()
        except:
            pass