"""
Run this script to add missing `doctors` columns introduced in the models.
It uses the app's configured SQLAlchemy engine. Run from project root with your virtualenv activated.

Usage:
  python3 scripts/add_doctor_columns.py

This will execute ALTER TABLE IF NOT EXISTS statements and is idempotent.
"""
from app.database import engine
from sqlalchemy import text

DDL_STATEMENTS = [
    "ALTER TABLE doctors ADD COLUMN IF NOT EXISTS profile_picture VARCHAR(255);",
    "ALTER TABLE doctors ADD COLUMN IF NOT EXISTS address TEXT;",
    "ALTER TABLE doctors ADD COLUMN IF NOT EXISTS city VARCHAR(100);",
    "ALTER TABLE doctors ADD COLUMN IF NOT EXISTS state VARCHAR(100);",
    "ALTER TABLE doctors ADD COLUMN IF NOT EXISTS country VARCHAR(100);",
    "ALTER TABLE doctors ADD COLUMN IF NOT EXISTS about_me TEXT;",
    "ALTER TABLE doctors ADD COLUMN IF NOT EXISTS working_time VARCHAR(255);",
    "ALTER TABLE doctors ADD COLUMN IF NOT EXISTS patients INTEGER DEFAULT 0;",
    "ALTER TABLE doctors ADD COLUMN IF NOT EXISTS rating NUMERIC(3,2) DEFAULT 0.0;",
    "ALTER TABLE doctors ADD COLUMN IF NOT EXISTS reviews INTEGER DEFAULT 0;",
]


def run():
    print("Connecting to database and applying schema updates...")
    with engine.connect() as conn:
        for ddl in DDL_STATEMENTS:
            print("Executing:", ddl)
            conn.execute(text(ddl))
        # Some DB drivers require explicit commit for DDL; use begin
        try:
            conn.commit()
        except Exception:
            pass
    print("Done. Columns added (if they were missing).")


if __name__ == '__main__':
    run()
