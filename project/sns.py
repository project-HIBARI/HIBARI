"""
Music Memories SNS機能（ストーリーズ / 投稿 / フォロー / DM 等）

- テーブル作成は既存パターンに合わせ ensure_sns_schema(engine) で起動時に実行
- ルート登録は open_chat.py と同様に register_sns_routes(app, engine, **deps) の
  依存注入パターンを踏襲する
- フェーズ1: データ構造と「週間投稿回数制限」のサーバー側判定のみを実装する
  （フィード/投稿/ストーリーズ本体のAPIはフェーズ2以降で追加）
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from flask import jsonify
from sqlalchemy import text

JST = timezone(timedelta(hours=9))
WEEKDAY_LABELS_JA = ["月", "火", "水", "木", "金", "土", "日"]

# 週間投稿回数制限（ストーリーズ・写真/動画投稿・ひとこと投稿の合計）
FREE_WEEKLY_POST_LIMIT = 2
GENERAL_WEEKLY_POST_LIMIT = 5
# プレミアム会員は無制限（limit=None）


class SnsUsageLimitError(Exception):
    def __init__(self, message, status=None):
        super().__init__(message)
        self.message = message
        self.status = status or {}


def ensure_sns_schema(engine):
    with engine.begin() as conn:
        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS sns_profiles (
                account_id INTEGER PRIMARY KEY REFERENCES accounts(account_id),
                bio VARCHAR(500) NOT NULL DEFAULT '',
                avatar_path VARCHAR(500) NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        ))
        conn.execute(text(
            "ALTER TABLE sns_profiles ADD COLUMN IF NOT EXISTS avatar_path VARCHAR(500)"
        ))

        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS sns_posts (
                post_id SERIAL PRIMARY KEY,
                account_id INTEGER NOT NULL REFERENCES accounts(account_id),
                post_type VARCHAR(16) NOT NULL CHECK (post_type IN ('photo', 'text')),
                body TEXT NOT NULL DEFAULT '',
                hashtags TEXT[] NOT NULL DEFAULT '{}',
                comments_enabled BOOLEAN NOT NULL DEFAULT TRUE,
                visibility VARCHAR(16) NOT NULL DEFAULT 'public',
                is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_sns_posts_feed "
            "ON sns_posts (is_deleted, created_at DESC)"
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_sns_posts_account "
            "ON sns_posts (account_id, created_at DESC)"
        ))

        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS sns_post_media (
                media_id SERIAL PRIMARY KEY,
                post_id INTEGER NOT NULL REFERENCES sns_posts(post_id) ON DELETE CASCADE,
                media_type VARCHAR(8) NOT NULL CHECK (media_type IN ('image', 'video')),
                file_path VARCHAR(500) NOT NULL,
                sort_order INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_sns_post_media_post "
            "ON sns_post_media (post_id, sort_order)"
        ))

        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS sns_stories (
                story_id SERIAL PRIMARY KEY,
                account_id INTEGER NOT NULL REFERENCES accounts(account_id),
                media_type VARCHAR(8) NOT NULL CHECK (media_type IN ('image', 'video')),
                file_path VARCHAR(500) NOT NULL,
                caption VARCHAR(300) NOT NULL DEFAULT '',
                is_archived BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                expires_at TIMESTAMPTZ NOT NULL
            )
            """
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_sns_stories_active "
            "ON sns_stories (is_archived, expires_at)"
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_sns_stories_account "
            "ON sns_stories (account_id, created_at DESC)"
        ))

        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS sns_story_views (
                view_id SERIAL PRIMARY KEY,
                story_id INTEGER NOT NULL REFERENCES sns_stories(story_id) ON DELETE CASCADE,
                viewer_account_id INTEGER NOT NULL REFERENCES accounts(account_id),
                viewed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                UNIQUE (story_id, viewer_account_id)
            )
            """
        ))

        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS sns_follows (
                follow_id SERIAL PRIMARY KEY,
                follower_account_id INTEGER NOT NULL REFERENCES accounts(account_id),
                following_account_id INTEGER NOT NULL REFERENCES accounts(account_id),
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                UNIQUE (follower_account_id, following_account_id),
                CHECK (follower_account_id <> following_account_id)
            )
            """
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_sns_follows_following "
            "ON sns_follows (following_account_id)"
        ))

        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS sns_likes (
                like_id SERIAL PRIMARY KEY,
                account_id INTEGER NOT NULL REFERENCES accounts(account_id),
                post_id INTEGER NOT NULL REFERENCES sns_posts(post_id) ON DELETE CASCADE,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                UNIQUE (account_id, post_id)
            )
            """
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_sns_likes_post ON sns_likes (post_id)"
        ))

        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS sns_comments (
                comment_id SERIAL PRIMARY KEY,
                post_id INTEGER NOT NULL REFERENCES sns_posts(post_id) ON DELETE CASCADE,
                account_id INTEGER NOT NULL REFERENCES accounts(account_id),
                body VARCHAR(500) NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                deleted_at TIMESTAMPTZ NULL
            )
            """
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_sns_comments_post "
            "ON sns_comments (post_id, created_at)"
        ))

        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS sns_saved_posts (
                saved_id SERIAL PRIMARY KEY,
                account_id INTEGER NOT NULL REFERENCES accounts(account_id),
                post_id INTEGER NOT NULL REFERENCES sns_posts(post_id) ON DELETE CASCADE,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                UNIQUE (account_id, post_id)
            )
            """
        ))

        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS sns_dm_threads (
                thread_id SERIAL PRIMARY KEY,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        ))

        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS sns_dm_participants (
                participant_id SERIAL PRIMARY KEY,
                thread_id INTEGER NOT NULL REFERENCES sns_dm_threads(thread_id) ON DELETE CASCADE,
                account_id INTEGER NOT NULL REFERENCES accounts(account_id),
                status VARCHAR(16) NOT NULL DEFAULT 'accepted' CHECK (status IN ('accepted', 'requested')),
                last_read_message_id INTEGER NOT NULL DEFAULT 0,
                joined_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                UNIQUE (thread_id, account_id)
            )
            """
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_sns_dm_participants_account "
            "ON sns_dm_participants (account_id)"
        ))

        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS sns_dm_messages (
                message_id SERIAL PRIMARY KEY,
                thread_id INTEGER NOT NULL REFERENCES sns_dm_threads(thread_id) ON DELETE CASCADE,
                sender_account_id INTEGER NOT NULL REFERENCES accounts(account_id),
                message_type VARCHAR(16) NOT NULL DEFAULT 'text'
                    CHECK (message_type IN ('text', 'image', 'post_share', 'story_reply')),
                body TEXT NOT NULL DEFAULT '',
                media_path VARCHAR(500) NULL,
                shared_post_id INTEGER NULL REFERENCES sns_posts(post_id) ON DELETE SET NULL,
                shared_story_id INTEGER NULL REFERENCES sns_stories(story_id) ON DELETE SET NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                deleted_at TIMESTAMPTZ NULL
            )
            """
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_sns_dm_messages_thread "
            "ON sns_dm_messages (thread_id, message_id)"
        ))

        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS sns_blocks (
                block_id SERIAL PRIMARY KEY,
                blocker_account_id INTEGER NOT NULL REFERENCES accounts(account_id),
                blocked_account_id INTEGER NOT NULL REFERENCES accounts(account_id),
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                UNIQUE (blocker_account_id, blocked_account_id),
                CHECK (blocker_account_id <> blocked_account_id)
            )
            """
        ))

        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS sns_reports (
                report_id SERIAL PRIMARY KEY,
                reporter_account_id INTEGER NOT NULL REFERENCES accounts(account_id),
                target_type VARCHAR(16) NOT NULL
                    CHECK (target_type IN ('post', 'comment', 'user', 'dm_message')),
                target_id INTEGER NOT NULL,
                reason VARCHAR(500) NOT NULL,
                status VARCHAR(16) NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending', 'reviewed', 'actioned', 'dismissed')),
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                resolved_at TIMESTAMPTZ NULL
            )
            """
        ))

        # 週間投稿利用状況（ストーリーズ・写真/動画投稿・ひとこと投稿の合計を週単位で管理）
        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS sns_weekly_usage (
                usage_id SERIAL PRIMARY KEY,
                account_id INTEGER NOT NULL REFERENCES accounts(account_id),
                week_start TIMESTAMPTZ NOT NULL,
                post_count INTEGER NOT NULL DEFAULT 0,
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                UNIQUE (account_id, week_start)
            )
            """
        ))


# ---------------------------------------------------------------------------
# 週間投稿回数制限（日本時間・月曜0時起点）
# ---------------------------------------------------------------------------

def get_week_start(now=None):
    """指定時刻が属する「日本時間の月曜0時」を UTC aware datetime で返す"""
    now = now or datetime.now(timezone.utc)
    now_jst = now.astimezone(JST)
    monday_jst = now_jst - timedelta(days=now_jst.weekday())
    monday_jst = monday_jst.replace(hour=0, minute=0, second=0, microsecond=0)
    return monday_jst.astimezone(timezone.utc)


def get_next_week_start(now=None):
    return get_week_start(now) + timedelta(days=7)


def format_reset_label(dt):
    local = dt.astimezone(JST)
    weekday = WEEKDAY_LABELS_JA[local.weekday()]
    return f"{local.month}月{local.day}日（{weekday}）{local.hour}:{local.minute:02d}"


def weekly_limit_for_membership(membership):
    if membership == "premium":
        return None
    if membership == "general":
        return GENERAL_WEEKLY_POST_LIMIT
    return FREE_WEEKLY_POST_LIMIT


def build_sns_usage_status(account_id, membership, engine):
    """フロントエンド表示・投稿フォーム用に現在の利用状況を返す（消費はしない）"""
    limit = weekly_limit_for_membership(membership)
    week_start = get_week_start()
    next_reset = get_next_week_start()

    with engine.connect() as conn:
        row = conn.execute(
            text(
                """
                SELECT post_count FROM sns_weekly_usage
                WHERE account_id = :account_id AND week_start = :week_start
                """
            ),
            {"account_id": account_id, "week_start": week_start},
        ).fetchone()

    used = int(row[0]) if row else 0
    remaining = None if limit is None else max(limit - used, 0)
    can_post = True if limit is None else used < limit

    return {
        "membership": membership,
        "limit": limit,
        "used": used,
        "remaining": remaining,
        "can_post": can_post,
        "week_start": week_start.isoformat(),
        "next_reset_at": next_reset.isoformat(),
        "next_reset_label": format_reset_label(next_reset),
    }


def consume_sns_post_usage(account_id, membership, engine):
    """
    公開処理が正常に完了した時点で1回消費する。
    同時リクエストでも上限を超えないよう、行ロック（SELECT ... FOR UPDATE）を
    1トランザクション内で使用する。
    """
    limit = weekly_limit_for_membership(membership)
    week_start = get_week_start()

    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO sns_weekly_usage (account_id, week_start, post_count)
                VALUES (:account_id, :week_start, 0)
                ON CONFLICT (account_id, week_start) DO NOTHING
                """
            ),
            {"account_id": account_id, "week_start": week_start},
        )

        row = conn.execute(
            text(
                """
                SELECT post_count FROM sns_weekly_usage
                WHERE account_id = :account_id AND week_start = :week_start
                FOR UPDATE
                """
            ),
            {"account_id": account_id, "week_start": week_start},
        ).fetchone()
        used = int(row[0])

        if limit is not None and used >= limit:
            next_reset = get_next_week_start()
            status = {
                "membership": membership,
                "limit": limit,
                "used": used,
                "remaining": 0,
                "can_post": False,
                "week_start": week_start.isoformat(),
                "next_reset_at": next_reset.isoformat(),
                "next_reset_label": format_reset_label(next_reset),
            }
            raise SnsUsageLimitError("今週の投稿可能回数に達しました", status=status)

        new_used = used + 1
        conn.execute(
            text(
                """
                UPDATE sns_weekly_usage
                SET post_count = :new_used, updated_at = NOW()
                WHERE account_id = :account_id AND week_start = :week_start
                """
            ),
            {"new_used": new_used, "account_id": account_id, "week_start": week_start},
        )

    next_reset = get_next_week_start()
    remaining = None if limit is None else max(limit - new_used, 0)
    return {
        "membership": membership,
        "limit": limit,
        "used": new_used,
        "remaining": remaining,
        "can_post": True if limit is None else remaining > 0,
        "week_start": week_start.isoformat(),
        "next_reset_at": next_reset.isoformat(),
        "next_reset_label": format_reset_label(next_reset),
    }


# ---------------------------------------------------------------------------
# ルート登録（open_chat.py の依存注入パターンを踏襲）
# ---------------------------------------------------------------------------

def register_sns_routes(app, engine, **deps):
    get_session_account_id = deps["get_session_account_id"]
    get_membership_for_account = deps["get_membership_for_account"]

    @app.route("/api/sns/usage")
    def sns_get_usage():
        try:
            account_id = get_session_account_id()
        except ValueError:
            return jsonify({"error": "ログインが必要です", "redirect": "/debug/login"}), 401

        try:
            membership = get_membership_for_account(account_id)
            status = build_sns_usage_status(account_id, membership, engine)
            return jsonify(status)
        except Exception as e:
            print(e)
            return jsonify({"error": "利用状況の取得に失敗しました"}), 500
