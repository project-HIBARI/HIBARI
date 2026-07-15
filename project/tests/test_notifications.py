"""
SNS通知サービスのテスト（実DBに接続して検証する）

- 自分自身のイベントでは通知を作らない
- いいね/フォローのようなトグル系イベントは重複作成せず再利用する
- 未読の通知のみ解除時に削除され、既読済みは履歴として残る
"""
import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from notification_service import (  # noqa: E402
    NOTIFICATION_TYPE_FOLLOW,
    NOTIFICATION_TYPE_POST_LIKE,
    create_notification,
    delete_toggle_notification_if_unread,
    ensure_notification_schema,
    upsert_toggle_notification,
)
from sns import ensure_sns_schema  # noqa: E402

APP_DIR = Path(__file__).resolve().parent.parent
load_dotenv(APP_DIR / ".env")
load_dotenv(APP_DIR / "env")

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    pytest.skip("DATABASE_URL が未設定のため通知機能のDB連携テストをスキップします", allow_module_level=True)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
ensure_sns_schema(engine)
ensure_notification_schema(engine)

with engine.connect() as _conn:
    _account_rows = _conn.execute(text("SELECT account_id FROM accounts ORDER BY account_id LIMIT 2")).fetchall()

if len(_account_rows) < 2:
    pytest.skip("通知テスト用に2件以上のアカウントが必要です", allow_module_level=True)

RECIPIENT_ID = _account_rows[0][0]
ACTOR_ID = _account_rows[1][0]


@pytest.fixture(autouse=True)
def _clean_notification_rows():
    with engine.begin() as conn:
        conn.execute(
            text("DELETE FROM sns_notifications WHERE recipient_account_id = :r AND actor_account_id = :a"),
            {"r": RECIPIENT_ID, "a": ACTOR_ID},
        )
    yield
    with engine.begin() as conn:
        conn.execute(
            text("DELETE FROM sns_notifications WHERE recipient_account_id = :r AND actor_account_id = :a"),
            {"r": RECIPIENT_ID, "a": ACTOR_ID},
        )


def _count_notifications():
    with engine.connect() as conn:
        row = conn.execute(
            text(
                "SELECT COUNT(*) AS c FROM sns_notifications WHERE recipient_account_id = :r AND actor_account_id = :a"
            ),
            {"r": RECIPIENT_ID, "a": ACTOR_ID},
        ).fetchone()
        return row._mapping["c"]


def test_self_event_creates_no_notification():
    # post_id は FK 制約があるため自己通知ガードで INSERT に到達しない None を使う
    assert create_notification(engine, RECIPIENT_ID, RECIPIENT_ID, NOTIFICATION_TYPE_POST_LIKE) is None
    assert upsert_toggle_notification(engine, RECIPIENT_ID, RECIPIENT_ID, NOTIFICATION_TYPE_POST_LIKE) is None
    assert _count_notifications() == 0


def test_toggle_notification_is_not_duplicated():
    first_id = upsert_toggle_notification(engine, RECIPIENT_ID, ACTOR_ID, NOTIFICATION_TYPE_POST_LIKE)
    second_id = upsert_toggle_notification(engine, RECIPIENT_ID, ACTOR_ID, NOTIFICATION_TYPE_POST_LIKE)
    assert first_id == second_id
    assert _count_notifications() == 1


def test_unread_toggle_notification_is_removed_on_untoggle():
    upsert_toggle_notification(engine, RECIPIENT_ID, ACTOR_ID, NOTIFICATION_TYPE_FOLLOW)
    assert _count_notifications() == 1
    delete_toggle_notification_if_unread(engine, RECIPIENT_ID, ACTOR_ID, NOTIFICATION_TYPE_FOLLOW)
    assert _count_notifications() == 0


def test_read_toggle_notification_is_kept_on_untoggle():
    notification_id = upsert_toggle_notification(engine, RECIPIENT_ID, ACTOR_ID, NOTIFICATION_TYPE_FOLLOW)
    with engine.begin() as conn:
        conn.execute(
            text("UPDATE sns_notifications SET is_read = TRUE WHERE notification_id = :id"),
            {"id": notification_id},
        )
    delete_toggle_notification_if_unread(engine, RECIPIENT_ID, ACTOR_ID, NOTIFICATION_TYPE_FOLLOW)
    assert _count_notifications() == 1
