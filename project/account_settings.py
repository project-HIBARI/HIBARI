"""アカウント設定（支払方法・会員プラン）"""
from __future__ import annotations

import json
import re

from sqlalchemy import text

VALID_PAYMENT_METHODS = {"credit", "bank", "conveni", "carrier"}


def ensure_account_settings_schema(engine):
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS account_settings (
                    account_id INTEGER PRIMARY KEY,
                    payment_method VARCHAR(16) NULL,
                    payment_details JSONB NULL,
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
        )


def mask_card_number(number):
    digits = re.sub(r"\D", "", number or "")
    if len(digits) < 4:
        return None, None
    return digits[-4:], "**** **** **** " + digits[-4:]


def sanitize_payment_details(method, details):
    details = details or {}
    if method == "credit":
        last4, masked = mask_card_number(details.get("card_number", ""))
        return {
            "card_brand": details.get("card_brand") or "visa",
            "card_last4": last4,
            "card_masked": masked,
            "card_expiry": details.get("card_expiry"),
            "card_name": details.get("card_name"),
        }
    if method == "bank":
        return {
            "bank_name": details.get("bank_name"),
            "bank_branch": details.get("bank_branch"),
            "bank_account_type": details.get("bank_account_type"),
            "bank_account_number_masked": (
                "****" + str(details.get("bank_account_number", ""))[-4:]
                if details.get("bank_account_number")
                else None
            ),
            "bank_account_holder": details.get("bank_account_holder"),
        }
    if method == "conveni":
        return {"conveni_store": details.get("conveni_store")}
    if method == "carrier":
        return {"carrier_name": details.get("carrier_name")}
    return {}


def fetch_account_settings(engine, account_id):
    with engine.connect() as conn:
        result = conn.execute(
            text(
                """
                SELECT payment_method, payment_details
                FROM account_settings
                WHERE account_id = :account_id
                """
            ),
            {"account_id": account_id},
        )
        row = result.fetchone()
    if not row:
        return {"payment_method": None, "payment_details": None}
    mapping = row._mapping if hasattr(row, "_mapping") else row
    details = mapping["payment_details"]
    if isinstance(details, str):
        details = json.loads(details)
    return {
        "payment_method": mapping["payment_method"],
        "payment_details": details,
    }


def upsert_payment_settings(engine, account_id, method, details):
    if method not in VALID_PAYMENT_METHODS:
        raise ValueError("無効な支払い方法です")
    sanitized = sanitize_payment_details(method, details)
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO account_settings (account_id, payment_method, payment_details, updated_at)
                VALUES (:account_id, :payment_method, CAST(:payment_details AS JSONB), NOW())
                ON CONFLICT (account_id)
                DO UPDATE SET
                    payment_method = EXCLUDED.payment_method,
                    payment_details = EXCLUDED.payment_details,
                    updated_at = NOW()
                """
            ),
            {
                "account_id": account_id,
                "payment_method": method,
                "payment_details": json.dumps(sanitized, ensure_ascii=False),
            },
        )
    return {
        "payment_method": method,
        "payment_details": sanitized,
    }


def change_membership_plan(engine, account_id, is_premium):
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO fanclub_join_historys (account_id, is_premium, purchased_at)
                VALUES (:account_id, :is_premium, NOW())
                """
            ),
            {"account_id": account_id, "is_premium": bool(is_premium)},
        )
    return "premium" if is_premium else "general"
