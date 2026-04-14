"""Logout functionality."""

from flask import flash, redirect, url_for
from flask_login import logout_user


def logout():
    """Handle user logout."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))