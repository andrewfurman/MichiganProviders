"""
create_tables.py
─────────────────────────────────────────────────────────────────────────────
• Verifies the app can connect to the PostgreSQL database
• Imports every model so SQLAlchemy’s metadata is fully populated
• Creates (or upgrades) all tables in the database
Run:  python create_tables.py
─────────────────────────────────────────────────────────────────────────────
"""

import logging
from sqlalchemy import text
from main import app, db           # re-use the Flask app & SQLAlchemy instance

# ────────────────────────────────────────────────────────────────────────────
# 1.  Verify DB connectivity
# ────────────────────────────────────────────────────────────────────────────
def verify_db_connection() -> None:
    """
    Executes a simple SELECT 1 to confirm that the DATABASE_URL in main.py
    is valid and the server is reachable.
    """
    with app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
            print("✅  Database connection established")
        except Exception as exc:        # pylint: disable=broad-except
            print("❌  Failed to connect to database:", exc)
            raise                      # Surface the error so CI/CD fails


# ────────────────────────────────────────────────────────────────────────────
# 2.  Import every model so they’re registered with SQLAlchemy
#     (models/__init__.py already imports each sub-module)
# ────────────────────────────────────────────────────────────────────────────
def import_all_models() -> None:
    """
    Importing `models` triggers its __init__.py, which in turn imports every
    model module (provider, hospital, etc.).  That ensures all tables are
    present in SQLAlchemy’s metadata before we call `create_all()`.
    """
    import models  # noqa: F401  pylint: disable=import-outside-toplevel,unused-import


# ────────────────────────────────────────────────────────────────────────────
# 3.  Create every table defined in metadata
# ────────────────────────────────────────────────────────────────────────────
def create_all_tables() -> None:
    """Creates tables if they don’t exist; no-ops if they’re already present."""
    with app.app_context():
        db.create_all()
        print("🗄️  All tables created (or already existed)")


# ────────────────────────────────────────────────────────────────────────────
# Entrypoint
# ────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s | %(name)s | %(message)s"
    )

    verify_db_connection()
    import_all_models()
    create_all_tables()