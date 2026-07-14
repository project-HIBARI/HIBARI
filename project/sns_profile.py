"""
Music Memories SNS フェーズ4: プロフィール / フォロー / 保存済み投稿

sns.py と同じ依存注入パターンで app.py からルートを登録する。
"""
from __future__ import annotations

import os
import uuid

from flask import jsonify, request
from werkzeug.utils import secure_filename

from sns_posts import (
    ALLOWED_IMAGE_EXTENSIONS,
    MAX_IMAGE_BYTES,
    SNS_UPLOAD_FOLDER,
    POST_SELECT_BASE,
    _fetch_media_map,
    _serialize_post,
)

SAVED_POST_SELECT = f"""
    SELECT sp.saved_id, {POST_SELECT_BASE.strip()[len('SELECT'):]}
    JOIN sns_saved_posts sp ON sp.post_id = p.post_id
"""

MAX_BIO_LENGTH = 500
FEED_PAGE_SIZE = 20
FEED_PAGE_SIZE_MAX = 50
FOLLOW_PAGE_SIZE = 30


def _row_val(row, key):
    mapping = row._mapping if hasattr(row, "_mapping") else row
    return mapping[key]


def register_sns_profile_routes(app, engine, **deps):
    fetch_all = deps["fetch_all"]
    execute = deps["execute"]
    get_session_account_id = deps["get_session_account_id"]
    get_membership_for_account = deps["get_membership_for_account"]
    fetch_account_row = deps["fetch_account_row"]

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

    def _is_blocked(viewer_id, target_id):
        if not viewer_id:
            return False
        rows = fetch_all(
            """
            SELECT 1 FROM sns_blocks
            WHERE (blocker_account_id = :a AND blocked_account_id = :b)
               OR (blocker_account_id = :b AND blocked_account_id = :a)
            """,
            {"a": viewer_id, "b": target_id},
        )
        return bool(rows)

    @app.route("/api/sns/profile/avatar/upload", methods=["POST"])
    def sns_upload_avatar():
        account_id, err = _require_login()
        if err:
            return err

        file = request.files.get("file")
        if not file or not file.filename:
            return jsonify({"error": "ファイルがありません"}), 400

        original_name = secure_filename(file.filename)
        ext = original_name.rsplit(".", 1)[-1].lower() if "." in original_name else ""
        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            return jsonify({"error": "画像形式（jpg/png/gif/webp）のみアップロードできます"}), 400

        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        if size > MAX_IMAGE_BYTES or size == 0:
            return jsonify({"error": "ファイルサイズは10MB以下にしてください"}), 400

        stored_name = f"{uuid.uuid4().hex}.{ext}"
        save_path = SNS_UPLOAD_FOLDER / stored_name
        file.save(str(save_path))
        avatar_path = f"/uploads/sns/{stored_name}"

        try:
            execute(
                """
                INSERT INTO sns_profiles (account_id, avatar_path, updated_at)
                VALUES (:account_id, :avatar_path, NOW())
                ON CONFLICT (account_id) DO UPDATE SET
                    avatar_path = EXCLUDED.avatar_path, updated_at = NOW()
                """,
                {"account_id": account_id, "avatar_path": avatar_path},
            )
            return jsonify({"avatar_path": avatar_path})
        except Exception as e:
            print(e)
            return jsonify({"error": "プロフィール画像の更新に失敗しました"}), 500

    @app.route("/api/sns/profile/me", methods=["PATCH"])
    def sns_update_my_profile():
        account_id, err = _require_login()
        if err:
            return err

        data = request.get_json(silent=True) or {}
        bio = (data.get("bio") or "").strip()
        if len(bio) > MAX_BIO_LENGTH:
            return jsonify({"error": f"自己紹介は{MAX_BIO_LENGTH}文字以内で入力してください"}), 400

        try:
            execute(
                """
                INSERT INTO sns_profiles (account_id, bio, updated_at)
                VALUES (:account_id, :bio, NOW())
                ON CONFLICT (account_id) DO UPDATE SET
                    bio = EXCLUDED.bio, updated_at = NOW()
                """,
                {"account_id": account_id, "bio": bio},
            )
            return jsonify({"message": "更新しました", "bio": bio})
        except Exception as e:
            print(e)
            return jsonify({"error": "プロフィールの更新に失敗しました"}), 500

    @app.route("/api/sns/profile/<int:target_id>", methods=["GET"])
    def sns_get_profile(target_id):
        try:
            viewer_id = _optional_account_id()
            account = fetch_account_row(target_id)
            if not account:
                return jsonify({"error": "ユーザーが見つかりません"}), 404

            if _is_blocked(viewer_id, target_id) and viewer_id != target_id:
                return jsonify({"error": "このプロフィールは表示できません"}), 403

            profile_rows = fetch_all(
                "SELECT bio, avatar_path FROM sns_profiles WHERE account_id = :account_id",
                {"account_id": target_id},
            )
            bio = _row_val(profile_rows[0], "bio") if profile_rows else ""
            avatar_path = _row_val(profile_rows[0], "avatar_path") if profile_rows else None

            post_count = _row_val(fetch_all(
                "SELECT COUNT(*) AS c FROM sns_posts WHERE account_id = :id AND is_deleted = FALSE",
                {"id": target_id},
            )[0], "c")
            follower_count = _row_val(fetch_all(
                "SELECT COUNT(*) AS c FROM sns_follows WHERE following_account_id = :id",
                {"id": target_id},
            )[0], "c")
            following_count = _row_val(fetch_all(
                "SELECT COUNT(*) AS c FROM sns_follows WHERE follower_account_id = :id",
                {"id": target_id},
            )[0], "c")

            is_following = False
            if viewer_id and viewer_id != target_id:
                rows = fetch_all(
                    "SELECT 1 FROM sns_follows WHERE follower_account_id = :v AND following_account_id = :t",
                    {"v": viewer_id, "t": target_id},
                )
                is_following = bool(rows)

            return jsonify({
                "account_id": target_id,
                "name": account.get("name"),
                "bio": bio,
                "avatar_path": avatar_path,
                "post_count": int(post_count),
                "follower_count": int(follower_count),
                "following_count": int(following_count),
                "is_self": viewer_id == target_id,
                "is_following": is_following,
                "membership": get_membership_for_account(target_id),
            })
        except Exception as e:
            print(e)
            return jsonify({"error": "プロフィールの取得に失敗しました"}), 500

    @app.route("/api/sns/profile/<int:target_id>/posts", methods=["GET"])
    def sns_get_profile_posts(target_id):
        try:
            viewer_id = _optional_account_id()
            if _is_blocked(viewer_id, target_id) and viewer_id != target_id:
                return jsonify({"error": "この投稿は表示できません"}), 403

            post_type = request.args.get("type", "all")
            before_id = request.args.get("before_id", type=int)
            limit = min(request.args.get("limit", FEED_PAGE_SIZE, type=int) or FEED_PAGE_SIZE, FEED_PAGE_SIZE_MAX)

            where = ["p.is_deleted = FALSE", "p.account_id = :target_id"]
            params = {"viewer_id": viewer_id or 0, "target_id": target_id, "limit": limit}
            if post_type in ("photo", "text"):
                where.append("p.post_type = :post_type")
                params["post_type"] = post_type
            if before_id:
                where.append("p.post_id < :before_id")
                params["before_id"] = before_id

            sql = f"{POST_SELECT_BASE} WHERE {' AND '.join(where)} ORDER BY p.post_id DESC LIMIT :limit"
            rows = fetch_all(sql, params)
            post_ids = [_row_val(row, "post_id") for row in rows]
            media_by_post = _fetch_media_map(fetch_all, post_ids)
            posts = [_serialize_post(row, media_by_post, viewer_id) for row in rows]
            next_cursor = posts[-1]["post_id"] if len(posts) == limit else None
            return jsonify({"posts": posts, "next_before_id": next_cursor})
        except Exception as e:
            print(e)
            return jsonify({"error": "投稿の取得に失敗しました"}), 500

    @app.route("/api/sns/saved", methods=["GET"])
    def sns_get_saved_posts():
        account_id, err = _require_login()
        if err:
            return err

        try:
            before_id = request.args.get("before_id", type=int)
            limit = min(request.args.get("limit", FEED_PAGE_SIZE, type=int) or FEED_PAGE_SIZE, FEED_PAGE_SIZE_MAX)

            where = ["p.is_deleted = FALSE", "sp.account_id = :account_id"]
            params = {"viewer_id": account_id, "account_id": account_id, "limit": limit}
            if before_id:
                where.append("sp.saved_id < :before_id")
                params["before_id"] = before_id

            sql = f"{SAVED_POST_SELECT} WHERE {' AND '.join(where)} ORDER BY sp.saved_id DESC LIMIT :limit"
            rows = fetch_all(sql, params)
            post_ids = [_row_val(row, "post_id") for row in rows]
            media_by_post = _fetch_media_map(fetch_all, post_ids)
            posts = [_serialize_post(row, media_by_post, account_id) for row in rows]
            next_cursor = _row_val(rows[-1], "saved_id") if len(posts) == limit else None
            return jsonify({"posts": posts, "next_before_id": next_cursor})
        except Exception as e:
            print(e)
            return jsonify({"error": "保存済み投稿の取得に失敗しました"}), 500

    @app.route("/api/sns/follow/<int:target_id>", methods=["POST"])
    def sns_toggle_follow(target_id):
        account_id, err = _require_login()
        if err:
            return err

        if account_id == target_id:
            return jsonify({"error": "自分自身をフォローすることはできません"}), 400

        target = fetch_account_row(target_id)
        if not target:
            return jsonify({"error": "ユーザーが見つかりません"}), 404

        if _is_blocked(account_id, target_id):
            return jsonify({"error": "ブロック中のユーザーはフォローできません"}), 403

        try:
            rows = fetch_all(
                "SELECT follow_id FROM sns_follows WHERE follower_account_id = :f AND following_account_id = :t",
                {"f": account_id, "t": target_id},
            )
            if rows:
                execute(
                    "DELETE FROM sns_follows WHERE follow_id = :id",
                    {"id": _row_val(rows[0], "follow_id")},
                )
                following = False
            else:
                execute(
                    """
                    INSERT INTO sns_follows (follower_account_id, following_account_id)
                    VALUES (:f, :t)
                    ON CONFLICT (follower_account_id, following_account_id) DO NOTHING
                    """,
                    {"f": account_id, "t": target_id},
                )
                following = True

            follower_count = _row_val(fetch_all(
                "SELECT COUNT(*) AS c FROM sns_follows WHERE following_account_id = :id",
                {"id": target_id},
            )[0], "c")
            return jsonify({"following": following, "follower_count": int(follower_count)})
        except Exception as e:
            print(e)
            return jsonify({"error": "フォロー処理に失敗しました"}), 500

    @app.route("/api/sns/follow/<int:target_id>/following", methods=["GET"])
    def sns_get_following(target_id):
        try:
            viewer_id = _optional_account_id()
            before_id = request.args.get("before_id", type=int)
            params = {"target_id": target_id, "limit": FOLLOW_PAGE_SIZE}
            where = ["f.follower_account_id = :target_id"]
            if before_id:
                where.append("f.follow_id < :before_id")
                params["before_id"] = before_id

            rows = fetch_all(
                f"""
                SELECT f.follow_id, f.following_account_id AS account_id, a.name,
                       pr.avatar_path,
                       EXISTS(
                           SELECT 1 FROM sns_follows f2
                           WHERE f2.follower_account_id = :viewer_id
                             AND f2.following_account_id = f.following_account_id
                       ) AS is_following
                FROM sns_follows f
                JOIN accounts a ON a.account_id = f.following_account_id
                LEFT JOIN sns_profiles pr ON pr.account_id = f.following_account_id
                WHERE {' AND '.join(where)}
                ORDER BY f.follow_id DESC
                LIMIT :limit
                """,
                {**params, "viewer_id": viewer_id or 0},
            )
            users = [{
                "account_id": _row_val(r, "account_id"),
                "name": _row_val(r, "name"),
                "avatar_path": _row_val(r, "avatar_path"),
                "is_following": bool(_row_val(r, "is_following")) if viewer_id else False,
            } for r in rows]
            next_cursor = _row_val(rows[-1], "follow_id") if len(rows) == FOLLOW_PAGE_SIZE else None
            return jsonify({"users": users, "next_before_id": next_cursor})
        except Exception as e:
            print(e)
            return jsonify({"error": "フォロー中一覧の取得に失敗しました"}), 500

    @app.route("/api/sns/follow/<int:target_id>/followers", methods=["GET"])
    def sns_get_followers(target_id):
        try:
            viewer_id = _optional_account_id()
            before_id = request.args.get("before_id", type=int)
            params = {"target_id": target_id, "limit": FOLLOW_PAGE_SIZE}
            where = ["f.following_account_id = :target_id"]
            if before_id:
                where.append("f.follow_id < :before_id")
                params["before_id"] = before_id

            rows = fetch_all(
                f"""
                SELECT f.follow_id, f.follower_account_id AS account_id, a.name,
                       pr.avatar_path,
                       EXISTS(
                           SELECT 1 FROM sns_follows f2
                           WHERE f2.follower_account_id = :viewer_id
                             AND f2.following_account_id = f.follower_account_id
                       ) AS is_following
                FROM sns_follows f
                JOIN accounts a ON a.account_id = f.follower_account_id
                LEFT JOIN sns_profiles pr ON pr.account_id = f.follower_account_id
                WHERE {' AND '.join(where)}
                ORDER BY f.follow_id DESC
                LIMIT :limit
                """,
                {**params, "viewer_id": viewer_id or 0},
            )
            users = [{
                "account_id": _row_val(r, "account_id"),
                "name": _row_val(r, "name"),
                "avatar_path": _row_val(r, "avatar_path"),
                "is_following": bool(_row_val(r, "is_following")) if viewer_id else False,
            } for r in rows]
            next_cursor = _row_val(rows[-1], "follow_id") if len(rows) == FOLLOW_PAGE_SIZE else None
            return jsonify({"users": users, "next_before_id": next_cursor})
        except Exception as e:
            print(e)
            return jsonify({"error": "フォロワー一覧の取得に失敗しました"}), 500
