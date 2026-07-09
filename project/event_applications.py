"""交流イベント申込"""
from __future__ import annotations

from sqlalchemy import text


def ensure_event_applications_schema(engine):
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS event_applications (
                    application_id SERIAL PRIMARY KEY,
                    event_key VARCHAR(64) NOT NULL,
                    account_id INTEGER NULL,
                    applicant_name VARCHAR(128) NOT NULL,
                    applicant_email VARCHAR(256) NULL,
                    note TEXT NULL,
                    status VARCHAR(32) NOT NULL DEFAULT 'confirmed',
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
        )
        conn.execute(
            text(
                """
                CREATE INDEX IF NOT EXISTS idx_event_applications_event_key
                ON event_applications (event_key)
                """
            )
        )


def create_application(engine, event_key, account_id, name, email, note=None):
    with engine.begin() as conn:
        result = conn.execute(
            text(
                """
                INSERT INTO event_applications (
                    event_key, account_id, applicant_name, applicant_email, note
                )
                VALUES (
                    :event_key, :account_id, :applicant_name, :applicant_email, :note
                )
                RETURNING application_id, status, created_at
                """
            ),
            {
                "event_key": str(event_key),
                "account_id": account_id,
                "applicant_name": name.strip(),
                "applicant_email": email.strip() if email else None,
                "note": note.strip() if note else None,
            },
        )
        row = result.fetchone()
    mapping = row._mapping if hasattr(row, "_mapping") else row
    return {
        "application_id": mapping["application_id"],
        "status": mapping["status"],
        "created_at": mapping["created_at"],
    }


def fetch_applications_for_account(engine, account_id):
    with engine.connect() as conn:
        result = conn.execute(
            text(
                """
                SELECT application_id, event_key, status, created_at
                FROM event_applications
                WHERE account_id = :account_id
                ORDER BY created_at DESC
                """
            ),
            {"account_id": account_id},
        )
        rows = result.fetchall()
    items = []
    for row in rows:
        mapping = row._mapping if hasattr(row, "_mapping") else row
        items.append(
            {
                "application_id": mapping["application_id"],
                "event_key": mapping["event_key"],
                "status": mapping["status"],
                "created_at": mapping["created_at"].isoformat()
                if mapping["created_at"]
                else None,
            }
        )
    return items
