"""
Music Memories SNS フェーズ2: フィード / 投稿(写真・動画 / ひとこと) / いいね / コメント / 保存

sns.py と同じ依存注入パターン（register_sns_post_routes(app, engine, **deps)）で
app.py からルートを登録する。
"""
from __future__ import annotations

import os
import re
import uuid
from pathlib import Path

from flask import jsonify, request, send_from_directory
from sqlalchemy import text
from werkzeug.utils import secure_filename

from sns import SnsUsageLimitError, build_sns_usage_status, consume_sns_post_usage

BASE_DIR = Path(__file__).resolve().parent
SNS_UPLOAD_FOLDER = BASE_DIR / "uploads" / "sns"
ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "webm", "mov"}
MAX_IMAGE_BYTES = 10 * 1024 * 1024
MAX_VIDEO_BYTES = 50 * 1024 * 1024

MAX_TEXT_POST_LENGTH = 300
MAX_PHOTO_POST_BODY_LENGTH = 2200
MAX_COMMENT_LENGTH = 500
MAX_IMAGES_PER_POST = 4
MAX_HASHTAGS = 10
MAX_HASHTAG_LENGTH = 50

FEED_PAGE_SIZE = 20
FEED_PAGE_SIZE_MAX = 50
COMMENTS_PAGE_SIZE = 30

HASHTAG_SANITIZE_RE = re.compile(r"[^\w぀-ヿ一-鿿０-９Ａ-Ｚａ-ｚ-]")

os.makedirs(SNS_UPLOAD_FOLDER, exist_ok=True)


def _get_media_type(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext in ALLOWED_IMAGE_EXTENSIONS:
        return "image", ext
    if ext in ALLOWED_VIDEO_EXTENSIONS:
        return "video", ext
    return None, None


def _save_media_file(file_storage):
    if not file_storage or not file_storage.filename:
        raise ValueError("ファイルがありません")

    original_name = secure_filename(file_storage.filename)
    media_type, ext = _get_media_type(original_name)
    if not media_type:
        raise ValueError("対応していないファイル形式です（画像: jpg/png/gif/webp、動画: mp4/webm/mov）")

    file_storage.seek(0, os.SEEK_END)
    size = file_storage.tell()
    file_storage.seek(0)

    max_size = MAX_IMAGE_BYTES if media_type == "image" else MAX_VIDEO_BYTES
    if size > max_size:
        limit_mb = max_size // (1024 * 1024)
        raise ValueError(f"ファイルサイズは{limit_mb}MB以下にしてください")
    if size == 0:
        raise ValueError("ファイルが空です")

    stored_name = f"{uuid.uuid4().hex}.{ext}"
    save_path = SNS_UPLOAD_FOLDER / stored_name
    file_storage.save(str(save_path))

    return f"/uploads/sns/{stored_name}", media_type


def _sanitize_hashtags(raw_tags):
    if not raw_tags or not isinstance(raw_tags, list):
        return []
    cleaned = []
    for tag in raw_tags[:MAX_HASHTAGS]:
        if not isinstance(tag, str):
            continue
        tag = tag.strip().lstrip("#")
        tag = HASHTAG_SANITIZE_RE.sub("", tag)[:MAX_HASHTAG_LENGTH]
        if tag and tag not in cleaned:
            cleaned.append(tag)
    return cleaned


def _serialize_post(row, media_by_post, viewer_account_id):
    mapping = row._mapping if hasattr(row, "_mapping") else row
    post_id = mapping["post_id"]
    return {
        "post_id": post_id,
        "post_type": mapping["post_type"],
        "body": mapping["body"],
        "hashtags": list(mapping["hashtags"] or []),
        "comments_enabled": mapping["comments_enabled"],
        "visibility": mapping["visibility"],
        "created_at": mapping["created_at"].isoformat() if mapping["created_at"] else None,
        "updated_at": mapping["updated_at"].isoformat() if mapping["updated_at"] else None,
        "account_id": mapping["account_id"],
        "author_name": mapping["author_name"],
        "author_avatar_path": mapping["author_avatar_path"],
        "media": media_by_post.get(post_id, []),
        "like_count": int(mapping["like_count"] or 0),
        "comment_count": int(mapping["comment_count"] or 0),
        "liked_by_viewer": bool(mapping["liked_by_viewer"]) if viewer_account_id else False,
        "saved_by_viewer": bool(mapping["saved_by_viewer"]) if viewer_account_id else False,
        "is_owner": viewer_account_id == mapping["account_id"] if viewer_account_id else False,
    }


POST_SELECT_BASE = """
    SELECT
        p.post_id, p.post_type, p.body, p.hashtags, p.comments_enabled,
        p.visibility, p.created_at, p.updated_at, p.account_id,
        a.name AS author_name,
        pr.avatar_path AS author_avatar_path,
        (SELECT COUNT(*) FROM sns_likes l WHERE l.post_id = p.post_id) AS like_count,
        (SELECT COUNT(*) FROM sns_comments c
            WHERE c.post_id = p.post_id AND c.deleted_at IS NULL) AS comment_count,
        EXISTS(
            SELECT 1 FROM sns_likes l2
            WHERE l2.post_id = p.post_id AND l2.account_id = :viewer_id
        ) AS liked_by_viewer,
        EXISTS(
            SELECT 1 FROM sns_saved_posts s2
            WHERE s2.post_id = p.post_id AND s2.account_id = :viewer_id
        ) AS saved_by_viewer
    FROM sns_posts p
    JOIN accounts a ON a.account_id = p.account_id
    LEFT JOIN sns_profiles pr ON pr.account_id = p.account_id
"""

BLOCK_EXCLUSION_SQL = """
    NOT EXISTS (
        SELECT 1 FROM sns_blocks b
        WHERE (b.blocker_account_id = :viewer_id AND b.blocked_account_id = p.account_id)
           OR (b.blocker_account_id = p.account_id AND b.blocked_account_id = :viewer_id)
    )
"""


def _fetch_media_map(fetch_all, post_ids):
    if not post_ids:
        return {}
    rows = fetch_all(
        """
        SELECT post_id, media_type, file_path, sort_order
        FROM sns_post_media
        WHERE post_id = ANY(:post_ids)
        ORDER BY post_id, sort_order
        """,
        {"post_ids": list(post_ids)},
    )
    media_by_post = {}
    for row in rows:
        mapping = row._mapping if hasattr(row, "_mapping") else row
        media_by_post.setdefault(mapping["post_id"], []).append({
            "media_type": mapping["media_type"],
            "file_path": mapping["file_path"],
        })
    return media_by_post


def register_sns_post_routes(app, engine, **deps):
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

    @app.route("/uploads/sns/<path:filename>")
    def sns_serve_media(filename):
        safe_name = secure_filename(filename)
        return send_from_directory(str(SNS_UPLOAD_FOLDER), safe_name)

    @app.route("/api/sns/media/upload", methods=["POST"])
    def sns_upload_media():
        account_id, err = _require_login()
        if err:
            return err

        membership = get_membership_for_account(account_id)
        status = build_sns_usage_status(account_id, membership, engine)
        if not status["can_post"]:
            return jsonify({"error": "今週の投稿可能回数に達しました", **status}), 429

        file = request.files.get("file")
        try:
            path, media_type = _save_media_file(file)
            return jsonify({"path": path, "media_type": media_type})
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            print(e)
            return jsonify({"error": "アップロードに失敗しました"}), 500

    @app.route("/api/sns/posts", methods=["GET"])
    def sns_get_feed():
        try:
            viewer_id = _optional_account_id()
            post_type = request.args.get("type", "all")
            before_id = request.args.get("before_id", type=int)
            limit = min(request.args.get("limit", FEED_PAGE_SIZE, type=int) or FEED_PAGE_SIZE, FEED_PAGE_SIZE_MAX)

            where = ["p.is_deleted = FALSE"]
            params = {"viewer_id": viewer_id or 0, "limit": limit}

            if post_type in ("photo", "text"):
                where.append("p.post_type = :post_type")
                params["post_type"] = post_type

            if before_id:
                where.append("p.post_id < :before_id")
                params["before_id"] = before_id

            if viewer_id:
                where.append(BLOCK_EXCLUSION_SQL)

            sql = f"{POST_SELECT_BASE} WHERE {' AND '.join(where)} ORDER BY p.post_id DESC LIMIT :limit"
            rows = fetch_all(sql, params)

            post_ids = [row._mapping["post_id"] if hasattr(row, "_mapping") else row["post_id"] for row in rows]
            media_by_post = _fetch_media_map(fetch_all, post_ids)

            posts = [_serialize_post(row, media_by_post, viewer_id) for row in rows]
            next_cursor = posts[-1]["post_id"] if len(posts) == limit else None

            return jsonify({"posts": posts, "next_before_id": next_cursor})
        except Exception as e:
            print(e)
            return jsonify({"error": "フィードの取得に失敗しました"}), 500

    @app.route("/api/sns/posts/<int:post_id>", methods=["GET"])
    def sns_get_post(post_id):
        try:
            viewer_id = _optional_account_id()
            params = {"viewer_id": viewer_id or 0, "post_id": post_id}
            where = ["p.is_deleted = FALSE", "p.post_id = :post_id"]
            if viewer_id:
                where.append(BLOCK_EXCLUSION_SQL)
            sql = f"{POST_SELECT_BASE} WHERE {' AND '.join(where)}"
            rows = fetch_all(sql, params)
            if not rows:
                return jsonify({"error": "投稿が見つかりません"}), 404
            media_by_post = _fetch_media_map(fetch_all, [post_id])
            return jsonify(_serialize_post(rows[0], media_by_post, viewer_id))
        except Exception as e:
            print(e)
            return jsonify({"error": "投稿の取得に失敗しました"}), 500

    @app.route("/api/sns/posts", methods=["POST"])
    def sns_create_post():
        account_id, err = _require_login()
        if err:
            return err

        data = request.get_json(silent=True) or {}
        post_type = data.get("post_type")
        body = (data.get("body") or "").strip()
        media = data.get("media") or []
        comments_enabled = bool(data.get("comments_enabled", True))
        hashtags = _sanitize_hashtags(data.get("hashtags"))

        if post_type not in ("photo", "text"):
            return jsonify({"error": "投稿種別が不正です"}), 400

        if not isinstance(media, list):
            return jsonify({"error": "メディア情報が不正です"}), 400

        if post_type == "text":
            if not body and not media:
                return jsonify({"error": "本文または画像を入力してください"}), 400
            if len(body) > MAX_TEXT_POST_LENGTH:
                return jsonify({"error": f"本文は{MAX_TEXT_POST_LENGTH}文字以内で入力してください"}), 400
            if len(media) > 1 or any(m.get("media_type") != "image" for m in media):
                return jsonify({"error": "ひとこと投稿に添付できる画像は1枚までです"}), 400
        else:
            if not media:
                return jsonify({"error": "画像または動画を選択してください"}), 400
            if len(body) > MAX_PHOTO_POST_BODY_LENGTH:
                return jsonify({"error": f"本文は{MAX_PHOTO_POST_BODY_LENGTH}文字以内で入力してください"}), 400
            video_count = sum(1 for m in media if m.get("media_type") == "video")
            image_count = sum(1 for m in media if m.get("media_type") == "image")
            if video_count and (video_count > 1 or image_count):
                return jsonify({"error": "動画は1件のみ、画像との同時投稿はできません"}), 400
            if not video_count and image_count > MAX_IMAGES_PER_POST:
                return jsonify({"error": f"画像は{MAX_IMAGES_PER_POST}枚までです"}), 400
            for m in media:
                if not m.get("file_path") or m.get("media_type") not in ("image", "video"):
                    return jsonify({"error": "メディア情報が不正です"}), 400

        membership = get_membership_for_account(account_id)
        try:
            usage_status = consume_sns_post_usage(account_id, membership, engine)
        except SnsUsageLimitError as e:
            return jsonify({"error": e.message, **e.status}), 429

        try:
            post_id = execute_insert(
                """
                INSERT INTO sns_posts (account_id, post_type, body, hashtags, comments_enabled, visibility)
                VALUES (:account_id, :post_type, :body, :hashtags, :comments_enabled, 'public')
                RETURNING post_id
                """,
                {
                    "account_id": account_id,
                    "post_type": post_type,
                    "body": body,
                    "hashtags": hashtags,
                    "comments_enabled": comments_enabled,
                },
            )
            for index, m in enumerate(media):
                execute(
                    """
                    INSERT INTO sns_post_media (post_id, media_type, file_path, sort_order)
                    VALUES (:post_id, :media_type, :file_path, :sort_order)
                    """,
                    {
                        "post_id": post_id,
                        "media_type": m.get("media_type"),
                        "file_path": m.get("file_path"),
                        "sort_order": index,
                    },
                )

            return jsonify({
                "message": "投稿しました",
                "post_id": post_id,
                "usage": usage_status,
            }), 201
        except Exception as e:
            print(e)
            return jsonify({"error": "投稿の作成に失敗しました"}), 500

    @app.route("/api/sns/posts/<int:post_id>", methods=["PATCH"])
    def sns_update_post(post_id):
        account_id, err = _require_login()
        if err:
            return err

        rows = fetch_all(
            "SELECT account_id, post_type FROM sns_posts WHERE post_id = :post_id AND is_deleted = FALSE",
            {"post_id": post_id},
        )
        if not rows:
            return jsonify({"error": "投稿が見つかりません"}), 404
        owner_id = rows[0]._mapping["account_id"] if hasattr(rows[0], "_mapping") else rows[0]["account_id"]
        if owner_id != account_id:
            return jsonify({"error": "この投稿を編集する権限がありません"}), 403

        data = request.get_json(silent=True) or {}
        post_type = rows[0]._mapping["post_type"] if hasattr(rows[0], "_mapping") else rows[0]["post_type"]
        body = (data.get("body") or "").strip()
        max_len = MAX_TEXT_POST_LENGTH if post_type == "text" else MAX_PHOTO_POST_BODY_LENGTH
        if len(body) > max_len:
            return jsonify({"error": f"本文は{max_len}文字以内で入力してください"}), 400
        hashtags = _sanitize_hashtags(data.get("hashtags"))
        comments_enabled = bool(data.get("comments_enabled", True))

        try:
            execute(
                """
                UPDATE sns_posts
                SET body = :body, hashtags = :hashtags, comments_enabled = :comments_enabled, updated_at = NOW()
                WHERE post_id = :post_id AND account_id = :account_id
                """,
                {
                    "body": body, "hashtags": hashtags, "comments_enabled": comments_enabled,
                    "post_id": post_id, "account_id": account_id,
                },
            )
            return jsonify({"message": "更新しました"})
        except Exception as e:
            print(e)
            return jsonify({"error": "更新に失敗しました"}), 500

    @app.route("/api/sns/posts/<int:post_id>", methods=["DELETE"])
    def sns_delete_post(post_id):
        account_id, err = _require_login()
        if err:
            return err

        rows = fetch_all(
            "SELECT account_id FROM sns_posts WHERE post_id = :post_id AND is_deleted = FALSE",
            {"post_id": post_id},
        )
        if not rows:
            return jsonify({"error": "投稿が見つかりません"}), 404
        owner_id = rows[0]._mapping["account_id"] if hasattr(rows[0], "_mapping") else rows[0]["account_id"]
        if owner_id != account_id:
            return jsonify({"error": "この投稿を削除する権限がありません"}), 403

        try:
            execute(
                "UPDATE sns_posts SET is_deleted = TRUE, updated_at = NOW() WHERE post_id = :post_id",
                {"post_id": post_id},
            )
            return jsonify({"message": "削除しました"})
        except Exception as e:
            print(e)
            return jsonify({"error": "削除に失敗しました"}), 500

    @app.route("/api/sns/posts/<int:post_id>/like", methods=["POST"])
    def sns_toggle_like(post_id):
        account_id, err = _require_login()
        if err:
            return err

        try:
            rows = fetch_all(
                "SELECT like_id FROM sns_likes WHERE account_id = :account_id AND post_id = :post_id",
                {"account_id": account_id, "post_id": post_id},
            )
            if rows:
                like_id = rows[0]._mapping["like_id"] if hasattr(rows[0], "_mapping") else rows[0]["like_id"]
                execute("DELETE FROM sns_likes WHERE like_id = :like_id", {"like_id": like_id})
                liked = False
            else:
                execute(
                    "INSERT INTO sns_likes (account_id, post_id) VALUES (:account_id, :post_id) "
                    "ON CONFLICT (account_id, post_id) DO NOTHING",
                    {"account_id": account_id, "post_id": post_id},
                )
                liked = True

            count_row = fetch_all(
                "SELECT COUNT(*) AS c FROM sns_likes WHERE post_id = :post_id", {"post_id": post_id}
            )[0]
            like_count = count_row._mapping["c"] if hasattr(count_row, "_mapping") else count_row["c"]
            return jsonify({"liked": liked, "like_count": int(like_count)})
        except Exception as e:
            print(e)
            return jsonify({"error": "いいねの処理に失敗しました"}), 500

    @app.route("/api/sns/posts/<int:post_id>/save", methods=["POST"])
    def sns_toggle_save(post_id):
        account_id, err = _require_login()
        if err:
            return err

        try:
            rows = fetch_all(
                "SELECT saved_id FROM sns_saved_posts WHERE account_id = :account_id AND post_id = :post_id",
                {"account_id": account_id, "post_id": post_id},
            )
            if rows:
                saved_id = rows[0]._mapping["saved_id"] if hasattr(rows[0], "_mapping") else rows[0]["saved_id"]
                execute("DELETE FROM sns_saved_posts WHERE saved_id = :saved_id", {"saved_id": saved_id})
                saved = False
            else:
                execute(
                    "INSERT INTO sns_saved_posts (account_id, post_id) VALUES (:account_id, :post_id) "
                    "ON CONFLICT (account_id, post_id) DO NOTHING",
                    {"account_id": account_id, "post_id": post_id},
                )
                saved = True
            return jsonify({"saved": saved})
        except Exception as e:
            print(e)
            return jsonify({"error": "保存の処理に失敗しました"}), 500

    @app.route("/api/sns/posts/<int:post_id>/comments", methods=["GET"])
    def sns_get_comments(post_id):
        try:
            before_id = request.args.get("before_id", type=int)
            where = ["c.post_id = :post_id", "c.deleted_at IS NULL"]
            params = {"post_id": post_id, "limit": COMMENTS_PAGE_SIZE}
            if before_id:
                where.append("c.comment_id < :before_id")
                params["before_id"] = before_id

            rows = fetch_all(
                f"""
                SELECT c.comment_id, c.post_id, c.account_id, c.body, c.created_at,
                       a.name AS author_name, pr.avatar_path AS author_avatar_path
                FROM sns_comments c
                JOIN accounts a ON a.account_id = c.account_id
                LEFT JOIN sns_profiles pr ON pr.account_id = c.account_id
                WHERE {' AND '.join(where)}
                ORDER BY c.comment_id DESC
                LIMIT :limit
                """,
                params,
            )
            comments = []
            for row in rows:
                m = row._mapping if hasattr(row, "_mapping") else row
                comments.append({
                    "comment_id": m["comment_id"],
                    "post_id": m["post_id"],
                    "account_id": m["account_id"],
                    "body": m["body"],
                    "created_at": m["created_at"].isoformat() if m["created_at"] else None,
                    "author_name": m["author_name"],
                    "author_avatar_path": m["author_avatar_path"],
                })
            comments.reverse()
            next_cursor = comments[0]["comment_id"] if len(comments) == COMMENTS_PAGE_SIZE else None
            return jsonify({"comments": comments, "next_before_id": next_cursor})
        except Exception as e:
            print(e)
            return jsonify({"error": "コメントの取得に失敗しました"}), 500

    @app.route("/api/sns/posts/<int:post_id>/comments", methods=["POST"])
    def sns_create_comment(post_id):
        account_id, err = _require_login()
        if err:
            return err

        data = request.get_json(silent=True) or {}
        body = (data.get("body") or "").strip()
        if not body:
            return jsonify({"error": "コメントを入力してください"}), 400
        if len(body) > MAX_COMMENT_LENGTH:
            return jsonify({"error": f"コメントは{MAX_COMMENT_LENGTH}文字以内で入力してください"}), 400

        post_rows = fetch_all(
            "SELECT comments_enabled FROM sns_posts WHERE post_id = :post_id AND is_deleted = FALSE",
            {"post_id": post_id},
        )
        if not post_rows:
            return jsonify({"error": "投稿が見つかりません"}), 404
        enabled = post_rows[0]._mapping["comments_enabled"] if hasattr(post_rows[0], "_mapping") else post_rows[0]["comments_enabled"]
        if not enabled:
            return jsonify({"error": "この投稿はコメントが許可されていません"}), 403

        try:
            comment_id = execute_insert(
                """
                INSERT INTO sns_comments (post_id, account_id, body)
                VALUES (:post_id, :account_id, :body)
                RETURNING comment_id
                """,
                {"post_id": post_id, "account_id": account_id, "body": body},
            )
            return jsonify({"message": "コメントしました", "comment_id": comment_id}), 201
        except Exception as e:
            print(e)
            return jsonify({"error": "コメントの作成に失敗しました"}), 500

    @app.route("/api/sns/comments/<int:comment_id>", methods=["DELETE"])
    def sns_delete_comment(comment_id):
        account_id, err = _require_login()
        if err:
            return err

        rows = fetch_all(
            "SELECT account_id FROM sns_comments WHERE comment_id = :comment_id AND deleted_at IS NULL",
            {"comment_id": comment_id},
        )
        if not rows:
            return jsonify({"error": "コメントが見つかりません"}), 404
        owner_id = rows[0]._mapping["account_id"] if hasattr(rows[0], "_mapping") else rows[0]["account_id"]
        if owner_id != account_id:
            return jsonify({"error": "このコメントを削除する権限がありません"}), 403

        try:
            execute(
                "UPDATE sns_comments SET deleted_at = NOW() WHERE comment_id = :comment_id",
                {"comment_id": comment_id},
            )
            return jsonify({"message": "削除しました"})
        except Exception as e:
            print(e)
            return jsonify({"error": "削除に失敗しました"}), 500
