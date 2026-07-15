"""
Music Memories SNS 通知機能: テーブル定義と作成/集計の共通ロジック

各ルート（いいね・コメント・フォロー・DM）から呼び出される共通関数群。
notification_type を文字列でばらばらに書かないよう、ここで定数化する。
"""
from __future__ import annotations

from sqlalchemy import text

NOTIFICATION_TYPE_POST_LIKE = "post_like"
NOTIFICATION_TYPE_POST_COMMENT = "post_comment"
NOTIFICATION_TYPE_FOLLOW = "follow"
NOTIFICATION_TYPE_DM_MESSAGE = "dm_message"
NOTIFICATION_TYPE_DM_REQUEST = "dm_request"
NOTIFICATION_TYPE_STORY_REACTION = "story_reaction"
NOTIFICATION_TYPE_STORY_REPLY = "story_reply"

NOTIFICATION_TYPES = (
    NOTIFICATION_TYPE_POST_LIKE,
    NOTIFICATION_TYPE_POST_COMMENT,
    NOTIFICATION_TYPE_FOLLOW,
    NOTIFICATION_TYPE_DM_MESSAGE,
    NOTIFICATION_TYPE_DM_REQUEST,
    NOTIFICATION_TYPE_STORY_REACTION,
    NOTIFICATION_TYPE_STORY_REPLY,
)

NOTIFICATIONS_PAGE_SIZE = 20

# ストーリーへ送信できるリアクション絵文字のホワイトリスト（任意文字列を保存しないため）
STORY_REACTION_EMOJI = ("❤️", "🔥", "👏", "😂", "😢", "😮")

NOTIFICATION_MESSAGE_TEMPLATES = {
    NOTIFICATION_TYPE_POST_LIKE: "{actor}さんがあなたの投稿にいいねしました",
    NOTIFICATION_TYPE_POST_COMMENT: "{actor}さんがコメントしました",
    NOTIFICATION_TYPE_FOLLOW: "{actor}さんにフォローされました",
    NOTIFICATION_TYPE_DM_MESSAGE: "{actor}さんからメッセージが届きました",
    NOTIFICATION_TYPE_DM_REQUEST: "{actor}さんからメッセージリクエストが届きました",
    NOTIFICATION_TYPE_STORY_REACTION: "{actor}さんがストーリーズにリアクションしました",
    NOTIFICATION_TYPE_STORY_REPLY: "{actor}さんがストーリーズに返信しました",
}


def _row_val(row, key):
    mapping = row._mapping if hasattr(row, "_mapping") else row
    return mapping[key]


def ensure_notification_schema(engine):
    with engine.begin() as conn:
        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS sns_notifications (
                notification_id SERIAL PRIMARY KEY,
                recipient_account_id INTEGER NOT NULL REFERENCES accounts(account_id),
                actor_account_id INTEGER NOT NULL REFERENCES accounts(account_id),
                notification_type VARCHAR(24) NOT NULL,
                post_id INTEGER NULL REFERENCES sns_posts(post_id) ON DELETE CASCADE,
                comment_id INTEGER NULL REFERENCES sns_comments(comment_id) ON DELETE CASCADE,
                story_id INTEGER NULL REFERENCES sns_stories(story_id) ON DELETE CASCADE,
                message_id INTEGER NULL REFERENCES sns_dm_messages(message_id) ON DELETE CASCADE,
                thread_id INTEGER NULL REFERENCES sns_dm_threads(thread_id) ON DELETE CASCADE,
                is_read BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                read_at TIMESTAMPTZ NULL
            )
            """
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_sns_notifications_recipient "
            "ON sns_notifications (recipient_account_id, created_at DESC)"
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_sns_notifications_recipient_unread "
            "ON sns_notifications (recipient_account_id, is_read)"
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_sns_notifications_actor "
            "ON sns_notifications (actor_account_id)"
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_sns_notifications_type "
            "ON sns_notifications (notification_type)"
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_sns_notifications_post "
            "ON sns_notifications (post_id)"
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_sns_notifications_thread "
            "ON sns_notifications (thread_id)"
        ))

        # sns_dm_messages: ストーリーリアクション対応（既存 CHECK 制約の拡張 + 絵文字カラム追加）
        conn.execute(text(
            "ALTER TABLE sns_dm_messages DROP CONSTRAINT IF EXISTS sns_dm_messages_message_type_check"
        ))
        conn.execute(text(
            """
            ALTER TABLE sns_dm_messages ADD CONSTRAINT sns_dm_messages_message_type_check
                CHECK (message_type IN ('text', 'image', 'post_share', 'story_reply', 'story_reaction'))
            """
        ))
        conn.execute(text(
            "ALTER TABLE sns_dm_messages ADD COLUMN IF NOT EXISTS reaction_emoji VARCHAR(8) NULL"
        ))


def create_notification(engine, recipient_id, actor_id, notification_type, *,
                         post_id=None, comment_id=None, story_id=None,
                         message_id=None, thread_id=None):
    """一発系イベント（コメント・DM・ストーリー返信/リアクション）用の通知作成。
    自分自身へのイベントは通知を作らない。"""
    if recipient_id is None or actor_id is None or recipient_id == actor_id:
        return None
    with engine.begin() as conn:
        return conn.execute(
            text(
                """
                INSERT INTO sns_notifications (
                    recipient_account_id, actor_account_id, notification_type,
                    post_id, comment_id, story_id, message_id, thread_id
                )
                VALUES (:recipient_id, :actor_id, :notification_type,
                        :post_id, :comment_id, :story_id, :message_id, :thread_id)
                RETURNING notification_id
                """
            ),
            {
                "recipient_id": recipient_id,
                "actor_id": actor_id,
                "notification_type": notification_type,
                "post_id": post_id,
                "comment_id": comment_id,
                "story_id": story_id,
                "message_id": message_id,
                "thread_id": thread_id,
            },
        ).scalar()


def upsert_toggle_notification(engine, recipient_id, actor_id, notification_type, *, post_id=None):
    """いいね/フォローのようなトグル系イベント用。
    同じ (recipient, actor, type, post_id) の通知が既にあれば再利用し、複数作成しない。"""
    if recipient_id is None or actor_id is None or recipient_id == actor_id:
        return None
    with engine.begin() as conn:
        existing = conn.execute(
            text(
                """
                SELECT notification_id FROM sns_notifications
                WHERE recipient_account_id = :recipient_id
                  AND actor_account_id = :actor_id
                  AND notification_type = :notification_type
                  AND post_id IS NOT DISTINCT FROM :post_id
                """
            ),
            {
                "recipient_id": recipient_id,
                "actor_id": actor_id,
                "notification_type": notification_type,
                "post_id": post_id,
            },
        ).fetchone()
        if existing:
            notification_id = _row_val(existing, "notification_id")
            conn.execute(
                text(
                    """
                    UPDATE sns_notifications
                    SET is_read = FALSE, created_at = NOW(), read_at = NULL
                    WHERE notification_id = :id
                    """
                ),
                {"id": notification_id},
            )
            return notification_id
        return conn.execute(
            text(
                """
                INSERT INTO sns_notifications (
                    recipient_account_id, actor_account_id, notification_type, post_id
                )
                VALUES (:recipient_id, :actor_id, :notification_type, :post_id)
                RETURNING notification_id
                """
            ),
            {
                "recipient_id": recipient_id,
                "actor_id": actor_id,
                "notification_type": notification_type,
                "post_id": post_id,
            },
        ).scalar()


def delete_toggle_notification_if_unread(engine, recipient_id, actor_id, notification_type, *, post_id=None):
    """いいね解除/フォロー解除時。未読の通知のみ削除し、既読済みは履歴として残す。"""
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                DELETE FROM sns_notifications
                WHERE recipient_account_id = :recipient_id
                  AND actor_account_id = :actor_id
                  AND notification_type = :notification_type
                  AND post_id IS NOT DISTINCT FROM :post_id
                  AND is_read = FALSE
                """
            ),
            {
                "recipient_id": recipient_id,
                "actor_id": actor_id,
                "notification_type": notification_type,
                "post_id": post_id,
            },
        )


def format_notification_message(notification_type, actor_name):
    template = NOTIFICATION_MESSAGE_TEMPLATES.get(notification_type, "{actor}さんから通知が届きました")
    return template.format(actor=actor_name or "不明なユーザー")
