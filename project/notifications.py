"""
Music Memories SNS 通知機能: 通知一覧 / 未読件数 / 既読化 API

sns.py と同じ依存注入パターンで app.py からルートを登録する。
通知の作成は各イベント（いいね/コメント/フォロー/DM）側から notification_service を通じて行い、
ここでは自分宛ての通知の参照・既読化のみを扱う。
"""
from __future__ import annotations

from flask import jsonify, request

from notification_service import NOTIFICATIONS_PAGE_SIZE, format_notification_message


def _row_val(row, key):
    mapping = row._mapping if hasattr(row, "_mapping") else row
    return mapping[key]


NOTIFICATION_SELECT = """
    SELECT
        n.notification_id, n.notification_type, n.is_read, n.created_at,
        n.post_id, n.comment_id, n.story_id, n.message_id, n.thread_id,
        n.actor_account_id, a.name AS actor_name, pr.avatar_path AS actor_avatar_path,
        p.is_deleted AS post_is_deleted,
        (SELECT pm.file_path FROM sns_post_media pm
            WHERE pm.post_id = n.post_id ORDER BY pm.sort_order LIMIT 1) AS post_thumbnail_path,
        (n.comment_id IS NOT NULL AND c.comment_id IS NULL) AS comment_missing
    FROM sns_notifications n
    JOIN accounts a ON a.account_id = n.actor_account_id
    LEFT JOIN sns_profiles pr ON pr.account_id = n.actor_account_id
    LEFT JOIN sns_posts p ON p.post_id = n.post_id
    LEFT JOIN sns_comments c ON c.comment_id = n.comment_id AND c.deleted_at IS NULL
"""


def register_notification_routes(app, engine, **deps):
    fetch_all = deps["fetch_all"]
    execute = deps["execute"]
    get_session_account_id = deps["get_session_account_id"]

    def _require_login():
        try:
            return get_session_account_id(), None
        except ValueError:
            return None, (jsonify({"error": "ログインが必要です", "redirect": "/debug/login"}), 401)

    def _serialize(row):
        notification_type = _row_val(row, "notification_type")
        actor_name = _row_val(row, "actor_name")
        post_id = _row_val(row, "post_id")
        post_is_deleted = _row_val(row, "post_is_deleted")
        target_deleted = bool(post_id and (post_is_deleted is None or post_is_deleted)) or bool(
            _row_val(row, "comment_missing")
        )
        return {
            "notification_id": _row_val(row, "notification_id"),
            "notification_type": notification_type,
            "is_read": bool(_row_val(row, "is_read")),
            "created_at": _row_val(row, "created_at").isoformat(),
            "actor_account_id": _row_val(row, "actor_account_id"),
            "actor_name": actor_name,
            "actor_avatar_path": _row_val(row, "actor_avatar_path"),
            "post_id": post_id,
            "comment_id": _row_val(row, "comment_id"),
            "story_id": _row_val(row, "story_id"),
            "message_id": _row_val(row, "message_id"),
            "thread_id": _row_val(row, "thread_id"),
            "post_thumbnail_path": _row_val(row, "post_thumbnail_path"),
            "target_deleted": target_deleted,
            "message": format_notification_message(notification_type, actor_name),
        }

    @app.route("/api/notifications", methods=["GET"])
    def sns_get_notifications():
        account_id, err = _require_login()
        if err:
            return err

        cursor = request.args.get("cursor", type=int)
        limit = request.args.get("limit", type=int) or NOTIFICATIONS_PAGE_SIZE
        limit = max(1, min(limit, 50))

        where = ["n.recipient_account_id = :account_id"]
        params = {"account_id": account_id, "limit": limit}
        if cursor:
            where.append("n.notification_id < :cursor")
            params["cursor"] = cursor

        try:
            sql = f"{NOTIFICATION_SELECT} WHERE {' AND '.join(where)} ORDER BY n.notification_id DESC LIMIT :limit"
            rows = fetch_all(sql, params)
            notifications = [_serialize(r) for r in rows]
            next_cursor = notifications[-1]["notification_id"] if len(notifications) == limit else None
            return jsonify({"notifications": notifications, "next_cursor": next_cursor})
        except Exception as e:
            print(e)
            return jsonify({"error": "通知の取得に失敗しました"}), 500

    @app.route("/api/notifications/unread-count", methods=["GET"])
    def sns_get_notifications_unread_count():
        account_id, err = _require_login()
        if err:
            return err

        rows = fetch_all(
            "SELECT COUNT(*) AS c FROM sns_notifications WHERE recipient_account_id = :account_id AND is_read = FALSE",
            {"account_id": account_id},
        )
        return jsonify({"unread_count": int(_row_val(rows[0], "c"))})

    @app.route("/api/notifications/<int:notification_id>/read", methods=["POST"])
    def sns_mark_notification_read(notification_id):
        account_id, err = _require_login()
        if err:
            return err

        rows = fetch_all(
            "SELECT recipient_account_id FROM sns_notifications WHERE notification_id = :id",
            {"id": notification_id},
        )
        if not rows:
            return jsonify({"error": "通知が見つかりません"}), 404
        if _row_val(rows[0], "recipient_account_id") != account_id:
            return jsonify({"error": "この通知を操作する権限がありません"}), 403

        try:
            execute(
                """
                UPDATE sns_notifications
                SET is_read = TRUE, read_at = NOW()
                WHERE notification_id = :id AND is_read = FALSE
                """,
                {"id": notification_id},
            )
            return jsonify({"message": "OK"})
        except Exception as e:
            print(e)
            return jsonify({"error": "既読の更新に失敗しました"}), 500

    @app.route("/api/notifications/read-all", methods=["POST"])
    def sns_mark_all_notifications_read():
        account_id, err = _require_login()
        if err:
            return err

        try:
            execute(
                """
                UPDATE sns_notifications
                SET is_read = TRUE, read_at = NOW()
                WHERE recipient_account_id = :account_id AND is_read = FALSE
                """,
                {"account_id": account_id},
            )
            return jsonify({"message": "OK"})
        except Exception as e:
            print(e)
            return jsonify({"error": "既読の更新に失敗しました"}), 500
