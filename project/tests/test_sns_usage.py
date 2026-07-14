"""
SNS週間投稿回数制限のテスト（実DBに接続して検証する）

- 無料ユーザー: 週2回まで
- 月額500円会員(general): 週5回まで
- プレミアム会員(premium): 無制限
- 日本時間の月曜0時で週が切り替わる
- 同時投稿でも上限を超えない
"""
import os
import sys
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sns import (  # noqa: E402
    SnsUsageLimitError,
    build_sns_usage_status,
    consume_sns_post_usage,
    ensure_sns_schema,
    get_next_week_start,
    get_week_start,
)

APP_DIR = Path(__file__).resolve().parent.parent
load_dotenv(APP_DIR / ".env")
load_dotenv(APP_DIR / "env")

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    pytest.skip("DATABASE_URL が未設定のためSNS週間利用制限のDB連携テストをスキップします", allow_module_level=True)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
ensure_sns_schema(engine)

TEST_ACCOUNT_ID = 18  # 既存のテスト用アカウント（accounts.account_id=18 "Test User"）


@pytest.fixture(autouse=True)
def _clean_usage_rows():
    with engine.begin() as conn:
        conn.execute(
            text("DELETE FROM sns_weekly_usage WHERE account_id = :account_id"),
            {"account_id": TEST_ACCOUNT_ID},
        )
    yield
    with engine.begin() as conn:
        conn.execute(
            text("DELETE FROM sns_weekly_usage WHERE account_id = :account_id"),
            {"account_id": TEST_ACCOUNT_ID},
        )


def test_free_user_allows_two_posts_then_blocks_third():
    consume_sns_post_usage(TEST_ACCOUNT_ID, None, engine)
    consume_sns_post_usage(TEST_ACCOUNT_ID, None, engine)

    with pytest.raises(SnsUsageLimitError) as exc:
        consume_sns_post_usage(TEST_ACCOUNT_ID, None, engine)
    assert exc.value.status["remaining"] == 0
    assert exc.value.status["can_post"] is False

    status = build_sns_usage_status(TEST_ACCOUNT_ID, None, engine)
    assert status["used"] == 2
    assert status["limit"] == 2
    assert status["can_post"] is False


def test_general_member_allows_five_posts_then_blocks_sixth():
    for _ in range(5):
        consume_sns_post_usage(TEST_ACCOUNT_ID, "general", engine)

    with pytest.raises(SnsUsageLimitError):
        consume_sns_post_usage(TEST_ACCOUNT_ID, "general", engine)

    status = build_sns_usage_status(TEST_ACCOUNT_ID, "general", engine)
    assert status["used"] == 5
    assert status["can_post"] is False


def test_premium_member_is_unlimited():
    for _ in range(20):
        result = consume_sns_post_usage(TEST_ACCOUNT_ID, "premium", engine)
        assert result["can_post"] is True
        assert result["limit"] is None

    status = build_sns_usage_status(TEST_ACCOUNT_ID, "premium", engine)
    assert status["limit"] is None
    assert status["can_post"] is True
    assert status["used"] == 20


def test_failed_consume_does_not_increment_further_after_limit():
    consume_sns_post_usage(TEST_ACCOUNT_ID, None, engine)
    consume_sns_post_usage(TEST_ACCOUNT_ID, None, engine)
    for _ in range(3):
        with pytest.raises(SnsUsageLimitError):
            consume_sns_post_usage(TEST_ACCOUNT_ID, None, engine)

    status = build_sns_usage_status(TEST_ACCOUNT_ID, None, engine)
    assert status["used"] == 2


def test_concurrent_requests_never_exceed_limit():
    results = {"success": 0, "blocked": 0}
    lock = threading.Lock()

    def worker():
        try:
            consume_sns_post_usage(TEST_ACCOUNT_ID, None, engine)
            with lock:
                results["success"] += 1
        except SnsUsageLimitError:
            with lock:
                results["blocked"] += 1

    threads = [threading.Thread(target=worker) for _ in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert results["success"] == 2
    assert results["blocked"] == 18

    status = build_sns_usage_status(TEST_ACCOUNT_ID, None, engine)
    assert status["used"] == 2


def test_week_start_is_monday_0000_jst():
    JST = timezone(timedelta(hours=9))
    # 2026-07-13 は月曜日
    monday = datetime(2026, 7, 13, 15, 30, tzinfo=JST)
    week_start = get_week_start(monday.astimezone(timezone.utc))
    week_start_jst = week_start.astimezone(JST)
    assert (week_start_jst.year, week_start_jst.month, week_start_jst.day) == (2026, 7, 13)
    assert week_start_jst.hour == 0 and week_start_jst.minute == 0

    # 2026-07-19 は日曜日 -> 同じ週(7/13週)に属する
    sunday = datetime(2026, 7, 19, 23, 59, tzinfo=JST)
    week_start_2 = get_week_start(sunday.astimezone(timezone.utc))
    assert week_start_2 == week_start

    # 2026-07-20 は月曜日 -> 次の週になる
    next_monday = datetime(2026, 7, 20, 0, 0, tzinfo=JST)
    week_start_3 = get_week_start(next_monday.astimezone(timezone.utc))
    assert week_start_3 == get_next_week_start(monday.astimezone(timezone.utc))
