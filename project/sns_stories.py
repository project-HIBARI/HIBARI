"""
Music Memories SNS フェーズ3: ストーリーズ（一覧・投稿・24時間制御・閲覧履歴・閲覧者一覧）

sns.py / sns_posts.py と同じ依存注入パターンで app.py からルートを登録する。
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from flask import jsonify, request

from sns import SnsUsageLimitError, consume_sns_post_usage

MAX_CAPTION_LENGTH = 300
STORY_LIFETIME_HOURS = 24

BLOCK_EXCLUSION_SQL = """
    NOT EXISTS (
        SELECT 1 FROM sns_blocks b
        WHERE (b.blocker_account_id = :viewer_id AND b.blocked_account_id = s.account_id)
           OR (b.blocker_account_id = s.account_id AND b.blocked_account_id = :viewer_id)
    )
"""

STORY_SELECT = """
    SELECT
        s.story_id, s.account_id, s.media_type, s.file_path, s.caption,
        s.created_at, s.expires_at,
        a.name AS author_name,
        pr.avatar_path AS author_avatar_path,
        EXISTS(
            SELECT 1 FROM sns_story_views v
            WHERE v.story_id = s.story_id AND v.viewer_account_id = :viewer_id
        ) AS viewed_by_viewer
    FROM sns_stories s
    JOIN accounts a ON a.account_id = s.account_id
    LEFT JOIN sns_profiles pr ON pr.account_id = s.account_id
"""


def _row_val(row, key):
    mapping = row._mapping if hasattr(row, "_mapping") else row
    return mapping[key]


def register_sns_story_routes(app, engine, **deps):
    fetch_all = deps["fetch_all"]
    execute = deps["execute"]
    execute_insert = deps["execute_insert"]
    get_session_account_id = deps["get_session_account_id"]
    get_membership_for_account = deps["get_membership_for_account"]

    def _require_login():
        try:
            return get_session_account_id(), None
        except ValueError:
            return None, (jsonify({"error": "ログインが必要です", "redirect": "/debug/login"}), 401)

    def _optional_account_id():
        try:
            return get_session_account_id()
        except ValueError:
            return None

    @app.route("/api/sns/stories", methods=["GET"])
    def sns_get_stories():
        try:
            viewer_id = _optional_account_id()
            where = ["s.is_archived = FALSE", "s.expires_at > NOW()"]
            params = {"viewer_id": viewer_id or 0}
            if viewer_id:
                where.append(BLOCK_EXCLUSION_SQL)

            sql = f"{STORY_SELECT} WHERE {' AND '.join(where)} ORDER BY s.account_id, s.created_at ASC"
            rows = fetch_all(sql, params)

            groups = {}
            order = []
            for row in rows:
                account_id = _row_val(row, "account_id")
                if account_id not in groups:
                    groups[account_id] = {
                        "account_id": account_id,
                        "author_name": _row_val(row, "author_name"),
                        "author_avatar_path": _row_val(row, "author_avatar_path"),
                        "stories": [],
                    }
                    order.append(account_id)
                groups[account_id]["stories"].append({
                    "story_id": _row_val(row, "story_id"),
                    "media_type": _row_val(row, "media_type"),
                    "file_path": _row_val(row, "file_path"),
                    "caption": _row_val(row, "caption"),
                    "created_at": _row_val(row, "created_at").isoformat(),
                    "expires_at": _row_val(row, "expires_at").isoformat(),
                    "viewed_by_viewer": bool(_row_val(row, "viewed_by_viewer")) if viewer_id else False,
                })

            group_list = []
            for account_id in order:
                g = groups[account_id]
                g["has_unviewed"] = any(not s["viewed_by_viewer"] for s in g["stories"])
                g["latest_created_at"] = g["stories"][-1]["created_at"]
                group_list.append(g)

            # stable sort: 最下位キーから順に適用（最新順 → 未読優先 → 自分を先頭）
            group_list.sort(key=lambda g: g["latest_created_at"], reverse=True)
            group_list.sort(key=lambda g: 0 if g["has_unviewed"] else 1)
            group_list.sort(key=lambda g: 0 if (viewer_id is not None and g["account_id"] == viewer_id) else 1)

            return jsonify({"groups": group_list})
        except Exception as e:
            print(e)
            return jsonify({"error": "ストーリーズの取得に失敗しました"}), 500

    @app.route("/api/sns/stories", methods=["POST"])
    def sns_create_story():
        account_id, err = _require_login()
        if err:
            return err

        data = request.get_json(silent=True) or {}
        media_type = data.get("media_type")
        file_path = data.get("file_path")
        caption = (data.get("caption") or "").strip()

        if media_type not in ("image", "video") or not file_path:
            return jsonify({"error": "画像または動画を選択してください"}), 400
        if len(caption) > MAX_CAPTION_LENGTH:
            return jsonify({"error": f"キャプションは{MAX_CAPTION_LENGTH}文字以内で入力してください"}), 400

        membership = get_membership_for_account(account_id)
        try:
            usage_status = consume_sns_post_usage(account_id, membership, engine)
        except SnsUsageLimitError as e:
            return jsonify({"error": e.message, **e.status}), 429

        try:
            now = datetime.now(timezone.utc)
            expires_at = now + timedelta(hours=STORY_LIFETIME_HOURS)
            story_id = execute_insert(
                """
                INSERT INTO sns_stories (account_id, media_type, file_path, caption, expires_at)
                VALUES (:account_id, :media_type, :file_path, :caption, :expires_at)
                RETURNING story_id
                """,
                {
                    "account_id": account_id,
                    "media_type": media_type,
                    "file_path": file_path,
                    "caption": caption,
                    "expires_at": expires_at,
                },
            )
            return jsonify({
                "message": "ストーリーズを投稿しました",
                "story_id": story_id,
                "expires_at": expires_at.isoformat(),
                "usage": usage_status,
            }), 201
        except Exception as e:
            print(e)
            return jsonify({"error": "ストーリーズの投稿に失敗しました"}), 500

    @app.route("/api/sns/stories/mine", methods=["GET"])
    def sns_get_my_story_archive():
        account_id, err = _require_login()
        if err:
            return err

        try:
            rows = fetch_all(
                """
                SELECT story_id, media_type, file_path, caption, created_at, expires_at,
                       (expires_at > NOW() AND is_archived = FALSE) AS is_active
                FROM sns_stories
                WHERE account_id = :account_id
                ORDER BY created_at DESC
                """,
                {"account_id": account_id},
            )
            stories = [{
                "story_id": _row_val(r, "story_id"),
                "media_type": _row_val(r, "media_type"),
                "file_path": _row_val(r, "file_path"),
                "caption": _row_val(r, "caption"),
                "created_at": _row_val(r, "created_at").isoformat(),
                "expires_at": _row_val(r, "expires_at").isoformat(),
                "is_active": bool(_row_val(r, "is_active")),
            } for r in rows]
            return jsonify({"stories": stories})
        except Exception as e:
            print(e)
            return jsonify({"error": "アーカイブの取得に失敗しました"}), 500

    @app.route("/api/sns/stories/<int:story_id>", methods=["DELETE"])
    def sns_delete_story(story_id):
        account_id, err = _require_login()
        if err:
            return err

        rows = fetch_all(
            "SELECT account_id FROM sns_stories WHERE story_id = :story_id",
            {"story_id": story_id},
        )
        if not rows:
            return jsonify({"error": "ストーリーズが見つかりません"}), 404
        if _row_val(rows[0], "account_id") != account_id:
            return jsonify({"error": "このストーリーズを削除する権限がありません"}), 403

        try:
            execute("DELETE FROM sns_stories WHERE story_id = :story_id", {"story_id": story_id})
            return jsonify({"message": "削除しました"})
        except Exception as e:
            print(e)
            return jsonify({"error": "削除に失敗しました"}), 500

    @app.route("/api/sns/stories/<int:story_id>/view", methods=["POST"])
    def sns_record_story_view(story_id):
        account_id, err = _require_login()
        if err:
            return err

        rows = fetch_all(
            "SELECT account_id FROM sns_stories WHERE story_id = :story_id "
            "AND is_archived = FALSE AND expires_at > NOW()",
            {"story_id": story_id},
        )
        if not rows:
            return jsonify({"error": "ストーリーズが見つかりません"}), 404

        owner_id = _row_val(rows[0], "account_id")
        if owner_id == account_id:
            return jsonify({"message": "OK"})

        try:
            execute(
                """
                INSERT INTO sns_story_views (story_id, viewer_account_id)
                VALUES (:story_id, :viewer_account_id)
                ON CONFLICT (story_id, viewer_account_id) DO NOTHING
                """,
                {"story_id": story_id, "viewer_account_id": account_id},
            )
            return jsonify({"message": "OK"})
        except Exception as e:
            print(e)
            return jsonify({"error": "閲覧記録の保存に失敗しました"}), 500

    @app.route("/api/sns/stories/<int:story_id>/viewers", methods=["GET"])
    def sns_get_story_viewers(story_id):
        account_id, err = _require_login()
        if err:
            return err

        rows = fetch_all(
            "SELECT account_id FROM sns_stories WHERE story_id = :story_id",
            {"story_id": story_id},
        )
        if not rows:
            return jsonify({"error": "ストーリーズが見つかりません"}), 404
        if _row_val(rows[0], "account_id") != account_id:
            return jsonify({"error": "自分のストーリーズの閲覧者のみ確認できます"}), 403

        try:
            viewer_rows = fetch_all(
                """
                SELECT v.viewer_account_id, v.viewed_at, a.name AS viewer_name,
                       pr.avatar_path AS viewer_avatar_path
                FROM sns_story_views v
                JOIN accounts a ON a.account_id = v.viewer_account_id
                LEFT JOIN sns_profiles pr ON pr.account_id = v.viewer_account_id
                WHERE v.story_id = :story_id
                ORDER BY v.viewed_at DESC
                """,
                {"story_id": story_id},
            )
            viewers = [{
                "account_id": _row_val(r, "viewer_account_id"),
                "name": _row_val(r, "viewer_name"),
                "avatar_path": _row_val(r, "viewer_avatar_path"),
                "viewed_at": _row_val(r, "viewed_at").isoformat(),
            } for r in viewer_rows]
            return jsonify({"viewers": viewers, "count": len(viewers)})
        except Exception as e:
            print(e)
            return jsonify({"error": "閲覧者の取得に失敗しました"}), 500
