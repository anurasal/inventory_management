import os


class Config:
    """Application configuration."""

    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key")

    # Session
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

    # SQLite Database
    DATABASE = "inventory.db"

    # CSV Export Folder
    EXPORT_FOLDER = "exports"

    # Flask Settings
    TEMPLATES_AUTO_RELOAD = True
