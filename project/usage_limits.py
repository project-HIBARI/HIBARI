"""
機能利用回数の管理（PostgreSQL + Flask セッション）

- 非会員: guest_id（セッション Cookie）で識別 / 10回まで / 上限到達から7日後に解除
- 一般会員: account_id / 月10回 / 月初リセット
- プレミアム: 無制限
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import text

FEATURE_AI_CHAT = "ai_chat"
FEATURE_BOARD_POST = "board_post"

GUEST_LIMIT = 10
MEMBER_GENERAL_LIMIT = 10
GUEST_LOCK_DAYS = 7

JST = timezone(timedelta(hours=9))


class UsageLimitError(Exception):
    def __init__(self, message, status=None, locked_until=None):
        super().__init__(message)
        self.message = message
        self.status = status or {}
        self.locked_until = locked_until


def ensure_usage_schema(engine):
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS feature_usage (
                    usage_id SERIAL PRIMARY KEY,
                    subject_type VARCHAR(16) NOT NULL,
                    subject_key VARCHAR(64) NOT NULL,
                    feature VARCHAR(32) NOT NULL,
                    usage_count INTEGER NOT NULL DEFAULT 0,
                    period_start TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    locked_until TIMESTAMPTZ NULL,
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    UNIQUE (subject_type, subject_key, feature)
                )
                """
            )
        )


def ensure_guest_id(session):
    guest_id = session.get("guest_id")
    if not guest_id:
        guest_id = str(uuid.uuid4())
        session["guest_id"] = guest_id
    session.permanent = True
    return guest_id


def month_key(dt=None):
    dt = dt or datetime.now(JST)
    return f"{dt.year}-{dt.month:02d}"


def format_reset_date(dt):
    if dt is None:
        return ""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=JST)
    local = dt.astimezone(JST)
    return f"{local.year}年{local.month}月{local.day}日"


def get_usage_subject(session, get_membership_for_account):
    account_id = session.get("account_id")
    if account_id is not None:
        membership = session.get("membership")
        if membership is None:
            membership = get_membership_for_account(account_id)
        if membership is not None:
            return {
                "subject_type": "account",
                "subject_key": str(account_id),
                "membership": membership,
                "is_logged_in": True,
                "is_fanclub_member": True,
            }
        guest_id = ensure_guest_id(session)
        return {
            "subject_type": "guest",
            "subject_key": guest_id,
            "membership": None,
            "is_logged_in": True,
            "is_fanclub_member": False,
        }
    guest_id = ensure_guest_id(session)
    return {
        "subject_type": "guest",
        "subject_key": guest_id,
        "membership": None,
        "is_logged_in": False,
        "is_fanclub_member": False,
    }


def _fetch_row(engine, subject_type, subject_key, feature):
    with engine.connect() as conn:
        result = conn.execute(
            text(
                """
                SELECT usage_count, period_start, locked_until
                FROM feature_usage
                WHERE subject_type = :subject_type
                  AND subject_key = :subject_key
                  AND feature = :feature
                """
            ),
            {
                "subject_type": subject_type,
                "subject_key": subject_key,
                "feature": feature,
            },
        )
        rows = result.fetchall()
    if not rows:
        return None
    row = rows[0]
    mapping = row._mapping if hasattr(row, "_mapping") else row
    return {
        "usage_count": int(mapping["usage_count"] or 0),
        "period_start": mapping["period_start"],
        "locked_until": mapping["locked_until"],
    }


def _upsert_row(engine, subject_type, subject_key, feature, usage_count, period_start, locked_until):
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO feature_usage (
                    subject_type, subject_key, feature,
                    usage_count, period_start, locked_until, updated_at
                )
                VALUES (
                    :subject_type, :subject_key, :feature,
                    :usage_count, :period_start, :locked_until, NOW()
                )
                ON CONFLICT (subject_type, subject_key, feature)
                DO UPDATE SET
                    usage_count = EXCLUDED.usage_count,
                    period_start = EXCLUDED.period_start,
                    locked_until = EXCLUDED.locked_until,
                    updated_at = NOW()
                """
            ),
            {
                "subject_type": subject_type,
                "subject_key": subject_key,
                "feature": feature,
                "usage_count": usage_count,
                "period_start": period_start,
                "locked_until": locked_until,
            },
        )


def _normalize_row(subject, row, now=None):
    now = now or datetime.now(timezone.utc)
    if row is None:
        return {
            "usage_count": 0,
            "period_start": now,
            "locked_until": None,
        }

    usage_count = row["usage_count"]
    period_start = row["period_start"]
    locked_until = row["locked_until"]

    if period_start is not None and period_start.tzinfo is None:
        period_start = period_start.replace(tzinfo=timezone.utc)

    if locked_until is not None and locked_until.tzinfo is None:
        locked_until = locked_until.replace(tzinfo=timezone.utc)

    if subject["subject_type"] == "guest":
        if locked_until and now < locked_until:
            return {
                "usage_count": GUEST_LIMIT,
                "period_start": period_start or now,
                "locked_until": locked_until,
            }
        if locked_until and now >= locked_until:
            return {
                "usage_count": 0,
                "period_start": now,
                "locked_until": None,
            }
        return {
            "usage_count": usage_count,
            "period_start": period_start or now,
            "locked_until": None,
        }

    # 一般会員: カレンダー月が変わればリセット
    current_month = month_key(now.astimezone(JST))
    row_month = month_key((period_start or now).astimezone(JST))
    if current_month != row_month:
        return {
            "usage_count": 0,
            "period_start": now,
            "locked_until": None,
        }
    return {
        "usage_count": usage_count,
        "period_start": period_start or now,
        "locked_until": None,
    }


def _limit_for_subject(subject):
    if subject["subject_type"] == "account" and subject.get("membership") == "premium":
        return None
    return GUEST_LIMIT if subject["subject_type"] == "guest" else MEMBER_GENERAL_LIMIT


def build_usage_status(subject, feature, engine, persist_normalized=True):
    row = _fetch_row(engine, subject["subject_type"], subject["subject_key"], feature)
    normalized = _normalize_row(subject, row)
    limit = _limit_for_subject(subject)

    if persist_normalized and row is not None:
        row_locked = row.get("locked_until")
        if row_locked is not None and getattr(row_locked, "tzinfo", None) is None:
            row_locked = row_locked.replace(tzinfo=timezone.utc)
        norm_locked = normalized.get("locked_until")
        if (
            normalized["usage_count"] != row["usage_count"]
            or norm_locked != row_locked
        ):
            _upsert_row(
                engine,
                subject["subject_type"],
                subject["subject_key"],
                feature,
                normalized["usage_count"],
                normalized["period_start"],
                normalized["locked_until"],
            )

    if limit is None:
        return {
            "feature": feature,
            "is_guest": subject["subject_type"] == "guest",
            "is_logged_in": subject["is_logged_in"],
            "membership": subject.get("membership"),
            "limit": None,
            "used": normalized["usage_count"],
            "remaining": None,
            "can_use": True,
            "locked_until": None,
            "reset_label": None,
            "period": "unlimited",
        }

    remaining = max(limit - normalized["usage_count"], 0)
    locked_until = normalized["locked_until"]
    now = datetime.now(timezone.utc)
    if locked_until and locked_until.tzinfo is None:
        locked_until = locked_until.replace(tzinfo=timezone.utc)

    if locked_until and now < locked_until:
        can_use = False
        remaining = 0
    else:
        can_use = remaining > 0

    if subject["subject_type"] == "guest":
        period = "weekly_after_limit"
        reset_at = locked_until if locked_until and not can_use else None
    else:
        period = "monthly"
        reset_at = None

    return {
        "feature": feature,
        "is_guest": subject["subject_type"] == "guest",
        "is_logged_in": subject["is_logged_in"],
        "membership": subject.get("membership"),
        "limit": limit,
        "used": normalized["usage_count"],
        "remaining": remaining,
        "can_use": can_use,
        "locked_until": reset_at.isoformat() if reset_at else None,
        "reset_label": format_reset_date(reset_at) if reset_at else None,
        "period": period,
    }


def consume_usage(subject, feature, engine):
    status = build_usage_status(subject, feature, engine, persist_normalized=True)
    if not status["can_use"]:
        message = (
            f"非会員の利用上限（{GUEST_LIMIT}回）に達しました。"
            f"{status['reset_label']} に解除されます。"
            if status["is_guest"]
            else f"今月の利用上限（{MEMBER_GENERAL_LIMIT}回）に達しました。"
        )
        raise UsageLimitError(message, status=status, locked_until=status.get("locked_until"))

    if status["limit"] is None:
        return status

    row = _normalize_row(subject, _fetch_row(engine, subject["subject_type"], subject["subject_key"], feature))
    now = datetime.now(timezone.utc)
    period_start = row["period_start"] if row["usage_count"] > 0 else now
    new_count = row["usage_count"] + 1
    locked_until = row["locked_until"]

    if subject["subject_type"] == "guest" and new_count >= GUEST_LIMIT:
        locked_until = now + timedelta(days=GUEST_LOCK_DAYS)

    _upsert_row(
        engine,
        subject["subject_type"],
        subject["subject_key"],
        feature,
        new_count,
        period_start,
        locked_until,
    )
    return build_usage_status(subject, feature, engine, persist_normalized=False)
