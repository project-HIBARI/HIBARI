"""
Music Memories SNS: 検索・発見

sns.py と同じ依存注入パターン（register_sns_search_routes(app, engine, **deps)）で
app.py からルートを登録する。

検索対象:
- ユーザー（accounts.name / 数値の場合は account_id も一致対象）
- 投稿本文（sns_posts.body）
- ハッシュタグ（sns_posts.hashtags）

現状の DB にはアーティスト名・楽曲名・アルバム名を独立して保持するテーブルが存在しないため、
それらの検索は対応していない（実装結果の報告を参照）。
"""
from __future__ import annotations

from flask import jsonify, request

from sns_posts import (
    BLOCK_EXCLUSION_SQL,
    POST_SELECT_BASE,
    _fetch_media_map,
    _serialize_post,
)

SEARCH_MAX_QUERY_LENGTH = 100
USER_SEARCH_PAGE_SIZE = 20
POST_SEARCH_PAGE_SIZE = 20
HASHTAG_SEARCH_PAGE_SIZE = 20
TOP_SECTION_LIMIT = 5
DISCOVER_PAGE_SIZE = 21
PAGE_SIZE_MAX = 50


def _row_val(row, key):
    mapping = row._mapping if hasattr(row, "_mapping") else row
    return mapping[key]


def _clean_query(raw):
    q = (raw or "").strip()
    return q[:SEARCH_MAX_QUERY_LENGTH]


def register_sns_search_routes(app, engine, **deps):
    fetch_all = deps["fetch_all"]
    get_session_account_id = deps["get_session_account_id"]

    def _optional_account_id():
        try:
            return get_session_account_id()
        except ValueError:
            return None

    def _search_users(q, viewer_id, limit, offset):
        conditions = ["a.name ILIKE :q"]
        params = {
            "q": f"%{q}%",
            "q_exact": q,
            "viewer_id": viewer_id or 0,
            "limit": limit,
            "offset": offset,
        }
        if q.isdigit():
            conditions.append("a.account_id = :q_id")
            params["q_id"] = int(q)

        block_clause = ""
        if viewer_id:
            block_clause = """
                AND NOT EXISTS (
                    SELECT 1 FROM sns_blocks b
                    WHERE (b.blocker_account_id = :viewer_id AND b.blocked_account_id = a.account_id)
                       OR (b.blocker_account_id = a.account_id AND b.blocked_account_id = :viewer_id)
                )
            """

        rows = fetch_all(
            f"""
            SELECT a.account_id, a.name, pr.bio, pr.avatar_path,
                   EXISTS(
                       SELECT 1 FROM sns_follows f
                       WHERE f.follower_account_id = :viewer_id AND f.following_account_id = a.account_id
                   ) AS is_following
            FROM accounts a
            LEFT JOIN sns_profiles pr ON pr.account_id = a.account_id
            WHERE ({" OR ".join(conditions)})
            {block_clause}
            ORDER BY (a.name = :q_exact) DESC, a.name ASC
            LIMIT :limit OFFSET :offset
            """,
            params,
        )
        return [{
            "account_id": _row_val(r, "account_id"),
            "name": _row_val(r, "name"),
            "bio": _row_val(r, "bio") or "",
            "avatar_path": _row_val(r, "avatar_path"),
            "is_following": bool(_row_val(r, "is_following")) if viewer_id else False,
        } for r in rows]

    def _search_posts(q, viewer_id, limit, offset):
        where = [
            "p.is_deleted = FALSE",
            "(p.body ILIKE :q OR EXISTS (SELECT 1 FROM unnest(p.hashtags) tag WHERE tag ILIKE :q))",
        ]
        params = {"q": f"%{q}%", "viewer_id": viewer_id or 0, "limit": limit, "offset": offset}
        if viewer_id:
            where.append(BLOCK_EXCLUSION_SQL)

        sql = f"{POST_SELECT_BASE} WHERE {' AND '.join(where)} ORDER BY p.post_id DESC LIMIT :limit OFFSET :offset"
        rows = fetch_all(sql, params)
        post_ids = [_row_val(r, "post_id") for r in rows]
        media_by_post = _fetch_media_map(fetch_all, post_ids)
        return [_serialize_post(r, media_by_post, viewer_id) for r in rows]

    def _search_hashtags(q, limit, offset):
        rows = fetch_all(
            """
            SELECT tag, COUNT(*) AS post_count
            FROM (
                SELECT unnest(hashtags) AS tag
                FROM sns_posts
                WHERE is_deleted = FALSE
            ) tags
            WHERE tag ILIKE :q
            GROUP BY tag
            ORDER BY post_count DESC, tag ASC
            LIMIT :limit OFFSET :offset
            """,
            {"q": f"%{q}%", "limit": limit, "offset": offset},
        )
        return [{
            "tag": _row_val(r, "tag"),
            "post_count": int(_row_val(r, "post_count")),
        } for r in rows]

    @app.route("/api/sns/search/top", methods=["GET"])
    def sns_search_top():
        try:
            viewer_id = _optional_account_id()
            q = _clean_query(request.args.get("q"))
            if not q:
                return jsonify({"users": [], "posts": [], "hashtags": []})

            users = _search_users(q, viewer_id, TOP_SECTION_LIMIT, 0)
            posts = _search_posts(q, viewer_id, TOP_SECTION_LIMIT, 0)
            hashtags = _search_hashtags(q, TOP_SECTION_LIMIT, 0)
            return jsonify({"users": users, "posts": posts, "hashtags": hashtags})
        except Exception as e:
            print(e)
            return jsonify({"error": "検索に失敗しました"}), 500

    @app.route("/api/sns/search/users", methods=["GET"])
    def sns_search_users():
        try:
            viewer_id = _optional_account_id()
            q = _clean_query(request.args.get("q"))
            if not q:
                return jsonify({"users": [], "next_offset": None})

            offset = max(request.args.get("offset", 0, type=int) or 0, 0)
            limit = min(
                request.args.get("limit", USER_SEARCH_PAGE_SIZE, type=int) or USER_SEARCH_PAGE_SIZE,
                PAGE_SIZE_MAX,
            )
            users = _search_users(q, viewer_id, limit, offset)
            next_offset = offset + limit if len(users) == limit else None
            return jsonify({"users": users, "next_offset": next_offset})
        except Exception as e:
            print(e)
            return jsonify({"error": "ユーザー検索に失敗しました"}), 500

    @app.route("/api/sns/search/posts", methods=["GET"])
    def sns_search_posts():
        try:
            viewer_id = _optional_account_id()
            q = _clean_query(request.args.get("q"))
            if not q:
                return jsonify({"posts": [], "next_offset": None})

            offset = max(request.args.get("offset", 0, type=int) or 0, 0)
            limit = min(
                request.args.get("limit", POST_SEARCH_PAGE_SIZE, type=int) or POST_SEARCH_PAGE_SIZE,
                PAGE_SIZE_MAX,
            )
            posts = _search_posts(q, viewer_id, limit, offset)
            next_offset = offset + limit if len(posts) == limit else None
            return jsonify({"posts": posts, "next_offset": next_offset})
        except Exception as e:
            print(e)
            return jsonify({"error": "投稿検索に失敗しました"}), 500

    @app.route("/api/sns/search/hashtags", methods=["GET"])
    def sns_search_hashtags():
        try:
            q = _clean_query(request.args.get("q"))
            if not q:
                return jsonify({"hashtags": [], "next_offset": None})

            offset = max(request.args.get("offset", 0, type=int) or 0, 0)
            limit = min(
                request.args.get("limit", HASHTAG_SEARCH_PAGE_SIZE, type=int) or HASHTAG_SEARCH_PAGE_SIZE,
                PAGE_SIZE_MAX,
            )
            hashtags = _search_hashtags(q, limit, offset)
            next_offset = offset + limit if len(hashtags) == limit else None
            return jsonify({"hashtags": hashtags, "next_offset": next_offset})
        except Exception as e:
            print(e)
            return jsonify({"error": "ハッシュタグ検索に失敗しました"}), 500

    @app.route("/api/sns/discover/posts", methods=["GET"])
    def sns_discover_posts():
        try:
            viewer_id = _optional_account_id()
            offset = max(request.args.get("offset", 0, type=int) or 0, 0)
            limit = min(
                request.args.get("limit", DISCOVER_PAGE_SIZE, type=int) or DISCOVER_PAGE_SIZE,
                PAGE_SIZE_MAX,
            )

            where = [
                "p.is_deleted = FALSE",
                "EXISTS (SELECT 1 FROM sns_post_media m WHERE m.post_id = p.post_id)",
            ]
            params = {"viewer_id": viewer_id or 0, "limit": limit, "offset": offset}
            if viewer_id:
                where.append(BLOCK_EXCLUSION_SQL)

            # 単純な新着/人気ブレンド: いいね・コメントを加点し、経過時間で緩やかに減衰、
            # 未フォローの投稿者をわずかに優遇する（複雑なレコメンドは行わない）。
            sql = f"""
                {POST_SELECT_BASE}
                WHERE {' AND '.join(where)}
                ORDER BY (
                    (SELECT COUNT(*) FROM sns_likes l WHERE l.post_id = p.post_id) * 1.0
                    + (SELECT COUNT(*) FROM sns_comments c WHERE c.post_id = p.post_id AND c.deleted_at IS NULL) * 1.5
                    - EXTRACT(EPOCH FROM (NOW() - p.created_at)) / 21600.0
                    + CASE WHEN NOT EXISTS (
                        SELECT 1 FROM sns_follows f
                        WHERE f.follower_account_id = :viewer_id AND f.following_account_id = p.account_id
                      ) THEN 1.5 ELSE 0 END
                ) DESC, p.post_id DESC
                LIMIT :limit OFFSET :offset
            """
            rows = fetch_all(sql, params)
            post_ids = [_row_val(r, "post_id") for r in rows]
            media_by_post = _fetch_media_map(fetch_all, post_ids)
            posts = [_serialize_post(r, media_by_post, viewer_id) for r in rows]
            next_offset = offset + limit if len(posts) == limit else None
            return jsonify({"posts": posts, "next_offset": next_offset})
        except Exception as e:
            print(e)
            return jsonify({"error": "発見コンテンツの取得に失敗しました"}), 500
