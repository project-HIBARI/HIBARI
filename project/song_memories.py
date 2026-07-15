"""
同じ曲で泣いた人マッチング（楽曲ごとの思い出登録）

sns_profile.py と同じ依存注入パターンで app.py からルートを登録する。
"""
from __future__ import annotations

from flask import jsonify, request
from sqlalchemy import text

from open_chat import is_fanclub_member

MEMORY_TYPES = {"tears", "nostalgic", "loved_one", "energized", "special_moment"}
VISIBILITY_VALUES = {"public", "members", "private"}
MAX_COMMENT_LENGTH = 20


def ensure_song_memories_schema(engine):
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS song_memories (
                    memory_id SERIAL PRIMARY KEY,
                    song_id BIGINT NOT NULL REFERENCES songs(song_id) ON DELETE CASCADE,
                    account_id INTEGER NOT NULL REFERENCES accounts(account_id) ON DELETE CASCADE,
                    memory_type VARCHAR(32) NOT NULL,
                    comment VARCHAR(20),
                    visibility VARCHAR(16) NOT NULL DEFAULT 'public',
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    UNIQUE (song_id, account_id)
                )
                """
            )
        )
        conn.execute(
            text(
                """
                ALTER TABLE open_chat_rooms
                ADD COLUMN IF NOT EXISTS song_id BIGINT REFERENCES songs(song_id) ON DELETE CASCADE
                """
            )
        )
        conn.execute(
            text(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS idx_open_chat_rooms_song_id
                ON open_chat_rooms (song_id) WHERE song_id IS NOT NULL
                """
            )
        )


def _row_val(row, key):
    mapping = row._mapping if hasattr(row, "_mapping") else row
    return mapping[key]


def register_song_memory_routes(app, engine, **deps):
    fetch_all = deps["fetch_all"]
    execute = deps["execute"]
    get_session_account_id = deps["get_session_account_id"]
    to_jst_str = deps["to_jst_str"]

    def _require_login():
        try:
            return get_session_account_id(), None
        except ValueError:
            return None, (jsonify({"error": "ログインが必要です"}), 401)

    def _optional_account_id():
        try:
            return get_session_account_id()
        except ValueError:
            return None

    @app.route("/api/songs/<int:song_id>/memories", methods=["POST"])
    def create_song_memory(song_id):
        account_id, err = _require_login()
        if err:
            return err

        data = request.get_json(silent=True) or {}
        memory_type = data.get("memory_type")
        comment = (data.get("comment") or "").strip()
        visibility = data.get("visibility", "public")

        if memory_type not in MEMORY_TYPES:
            return jsonify({"error": "思い出の種類を選択してください"}), 400
        if visibility not in VISIBILITY_VALUES:
            return jsonify({"error": "公開範囲の指定が不正です"}), 400
        if len(comment) > MAX_COMMENT_LENGTH:
            return jsonify({"error": f"コメントは{MAX_COMMENT_LENGTH}文字以内で入力してください"}), 400

        try:
            execute(
                """
                INSERT INTO song_memories (song_id, account_id, memory_type, comment, visibility)
                VALUES (:song_id, :account_id, :memory_type, :comment, :visibility)
                ON CONFLICT (song_id, account_id) DO UPDATE SET
                    memory_type = EXCLUDED.memory_type,
                    comment = EXCLUDED.comment,
                    visibility = EXCLUDED.visibility
                """,
                {
                    "song_id": song_id,
                    "account_id": account_id,
                    "memory_type": memory_type,
                    "comment": comment or None,
                    "visibility": visibility,
                },
            )
            return jsonify({"message": "登録しました"}), 201
        except Exception as e:
            print(e)
            return jsonify({"error": "思い出の登録に失敗しました"}), 500

    @app.route("/api/songs/<int:song_id>/memories/summary", methods=["GET"])
    def get_song_memory_summary(song_id):
        try:
            rows = fetch_all(
                "SELECT COUNT(*) AS c FROM song_memories WHERE song_id = :song_id",
                {"song_id": song_id},
            )
            count = int(_row_val(rows[0], "c")) if rows else 0
            return jsonify({"count": count})
        except Exception as e:
            print(e)
            return jsonify({"error": "件数の取得に失敗しました"}), 500

    @app.route("/api/songs/<int:song_id>/memories", methods=["GET"])
    def get_song_memories(song_id):
        try:
            viewer_id = _optional_account_id()
            visibility_clause = "sm.visibility = 'public'"
            if viewer_id and is_fanclub_member(fetch_all, viewer_id):
                visibility_clause = "sm.visibility IN ('public', 'members')"

            rows = fetch_all(
                f"""
                SELECT sm.account_id, sm.memory_type, sm.comment, sm.created_at,
                       a.name, a.address, pr.avatar_path,
                       EXISTS(
                           SELECT 1 FROM sns_follows f
                           WHERE f.follower_account_id = :viewer_id AND f.following_account_id = sm.account_id
                       ) AS is_following
                FROM song_memories sm
                JOIN accounts a ON a.account_id = sm.account_id
                LEFT JOIN sns_profiles pr ON pr.account_id = sm.account_id
                WHERE sm.song_id = :song_id
                  AND {visibility_clause}
                ORDER BY sm.created_at DESC
                """,
                {"song_id": song_id, "viewer_id": viewer_id or 0},
            )
            memories = [{
                "account_id": _row_val(r, "account_id"),
                "name": _row_val(r, "name"),
                "avatar_path": _row_val(r, "avatar_path"),
                "address": _row_val(r, "address"),
                "memory_type": _row_val(r, "memory_type"),
                "comment": _row_val(r, "comment"),
                "created_at": to_jst_str(_row_val(r, "created_at")),
                "is_following": bool(_row_val(r, "is_following")) if viewer_id else False,
            } for r in rows]
            return jsonify({"memories": memories})
        except Exception as e:
            print(e)
            return jsonify({"error": "一覧の取得に失敗しました"}), 500

    @app.route("/api/accounts/<int:account_id>/song-memories", methods=["GET"])
    def get_account_song_memories(account_id):
        try:
            viewer_id = _optional_account_id()
            if viewer_id == account_id:
                visibility_clause = "TRUE"
            elif viewer_id and is_fanclub_member(fetch_all, viewer_id):
                visibility_clause = "sm.visibility IN ('public', 'members')"
            else:
                visibility_clause = "sm.visibility = 'public'"

            rows = fetch_all(
                f"""
                SELECT sm.memory_id, sm.song_id, sm.memory_type, sm.comment,
                       sm.visibility, sm.created_at, s.title, s.release_year
                FROM song_memories sm
                JOIN songs s ON s.song_id = sm.song_id
                WHERE sm.account_id = :account_id
                  AND {visibility_clause}
                ORDER BY sm.created_at DESC
                """,
                {"account_id": account_id},
            )
            memories = [{
                "memory_id": _row_val(r, "memory_id"),
                "song_id": _row_val(r, "song_id"),
                "title": _row_val(r, "title"),
                "release_year": _row_val(r, "release_year"),
                "memory_type": _row_val(r, "memory_type"),
                "comment": _row_val(r, "comment"),
                "visibility": _row_val(r, "visibility"),
                "created_at": to_jst_str(_row_val(r, "created_at")),
            } for r in rows]
            return jsonify({"memories": memories})
        except Exception as e:
            print(e)
            return jsonify({"error": "一覧の取得に失敗しました"}), 500
