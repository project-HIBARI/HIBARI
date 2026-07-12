"""
Music Memories SNS フェーズ5: ダイレクトメッセージ（1対1）

sns.py と同じ依存注入パターンで app.py からルートを登録する。
"""
from __future__ import annotations

import os
import uuid

from flask import jsonify, request
from werkzeug.utils import secure_filename

from sns_posts import ALLOWED_IMAGE_EXTENSIONS, MAX_IMAGE_BYTES, SNS_UPLOAD_FOLDER

MAX_MESSAGE_LENGTH = 2000
THREADS_PAGE_SIZE = 30
MESSAGES_PAGE_SIZE = 40
SEARCH_LIMIT = 20


def _row_val(row, key):
    mapping = row._mapping if hasattr(row, "_mapping") else row
    return mapping[key]


def register_sns_dm_routes(app, engine, **deps):
    fetch_all = deps["fetch_all"]
    execute = deps["execute"]
    execute_insert = deps["execute_insert"]
    get_session_account_id = deps["get_session_account_id"]
    fetch_account_row = deps["fetch_account_row"]

    def _require_login():
        try:
            return get_session_account_id(), None
        except ValueError:
            return None, (jsonify({"error": "ログインが必要です", "redirect": "/debug/login"}), 401)

    def _is_blocked(a, b):
        rows = fetch_all(
            """
            SELECT 1 FROM sns_blocks
            WHERE (blocker_account_id = :a AND blocked_account_id = :b)
               OR (blocker_account_id = :b AND blocked_account_id = :a)
            """,
            {"a": a, "b": b},
        )
        return bool(rows)

    def _is_mutual_follow(a, b):
        rows = fetch_all(
            """
            SELECT 1 FROM sns_follows f1
            WHERE f1.follower_account_id = :a AND f1.following_account_id = :b
              AND EXISTS (
                  SELECT 1 FROM sns_follows f2
                  WHERE f2.follower_account_id = :b AND f2.following_account_id = :a
              )
            """,
            {"a": a, "b": b},
        )
        return bool(rows)

    def _get_participant(thread_id, account_id):
        rows = fetch_all(
            "SELECT * FROM sns_dm_participants WHERE thread_id = :thread_id AND account_id = :account_id",
            {"thread_id": thread_id, "account_id": account_id},
        )
        return rows[0] if rows else None

    def _find_thread_id(a, b):
        rows = fetch_all(
            """
            SELECT p1.thread_id
            FROM sns_dm_participants p1
            JOIN sns_dm_participants p2 ON p2.thread_id = p1.thread_id
            WHERE p1.account_id = :a AND p2.account_id = :b
            """,
            {"a": a, "b": b},
        )
        return _row_val(rows[0], "thread_id") if rows else None

    def _other_participant(thread_id, account_id):
        rows = fetch_all(
            """
            SELECT dp.account_id, a.name, pr.avatar_path
            FROM sns_dm_participants dp
            JOIN accounts a ON a.account_id = dp.account_id
            LEFT JOIN sns_profiles pr ON pr.account_id = dp.account_id
            WHERE dp.thread_id = :thread_id AND dp.account_id != :account_id
            """,
            {"thread_id": thread_id, "account_id": account_id},
        )
        if not rows:
            return None
        return {
            "account_id": _row_val(rows[0], "account_id"),
            "name": _row_val(rows[0], "name"),
            "avatar_path": _row_val(rows[0], "avatar_path"),
        }

    def _ensure_thread(sender_id, recipient_id):
        thread_id = _find_thread_id(sender_id, recipient_id)
        if thread_id:
            return thread_id, False

        thread_id = execute_insert(
            "INSERT INTO sns_dm_threads DEFAULT VALUES RETURNING thread_id", {}
        )
        mutual = _is_mutual_follow(sender_id, recipient_id)
        execute(
            """
            INSERT INTO sns_dm_participants (thread_id, account_id, status)
            VALUES (:thread_id, :sender_id, 'accepted')
            """,
            {"thread_id": thread_id, "sender_id": sender_id},
        )
        execute(
            """
            INSERT INTO sns_dm_participants (thread_id, account_id, status)
            VALUES (:thread_id, :recipient_id, :status)
            """,
            {
                "thread_id": thread_id,
                "recipient_id": recipient_id,
                "status": "accepted" if mutual else "requested",
            },
        )
        return thread_id, True

    def _serialize_message(row, viewer_id):
        m = row._mapping if hasattr(row, "_mapping") else row
        return {
            "message_id": m["message_id"],
            "thread_id": m["thread_id"],
            "sender_account_id": m["sender_account_id"],
            "message_type": m["message_type"],
            "body": m["body"],
            "media_path": m["media_path"],
            "shared_post_id": m["shared_post_id"],
            "shared_story_id": m["shared_story_id"],
            "created_at": m["created_at"].isoformat(),
            "is_mine": m["sender_account_id"] == viewer_id,
        }

    @app.route("/api/sns/dm/media/upload", methods=["POST"])
    def sns_dm_upload_media():
        account_id, err = _require_login()
        if err:
            return err

        file = request.files.get("file")
        if not file or not file.filename:
            return jsonify({"error": "ファイルがありません"}), 400

        original_name = secure_filename(file.filename)
        ext = original_name.rsplit(".", 1)[-1].lower() if "." in original_name else ""
        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            return jsonify({"error": "画像形式（jpg/png/gif/webp）のみ送信できます"}), 400

        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        if size > MAX_IMAGE_BYTES or size == 0:
            return jsonify({"error": "ファイルサイズは10MB以下にしてください"}), 400

        stored_name = f"{uuid.uuid4().hex}.{ext}"
        save_path = SNS_UPLOAD_FOLDER / stored_name
        file.save(str(save_path))
        return jsonify({"path": f"/uploads/sns/{stored_name}"})

    @app.route("/api/sns/dm/search", methods=["GET"])
    def sns_dm_search_users():
        account_id, err = _require_login()
        if err:
            return err

        q = (request.args.get("q") or "").strip()
        if not q:
            return jsonify({"users": []})

        rows = fetch_all(
            """
            SELECT a.account_id, a.name, pr.avatar_path
            FROM accounts a
            LEFT JOIN sns_profiles pr ON pr.account_id = a.account_id
            WHERE a.account_id != :account_id
              AND a.name ILIKE :q
              AND NOT EXISTS (
                  SELECT 1 FROM sns_blocks b
                  WHERE (b.blocker_account_id = :account_id AND b.blocked_account_id = a.account_id)
                     OR (b.blocker_account_id = a.account_id AND b.blocked_account_id = :account_id)
              )
            ORDER BY a.name
            LIMIT :limit
            """,
            {"account_id": account_id, "q": f"%{q}%", "limit": SEARCH_LIMIT},
        )
        users = [{
            "account_id": _row_val(r, "account_id"),
            "name": _row_val(r, "name"),
            "avatar_path": _row_val(r, "avatar_path"),
        } for r in rows]
        return jsonify({"users": users})

    @app.route("/api/sns/dm/threads", methods=["GET"])
    def sns_dm_list_threads():
        account_id, err = _require_login()
        if err:
            return err

        box = request.args.get("box", "inbox")
        status_filter = "accepted" if box != "requests" else "requested"

        rows = fetch_all(
            """
            SELECT dp.thread_id, dp.last_read_message_id
            FROM sns_dm_participants dp
            WHERE dp.account_id = :account_id AND dp.status = :status
            """,
            {"account_id": account_id, "status": status_filter},
        )

        threads = []
        for r in rows:
            thread_id = _row_val(r, "thread_id")
            last_read = _row_val(r, "last_read_message_id")
            other = _other_participant(thread_id, account_id)
            if not other:
                continue

            last_msg_rows = fetch_all(
                """
                SELECT message_id, body, message_type, created_at, sender_account_id
                FROM sns_dm_messages
                WHERE thread_id = :thread_id AND deleted_at IS NULL
                ORDER BY message_id DESC LIMIT 1
                """,
                {"thread_id": thread_id},
            )
            unread_row = fetch_all(
                """
                SELECT COUNT(*) AS c FROM sns_dm_messages
                WHERE thread_id = :thread_id AND deleted_at IS NULL
                  AND sender_account_id != :account_id
                  AND message_id > :last_read
                """,
                {"thread_id": thread_id, "account_id": account_id, "last_read": last_read},
            )

            last_message = None
            updated_at = None
            if last_msg_rows:
                lm = last_msg_rows[0]
                last_message = {
                    "body": _row_val(lm, "body"),
                    "message_type": _row_val(lm, "message_type"),
                    "is_mine": _row_val(lm, "sender_account_id") == account_id,
                }
                updated_at = _row_val(lm, "created_at").isoformat()

            threads.append({
                "thread_id": thread_id,
                "other": other,
                "last_message": last_message,
                "updated_at": updated_at,
                "unread_count": int(_row_val(unread_row[0], "c")),
            })

        threads.sort(key=lambda t: t["updated_at"] or "", reverse=True)
        return jsonify({"threads": threads})

    @app.route("/api/sns/dm/threads/<int:thread_id>", methods=["GET"])
    def sns_dm_get_thread(thread_id):
        account_id, err = _require_login()
        if err:
            return err

        participant = _get_participant(thread_id, account_id)
        if not participant:
            return jsonify({"error": "スレッドが見つかりません"}), 404

        other = _other_participant(thread_id, account_id)
        before_id = request.args.get("before_id", type=int)
        where = ["thread_id = :thread_id"]
        params = {"thread_id": thread_id, "limit": MESSAGES_PAGE_SIZE}
        if before_id:
            where.append("message_id < :before_id")
            params["before_id"] = before_id

        rows = fetch_all(
            f"""
            SELECT message_id, thread_id, sender_account_id, message_type, body,
                   media_path, shared_post_id, shared_story_id, created_at, deleted_at
            FROM sns_dm_messages
            WHERE {' AND '.join(where)}
            ORDER BY message_id DESC
            LIMIT :limit
            """,
            params,
        )
        messages = []
        for r in rows:
            m = r._mapping if hasattr(r, "_mapping") else r
            if m["deleted_at"] is not None:
                messages.append({
                    "message_id": m["message_id"],
                    "thread_id": m["thread_id"],
                    "sender_account_id": m["sender_account_id"],
                    "message_type": "deleted",
                    "body": "",
                    "media_path": None,
                    "shared_post_id": None,
                    "shared_story_id": None,
                    "created_at": m["created_at"].isoformat(),
                    "is_mine": m["sender_account_id"] == account_id,
                })
            else:
                messages.append(_serialize_message(r, account_id))
        messages.reverse()
        next_cursor = messages[0]["message_id"] if len(messages) == MESSAGES_PAGE_SIZE else None

        blocked = _is_blocked(account_id, other["account_id"]) if other else False

        return jsonify({
            "thread_id": thread_id,
            "other": other,
            "status": _row_val(participant, "status"),
            "blocked": blocked,
            "messages": messages,
            "next_before_id": next_cursor,
        })

    @app.route("/api/sns/dm/threads/<int:thread_id>/read", methods=["POST"])
    def sns_dm_mark_read(thread_id):
        account_id, err = _require_login()
        if err:
            return err

        participant = _get_participant(thread_id, account_id)
        if not participant:
            return jsonify({"error": "スレッドが見つかりません"}), 404

        latest_rows = fetch_all(
            "SELECT MAX(message_id) AS m FROM sns_dm_messages WHERE thread_id = :thread_id",
            {"thread_id": thread_id},
        )
        latest_id = _row_val(latest_rows[0], "m") or 0

        try:
            execute(
                """
                UPDATE sns_dm_participants
                SET last_read_message_id = :latest_id,
                    status = CASE WHEN status = 'requested' THEN 'accepted' ELSE status END
                WHERE thread_id = :thread_id AND account_id = :account_id
                """,
                {"latest_id": latest_id, "thread_id": thread_id, "account_id": account_id},
            )
            return jsonify({"message": "OK"})
        except Exception as e:
            print(e)
            return jsonify({"error": "既読の更新に失敗しました"}), 500

    def _send_message(sender_id, recipient_id, message_type, body, media_path, shared_post_id, shared_story_id):
        if sender_id == recipient_id:
            raise ValueError("自分自身にはメッセージを送信できません")
        if _is_blocked(sender_id, recipient_id):
            raise PermissionError("ブロック中のユーザーとはメッセージを送受信できません")

        thread_id, _created = _ensure_thread(sender_id, recipient_id)

        message_id = execute_insert(
            """
            INSERT INTO sns_dm_messages (
                thread_id, sender_account_id, message_type, body,
                media_path, shared_post_id, shared_story_id
            )
            VALUES (:thread_id, :sender_id, :message_type, :body, :media_path, :shared_post_id, :shared_story_id)
            RETURNING message_id
            """,
            {
                "thread_id": thread_id,
                "sender_id": sender_id,
                "message_type": message_type,
                "body": body,
                "media_path": media_path,
                "shared_post_id": shared_post_id,
                "shared_story_id": shared_story_id,
            },
        )

        # 送信者側は常に既読扱いにする
        execute(
            """
            UPDATE sns_dm_participants
            SET last_read_message_id = :message_id,
                status = CASE WHEN status = 'requested' THEN 'accepted' ELSE status END
            WHERE thread_id = :thread_id AND account_id = :sender_id
            """,
            {"message_id": message_id, "thread_id": thread_id, "sender_id": sender_id},
        )

        return thread_id, message_id

    @app.route("/api/sns/dm/send", methods=["POST"])
    def sns_dm_send():
        account_id, err = _require_login()
        if err:
            return err

        data = request.get_json(silent=True) or {}
        recipient_id = data.get("recipient_id")
        message_type = data.get("message_type", "text")
        body = (data.get("body") or "").strip()
        media_path = data.get("media_path")
        shared_post_id = data.get("shared_post_id")
        shared_story_id = data.get("shared_story_id")

        if not isinstance(recipient_id, int):
            return jsonify({"error": "送信先を指定してください"}), 400
        if message_type not in ("text", "image", "post_share", "story_reply"):
            return jsonify({"error": "メッセージ種別が不正です"}), 400
        if message_type == "text" and not body:
            return jsonify({"error": "メッセージを入力してください"}), 400
        if message_type == "image" and not media_path:
            return jsonify({"error": "画像を選択してください"}), 400
        if message_type == "post_share" and not shared_post_id:
            return jsonify({"error": "共有する投稿を指定してください"}), 400
        if message_type == "story_reply" and not shared_story_id:
            return jsonify({"error": "返信するストーリーズを指定してください"}), 400
        if len(body) > MAX_MESSAGE_LENGTH:
            return jsonify({"error": f"メッセージは{MAX_MESSAGE_LENGTH}文字以内で入力してください"}), 400

        recipient = fetch_account_row(recipient_id)
        if not recipient:
            return jsonify({"error": "送信先ユーザーが見つかりません"}), 404

        try:
            thread_id, message_id = _send_message(
                account_id, recipient_id, message_type, body, media_path, shared_post_id, shared_story_id
            )
            return jsonify({"thread_id": thread_id, "message_id": message_id}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except PermissionError as e:
            return jsonify({"error": str(e)}), 403
        except Exception as e:
            print(e)
            return jsonify({"error": "メッセージの送信に失敗しました"}), 500

    @app.route("/api/sns/dm/threads/<int:thread_id>/messages", methods=["POST"])
    def sns_dm_send_in_thread(thread_id):
        account_id, err = _require_login()
        if err:
            return err

        participant = _get_participant(thread_id, account_id)
        if not participant:
            return jsonify({"error": "スレッドが見つかりません"}), 404

        other = _other_participant(thread_id, account_id)
        if not other:
            return jsonify({"error": "スレッドが見つかりません"}), 404

        data = request.get_json(silent=True) or {}
        message_type = data.get("message_type", "text")
        body = (data.get("body") or "").strip()
        media_path = data.get("media_path")
        shared_post_id = data.get("shared_post_id")
        shared_story_id = data.get("shared_story_id")

        if message_type not in ("text", "image", "post_share", "story_reply"):
            return jsonify({"error": "メッセージ種別が不正です"}), 400
        if message_type == "text" and not body:
            return jsonify({"error": "メッセージを入力してください"}), 400
        if len(body) > MAX_MESSAGE_LENGTH:
            return jsonify({"error": f"メッセージは{MAX_MESSAGE_LENGTH}文字以内で入力してください"}), 400

        try:
            _thread_id, message_id = _send_message(
                account_id, other["account_id"], message_type, body, media_path, shared_post_id, shared_story_id
            )
            return jsonify({"thread_id": thread_id, "message_id": message_id}), 201
        except PermissionError as e:
            return jsonify({"error": str(e)}), 403
        except Exception as e:
            print(e)
            return jsonify({"error": "メッセージの送信に失敗しました"}), 500

    @app.route("/api/sns/dm/messages/<int:message_id>", methods=["DELETE"])
    def sns_dm_delete_message(message_id):
        account_id, err = _require_login()
        if err:
            return err

        rows = fetch_all(
            "SELECT sender_account_id, thread_id FROM sns_dm_messages WHERE message_id = :id",
            {"id": message_id},
        )
        if not rows:
            return jsonify({"error": "メッセージが見つかりません"}), 404
        if _row_val(rows[0], "sender_account_id") != account_id:
            return jsonify({"error": "このメッセージを削除する権限がありません"}), 403

        try:
            execute(
                "UPDATE sns_dm_messages SET deleted_at = NOW() WHERE message_id = :id",
                {"id": message_id},
            )
            return jsonify({"message": "削除しました"})
        except Exception as e:
            print(e)
            return jsonify({"error": "削除に失敗しました"}), 500

    @app.route("/api/sns/dm/unread-count", methods=["GET"])
    def sns_dm_unread_count():
        account_id, err = _require_login()
        if err:
            return err

        rows = fetch_all(
            """
            SELECT dp.thread_id, dp.last_read_message_id,
                   (SELECT COUNT(*) FROM sns_dm_messages m
                    WHERE m.thread_id = dp.thread_id AND m.deleted_at IS NULL
                      AND m.sender_account_id != :account_id
                      AND m.message_id > dp.last_read_message_id) AS unread
            FROM sns_dm_participants dp
            WHERE dp.account_id = :account_id AND dp.status = 'accepted'
            """,
            {"account_id": account_id},
        )
        total = sum(int(_row_val(r, "unread")) for r in rows)
        return jsonify({"unread_count": total})
