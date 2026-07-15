"""
ファンクラブ オープンチャット（会員同士のグループチャット）

LINE オープンチャット風: ルーム一覧 → 参加 → メッセージ送受信（ポーリング）
"""
from __future__ import annotations

import os
import uuid
from pathlib import Path

from flask import jsonify, request, send_from_directory
from sqlalchemy import text
from werkzeug.utils import secure_filename

MAX_MESSAGE_LENGTH = 2000
MESSAGES_PAGE_SIZE = 50
POLL_MAX_MESSAGES = 100

BASE_DIR = Path(__file__).resolve().parent
OPEN_CHAT_UPLOAD_FOLDER = BASE_DIR / "uploads" / "open-chat"
ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "webm", "mov"}
MAX_CHAT_IMAGE_BYTES = 10 * 1024 * 1024
MAX_CHAT_VIDEO_BYTES = 50 * 1024 * 1024

MESSAGE_TYPES = {"text", "image", "video"}

DEFAULT_ROOMS = [
    {
        "slug": "fanclub-main",
        "name": "美空ひばりファンクラブ・メイン",
        "description": "ファン同士が自由に語り合えるメインのオープンチャットです。",
        "icon_emoji": "✦",
        "scope": "artist_site",
        "artist_slug": "hibari",
    },
    {
        "slug": "fanclub-events",
        "name": "イベント・ライブ交流",
        "description": "コンサートやイベントの感想・同行募集などを共有しましょう。",
        "icon_emoji": "★",
        "scope": "artist_site",
        "artist_slug": "hibari",
    },
    {
        "slug": "fanclub-memories",
        "name": "思い出・エピソード",
        "description": "ひばりさんへの思い出や感動した曲のエピソードを交換する部屋です。",
        "icon_emoji": "♪",
        "scope": "artist_site",
        "artist_slug": "hibari",
    },
]

PLATFORM_DEFAULT_ROOMS = [
    {
        "slug": "mm-hibari-main",
        "name": "美空ひばりファン交流",
        "description": "美空ひばりを愛するファン同士が語り合えるメインルームです。",
        "icon_emoji": "✦",
        "scope": "platform",
        "artist_slug": "hibari",
    },
    {
        "slug": "mm-hibari-music",
        "name": "楽曲・作品トーク",
        "description": "名曲の感想、おすすめ曲、ディスコグラフィの話題など。",
        "icon_emoji": "♪",
        "scope": "platform",
        "artist_slug": "hibari",
    },
    {
        "slug": "mm-hibari-events",
        "name": "イベント・ライブ交流",
        "description": "コンサートや記念イベントの感想・情報共有。",
        "icon_emoji": "★",
        "scope": "platform",
        "artist_slug": "hibari",
    },
    {
        "slug": "mm-lounge",
        "name": "Music Memories 広場",
        "description": "アーティストを超えて、音楽の思い出を語り合うオープンな広場です。",
        "icon_emoji": "🎵",
        "scope": "platform",
        "artist_slug": None,
    },
]

ARTIST_LABELS = {
    "hibari": "美空ひばり",
}


def ensure_open_chat_schema(engine):
    OPEN_CHAT_UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS open_chat_rooms (
                    room_id SERIAL PRIMARY KEY,
                    slug VARCHAR(64) UNIQUE NOT NULL,
                    name VARCHAR(128) NOT NULL,
                    description TEXT,
                    icon_emoji VARCHAR(16) NOT NULL DEFAULT '💬',
                    max_members INTEGER NULL,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
        )
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS open_chat_members (
                    member_id SERIAL PRIMARY KEY,
                    room_id INTEGER NOT NULL REFERENCES open_chat_rooms(room_id) ON DELETE CASCADE,
                    account_id INTEGER NOT NULL,
                    display_name VARCHAR(64) NOT NULL,
                    joined_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    last_read_message_id INTEGER NULL,
                    UNIQUE (room_id, account_id)
                )
                """
            )
        )
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS open_chat_messages (
                    message_id SERIAL PRIMARY KEY,
                    room_id INTEGER NOT NULL REFERENCES open_chat_rooms(room_id) ON DELETE CASCADE,
                    account_id INTEGER NOT NULL,
                    body TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    deleted_at TIMESTAMPTZ NULL
                )
                """
            )
        )
        conn.execute(
            text(
                """
                CREATE INDEX IF NOT EXISTS idx_open_chat_messages_room_id
                ON open_chat_messages (room_id, message_id)
                """
            )
        )
        conn.execute(
            text(
                """
                CREATE INDEX IF NOT EXISTS idx_open_chat_members_room_id
                ON open_chat_members (room_id)
                """
            )
        )
        conn.execute(
            text(
                """
                ALTER TABLE open_chat_messages
                ADD COLUMN IF NOT EXISTS message_type VARCHAR(16) NOT NULL DEFAULT 'text'
                """
            )
        )
        conn.execute(
            text(
                """
                ALTER TABLE open_chat_messages
                ADD COLUMN IF NOT EXISTS media_path VARCHAR(500) NULL
                """
            )
        )

        conn.execute(
            text(
                """
                ALTER TABLE open_chat_rooms
                ADD COLUMN IF NOT EXISTS scope VARCHAR(32) NOT NULL DEFAULT 'artist_site'
                """
            )
        )
        conn.execute(
            text(
                """
                ALTER TABLE open_chat_rooms
                ADD COLUMN IF NOT EXISTS artist_slug VARCHAR(64) NULL
                """
            )
        )

    seed_default_rooms(engine)


def seed_default_rooms(engine):
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                UPDATE open_chat_rooms
                SET scope = 'artist_site', artist_slug = 'hibari'
                WHERE slug IN ('fanclub-main', 'fanclub-events', 'fanclub-memories')
                  AND (scope IS NULL OR scope = '' OR artist_slug IS NULL)
                """
            )
        )
        for room in DEFAULT_ROOMS + PLATFORM_DEFAULT_ROOMS:
            conn.execute(
                text(
                    """
                    INSERT INTO open_chat_rooms (slug, name, description, icon_emoji, scope, artist_slug)
                    VALUES (:slug, :name, :description, :icon_emoji, :scope, :artist_slug)
                    ON CONFLICT (slug) DO NOTHING
                    """
                ),
                room,
            )


def _row_mapping(row):
    return row._mapping if hasattr(row, "_mapping") else row


def is_fanclub_member(fetch_all, account_id):
    rows = fetch_all(
        """
        SELECT 1
        FROM fanclub_join_historys
        WHERE account_id = :account_id
        LIMIT 1
        """,
        {"account_id": account_id},
    )
    return bool(rows)


def get_account_display_name(fetch_account_row, account_id):
    account = fetch_account_row(account_id)
    if not account:
        return "会員"
    name = (account.get("name") or "").strip()
    return name or "会員"


def get_membership_label(get_membership_for_account, account_id):
    membership = get_membership_for_account(account_id)
    return membership or "general"


def get_chat_media_type(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext in ALLOWED_IMAGE_EXTENSIONS:
        return "image"
    if ext in ALLOWED_VIDEO_EXTENSIONS:
        return "video"
    return None


def save_open_chat_media_file(file_storage):
    if not file_storage or not file_storage.filename:
        return None, None

    original_name = secure_filename(file_storage.filename)
    media_type = get_chat_media_type(original_name)
    if not media_type:
        raise ValueError("対応していないファイル形式です（画像: jpg/png/gif/webp、動画: mp4/webm/mov）")

    file_storage.seek(0, os.SEEK_END)
    size = file_storage.tell()
    file_storage.seek(0)

    max_size = MAX_CHAT_IMAGE_BYTES if media_type == "image" else MAX_CHAT_VIDEO_BYTES
    if size > max_size:
        limit_mb = max_size // (1024 * 1024)
        raise ValueError(f"ファイルサイズは{limit_mb}MB以下にしてください")

    ext = original_name.rsplit(".", 1)[-1].lower()
    stored_name = f"{uuid.uuid4().hex}.{ext}"
    save_path = OPEN_CHAT_UPLOAD_FOLDER / stored_name
    file_storage.save(save_path)
    if not save_path.is_file():
        raise ValueError("ファイルの保存に失敗しました")

    return f"/uploads/open-chat/{stored_name}", media_type


def normalize_message_type(message_type, media_path=None):
    value = (message_type or "text").strip().lower()
    if value in MESSAGE_TYPES:
        return value
    if media_path:
        inferred = get_chat_media_type(media_path.rsplit("/", 1)[-1])
        if inferred:
            return inferred
    return "text"


def build_media_url(media_path):
    if not media_path:
        return None
    path = str(media_path).strip()
    if not path.startswith("/uploads/open-chat/"):
        return path
    filename = path.rsplit("/", 1)[-1]
    if not filename:
        return None
    return f"/api/open-chats/media/{filename}"


MESSAGE_SELECT = """
    msg.message_id,
    msg.room_id,
    msg.account_id,
    msg.body,
    msg.message_type,
    msg.media_path,
    msg.created_at,
    COALESCE(m.display_name, a.name, '会員') AS author_name,
    CASE
        WHEN EXISTS (
            SELECT 1 FROM fanclub_join_historys fj
            WHERE fj.account_id = msg.account_id AND fj.is_premium = TRUE
        ) THEN 'premium'
        ELSE 'general'
    END AS membership
"""


def serialize_message(row, account_id, to_jst_str):
    mapping = _row_mapping(row)
    author_id = int(mapping["account_id"])
    media_path = mapping.get("media_path")
    message_type = normalize_message_type(mapping.get("message_type"), media_path)
    body = mapping.get("body") or ""
    return {
        "message_id": int(mapping["message_id"]),
        "room_id": int(mapping["room_id"]),
        "account_id": author_id,
        "author_name": mapping["author_name"],
        "membership": mapping["membership"],
        "message_type": message_type,
        "body": body,
        "media_path": media_path,
        "media_url": build_media_url(media_path),
        "created_at": to_jst_str(mapping["created_at"]),
        "is_own": author_id == account_id,
    }


def register_open_chat_routes(
    app,
    engine,
    *,
    fetch_all,
    execute,
    execute_insert,
    row_to_dict,
    get_session_account_id,
    get_membership_for_account,
    fetch_account_row,
    to_jst_str,
):
    def require_fanclub_member(account_id):
        if not is_fanclub_member(fetch_all, account_id):
            return jsonify({"error": "ファンクラブ会員のみご利用いただけます"}), 403
        return None

    def get_room_or_404(room_id):
        rows = fetch_all(
            """
            SELECT room_id, slug, name, description, icon_emoji, scope, artist_slug, is_active, created_at
            FROM open_chat_rooms
            WHERE room_id = :room_id AND is_active = TRUE
            """,
            {"room_id": room_id},
        )
        if not rows:
            return None, (jsonify({"error": "チャットルームが見つかりません"}), 404)
        return row_to_dict(rows[0]), None

    def is_room_member(room_id, account_id):
        rows = fetch_all(
            """
            SELECT member_id
            FROM open_chat_members
            WHERE room_id = :room_id AND account_id = :account_id
            """,
            {"room_id": room_id, "account_id": account_id},
        )
        return bool(rows)

    def get_or_create_song_room(song_id):
        rows = fetch_all(
            "SELECT room_id FROM open_chat_rooms WHERE song_id = :song_id AND is_active = TRUE",
            {"song_id": song_id},
        )
        if rows:
            return _row_mapping(rows[0])["room_id"]

        song_rows = fetch_all(
            "SELECT title FROM songs WHERE song_id = :song_id",
            {"song_id": song_id},
        )
        if not song_rows:
            return None
        title = _row_mapping(song_rows[0])["title"]
        slug = f"song-{song_id}"

        room_id = execute_insert(
            """
            INSERT INTO open_chat_rooms (slug, name, description, icon_emoji, scope, song_id)
            VALUES (:slug, :name, :description, :icon_emoji, 'song', :song_id)
            ON CONFLICT (slug) DO NOTHING
            RETURNING room_id
            """,
            {
                "slug": slug,
                "name": f"「{title}」が好きな人の部屋",
                "description": f"「{title}」の思い出を語り合うオープンチャットです。",
                "icon_emoji": "🎵",
                "song_id": song_id,
            },
        )
        if room_id:
            return room_id

        # 同時アクセスでON CONFLICT DO NOTHINGに落ちた場合は再取得
        rows = fetch_all(
            "SELECT room_id FROM open_chat_rooms WHERE slug = :slug",
            {"slug": slug},
        )
        return _row_mapping(rows[0])["room_id"] if rows else None

    def serialize_room_row(mapping, account_id):
        artist_slug = mapping.get("artist_slug")
        return {
            "room_id": int(mapping["room_id"]),
            "slug": mapping["slug"],
            "name": mapping["name"],
            "description": mapping["description"],
            "icon_emoji": mapping["icon_emoji"],
            "scope": mapping.get("scope") or "artist_site",
            "artist_slug": artist_slug,
            "artist_name": ARTIST_LABELS.get(artist_slug) if artist_slug else "Music Memories 広場",
            "member_count": int(mapping.get("member_count") or 0),
            "last_message_preview": _preview_message(
                mapping.get("last_message_body"),
                mapping.get("last_message_type"),
            ),
            "last_message_at": to_jst_str(mapping.get("last_message_at")),
            "is_joined": bool(mapping["is_joined"]),
            "unread_count": int(mapping.get("unread_count") or 0),
            "created_at": to_jst_str(mapping["created_at"]),
        }

    def room_list_query_filters():
        scope = (request.args.get("scope") or "artist_site").strip()
        if scope not in {"artist_site", "platform"}:
            scope = "artist_site"
        artist = (request.args.get("artist") or "").strip() or None
        return scope, artist

    @app.route("/api/open-chats", methods=["GET"])
    def list_open_chats():
        try:
            try:
                account_id = get_session_account_id()
            except ValueError:
                return jsonify({"error": "ログインが必要です"}), 401

            denied = require_fanclub_member(account_id)
            if denied:
                return denied

            scope, artist = room_list_query_filters()
            params = {"account_id": account_id, "scope": scope}
            artist_filter = ""
            if artist:
                artist_filter = "AND r.artist_slug = :artist"
                params["artist"] = artist

            rows = fetch_all(
                f"""
                SELECT
                    r.room_id,
                    r.slug,
                    r.name,
                    r.description,
                    r.icon_emoji,
                    r.scope,
                    r.artist_slug,
                    r.created_at,
                    (
                        SELECT COUNT(*)::int
                        FROM open_chat_members m
                        WHERE m.room_id = r.room_id
                    ) AS member_count,
                    (
                        SELECT body
                        FROM open_chat_messages msg
                        WHERE msg.room_id = r.room_id AND msg.deleted_at IS NULL
                        ORDER BY msg.message_id DESC
                        LIMIT 1
                    ) AS last_message_body,
                    (
                        SELECT message_type
                        FROM open_chat_messages msg
                        WHERE msg.room_id = r.room_id AND msg.deleted_at IS NULL
                        ORDER BY msg.message_id DESC
                        LIMIT 1
                    ) AS last_message_type,
                    (
                        SELECT msg.created_at
                        FROM open_chat_messages msg
                        WHERE msg.room_id = r.room_id AND msg.deleted_at IS NULL
                        ORDER BY msg.message_id DESC
                        LIMIT 1
                    ) AS last_message_at,
                    EXISTS (
                        SELECT 1
                        FROM open_chat_members m2
                        WHERE m2.room_id = r.room_id AND m2.account_id = :account_id
                    ) AS is_joined,
                    (
                        SELECT COUNT(*)::int
                        FROM open_chat_messages msg
                        JOIN open_chat_members mem
                            ON mem.room_id = r.room_id AND mem.account_id = :account_id
                        WHERE msg.room_id = r.room_id
                          AND msg.deleted_at IS NULL
                          AND msg.account_id != :account_id
                          AND msg.message_id > COALESCE(mem.last_read_message_id, 0)
                    ) AS unread_count
                FROM open_chat_rooms r
                WHERE r.is_active = TRUE
                  AND r.scope = :scope
                  {artist_filter}
                ORDER BY r.artist_slug NULLS LAST, r.room_id ASC
                """,
                params,
            )

            rooms = [serialize_room_row(_row_mapping(row), account_id) for row in rows]

            return jsonify({"rooms": rooms, "scope": scope})
        except Exception as e:
            print(e)
            return jsonify({"error": "ルーム一覧の取得に失敗しました"}), 500

    @app.route("/api/open-chats/notifications", methods=["GET"])
    def open_chat_notifications():
        try:
            try:
                account_id = get_session_account_id()
            except ValueError:
                return jsonify({"error": "ログインが必要です"}), 401

            denied = require_fanclub_member(account_id)
            if denied:
                return denied

            scope, _artist = room_list_query_filters()

            rows = fetch_all(
                """
                SELECT
                    r.room_id,
                    r.name,
                    r.icon_emoji,
                    (
                        SELECT COUNT(*)::int
                        FROM open_chat_messages msg
                        WHERE msg.room_id = r.room_id
                          AND msg.deleted_at IS NULL
                          AND msg.account_id != :account_id
                          AND msg.message_id > COALESCE(mem.last_read_message_id, 0)
                    ) AS unread_count
                FROM open_chat_members mem
                JOIN open_chat_rooms r ON r.room_id = mem.room_id AND r.is_active = TRUE
                WHERE mem.account_id = :account_id
                  AND r.scope = :scope
                ORDER BY r.room_id ASC
                """,
                {"account_id": account_id, "scope": scope},
            )

            room_notifications = []
            total_unread = 0

            for row in rows:
                mapping = _row_mapping(row)
                unread = int(mapping["unread_count"] or 0)
                if unread <= 0:
                    continue

                room_id = int(mapping["room_id"])
                latest_rows = fetch_all(
                    f"""
                    SELECT {MESSAGE_SELECT}
                    FROM open_chat_messages msg
                    LEFT JOIN open_chat_members m
                        ON m.room_id = msg.room_id AND m.account_id = msg.account_id
                    LEFT JOIN accounts a ON a.account_id = msg.account_id
                    JOIN open_chat_members mem
                        ON mem.room_id = msg.room_id AND mem.account_id = :account_id
                    WHERE msg.room_id = :room_id
                      AND msg.deleted_at IS NULL
                      AND msg.account_id != :account_id
                      AND msg.message_id > COALESCE(mem.last_read_message_id, 0)
                    ORDER BY msg.message_id DESC
                    LIMIT 1
                    """,
                    {"room_id": room_id, "account_id": account_id},
                )

                latest = None
                if latest_rows:
                    latest_msg = serialize_message(latest_rows[0], account_id, to_jst_str)
                    latest = {
                        "message_id": latest_msg["message_id"],
                        "author_name": latest_msg["author_name"],
                        "preview": _preview_message(latest_msg.get("body"), latest_msg.get("message_type")),
                        "message_type": latest_msg.get("message_type"),
                        "created_at": latest_msg.get("created_at"),
                    }

                total_unread += unread
                room_notifications.append({
                    "room_id": room_id,
                    "room_name": mapping["name"],
                    "icon_emoji": mapping["icon_emoji"],
                    "unread_count": unread,
                    "latest_unread": latest,
                })

            return jsonify({
                "total_unread": total_unread,
                "rooms": room_notifications,
            })
        except Exception as e:
            print(e)
            return jsonify({"error": "通知の取得に失敗しました"}), 500

    def serve_open_chat_media_file(filename):
        try:
            account_id = get_session_account_id()
        except ValueError:
            return jsonify({"error": "ログインが必要です"}), 401

        denied = require_fanclub_member(account_id)
        if denied:
            return denied

        safe_name = secure_filename(filename)
        if not safe_name:
            return jsonify({"error": "ファイルが見つかりません"}), 404

        media_path = f"/uploads/open-chat/{safe_name}"
        rows = fetch_all(
            """
            SELECT 1
            FROM open_chat_messages msg
            JOIN open_chat_members mem
                ON mem.room_id = msg.room_id AND mem.account_id = :account_id
            WHERE msg.media_path = :media_path
              AND msg.deleted_at IS NULL
            LIMIT 1
            """,
            {"account_id": account_id, "media_path": media_path},
        )
        if not rows:
            return jsonify({"error": "このメディアを表示する権限がありません"}), 403

        file_path = OPEN_CHAT_UPLOAD_FOLDER / safe_name
        if not file_path.is_file():
            return jsonify({"error": "ファイルが見つかりません"}), 404

        response = send_from_directory(str(OPEN_CHAT_UPLOAD_FOLDER), safe_name)
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        return response

    @app.route("/api/open-chats/media/<path:filename>")
    def serve_open_chat_media(filename):
        return serve_open_chat_media_file(filename)

    @app.route("/uploads/open-chat/<path:filename>")
    def serve_open_chat_upload(filename):
        return serve_open_chat_media_file(filename)

    @app.route("/api/open-chats/<int:room_id>/upload", methods=["POST"])
    def upload_open_chat_media(room_id):
        try:
            try:
                account_id = get_session_account_id()
            except ValueError:
                return jsonify({"error": "ログインが必要です"}), 401

            denied = require_fanclub_member(account_id)
            if denied:
                return denied

            room, err = get_room_or_404(room_id)
            if err:
                return err

            if not is_room_member(room_id, account_id):
                return jsonify({"error": "ルームに参加してからアップロードしてください"}), 403

            file = request.files.get("file")
            if not file:
                return jsonify({"error": "ファイルがありません"}), 400

            public_path, media_type = save_open_chat_media_file(file)
            return jsonify({
                "path": public_path,
                "media_type": media_type,
            })
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            print(e)
            return jsonify({"error": "アップロードに失敗しました"}), 500

    @app.route("/api/open-chats/<int:room_id>", methods=["GET"])
    def get_open_chat_room(room_id):
        try:
            try:
                account_id = get_session_account_id()
            except ValueError:
                return jsonify({"error": "ログインが必要です"}), 401

            denied = require_fanclub_member(account_id)
            if denied:
                return denied

            room, err = get_room_or_404(room_id)
            if err:
                return err

            stats = fetch_all(
                """
                SELECT
                    (
                        SELECT COUNT(*)::int
                        FROM open_chat_members m
                        WHERE m.room_id = :room_id
                    ) AS member_count,
                    EXISTS (
                        SELECT 1
                        FROM open_chat_members m2
                        WHERE m2.room_id = :room_id AND m2.account_id = :account_id
                    ) AS is_joined
                """,
                {"room_id": room_id, "account_id": account_id},
            )
            stat = _row_mapping(stats[0]) if stats else {}

            return jsonify({
                **room,
                "member_count": int(stat.get("member_count") or 0),
                "is_joined": bool(stat.get("is_joined")),
            })
        except Exception as e:
            print(e)
            return jsonify({"error": "ルーム情報の取得に失敗しました"}), 500

    @app.route("/api/open-chats/by-song/<int:song_id>", methods=["GET"])
    def get_song_chat_room(song_id):
        try:
            try:
                get_session_account_id()
            except ValueError:
                return jsonify({"error": "ログインが必要です"}), 401

            room_id = get_or_create_song_room(song_id)
            if not room_id:
                return jsonify({"error": "曲が見つかりません"}), 404

            return jsonify({"room_id": room_id})
        except Exception as e:
            print(e)
            return jsonify({"error": "チャットルームの取得に失敗しました"}), 500

    @app.route("/api/open-chats/<int:room_id>/join", methods=["POST"])
    def join_open_chat(room_id):
        try:
            try:
                account_id = get_session_account_id()
            except ValueError:
                return jsonify({"error": "ログインが必要です"}), 401

            denied = require_fanclub_member(account_id)
            if denied:
                return denied

            room, err = get_room_or_404(room_id)
            if err:
                return err

            if is_room_member(room_id, account_id):
                return jsonify({"success": True, "already_joined": True, "room_id": room_id})

            display_name = get_account_display_name(fetch_account_row, account_id)
            execute(
                """
                INSERT INTO open_chat_members (room_id, account_id, display_name)
                VALUES (:room_id, :account_id, :display_name)
                ON CONFLICT (room_id, account_id) DO NOTHING
                """,
                {
                    "room_id": room_id,
                    "account_id": account_id,
                    "display_name": display_name[:64],
                },
            )

            return jsonify({"success": True, "room_id": room_id, "display_name": display_name}), 201
        except Exception as e:
            print(e)
            return jsonify({"error": "ルームへの参加に失敗しました"}), 500

    @app.route("/api/open-chats/<int:room_id>/leave", methods=["POST"])
    def leave_open_chat(room_id):
        try:
            try:
                account_id = get_session_account_id()
            except ValueError:
                return jsonify({"error": "ログインが必要です"}), 401

            execute(
                """
                DELETE FROM open_chat_members
                WHERE room_id = :room_id AND account_id = :account_id
                """,
                {"room_id": room_id, "account_id": account_id},
            )
            return jsonify({"success": True})
        except Exception as e:
            print(e)
            return jsonify({"error": "ルームからの退出に失敗しました"}), 500

    @app.route("/api/open-chats/<int:room_id>/members", methods=["GET"])
    def list_open_chat_members(room_id):
        try:
            try:
                account_id = get_session_account_id()
            except ValueError:
                return jsonify({"error": "ログインが必要です"}), 401

            denied = require_fanclub_member(account_id)
            if denied:
                return denied

            if not is_room_member(room_id, account_id):
                return jsonify({"error": "ルームに参加してからメンバー一覧をご覧ください"}), 403

            rows = fetch_all(
                """
                SELECT
                    m.account_id,
                    m.display_name,
                    m.joined_at
                FROM open_chat_members m
                WHERE m.room_id = :room_id
                ORDER BY m.joined_at ASC
                LIMIT 200
                """,
                {"room_id": room_id},
            )

            members = []
            for row in rows:
                mapping = _row_mapping(row)
                member_id = int(mapping["account_id"])
                members.append({
                    "account_id": member_id,
                    "display_name": mapping["display_name"],
                    "membership": get_membership_label(get_membership_for_account, member_id),
                    "joined_at": to_jst_str(mapping["joined_at"]),
                    "is_own": member_id == account_id,
                })

            return jsonify({"members": members})
        except Exception as e:
            print(e)
            return jsonify({"error": "メンバー一覧の取得に失敗しました"}), 500

    @app.route("/api/open-chats/<int:room_id>/messages", methods=["GET"])
    def list_open_chat_messages(room_id):
        try:
            try:
                account_id = get_session_account_id()
            except ValueError:
                return jsonify({"error": "ログインが必要です"}), 401

            denied = require_fanclub_member(account_id)
            if denied:
                return denied

            if not is_room_member(room_id, account_id):
                return jsonify({"error": "ルームに参加してからメッセージをご覧ください"}), 403

            after_id = request.args.get("after_id", type=int)
            limit = min(request.args.get("limit", MESSAGES_PAGE_SIZE, type=int), MESSAGES_PAGE_SIZE)

            if after_id:
                rows = fetch_all(
                    f"""
                    SELECT {MESSAGE_SELECT}
                    FROM open_chat_messages msg
                    LEFT JOIN open_chat_members m
                        ON m.room_id = msg.room_id AND m.account_id = msg.account_id
                    LEFT JOIN accounts a ON a.account_id = msg.account_id
                    WHERE msg.room_id = :room_id
                      AND msg.deleted_at IS NULL
                      AND msg.message_id > :after_id
                    ORDER BY msg.message_id ASC
                    LIMIT :limit
                    """,
                    {
                        "room_id": room_id,
                        "after_id": after_id,
                        "limit": min(limit, POLL_MAX_MESSAGES),
                    },
                )
            else:
                rows = fetch_all(
                    f"""
                    SELECT *
                    FROM (
                        SELECT {MESSAGE_SELECT}
                        FROM open_chat_messages msg
                        LEFT JOIN open_chat_members m
                            ON m.room_id = msg.room_id AND m.account_id = msg.account_id
                        LEFT JOIN accounts a ON a.account_id = msg.account_id
                        WHERE msg.room_id = :room_id AND msg.deleted_at IS NULL
                        ORDER BY msg.message_id DESC
                        LIMIT :limit
                    ) recent
                    ORDER BY message_id ASC
                    """,
                    {"room_id": room_id, "limit": limit},
                )

            messages = [serialize_message(row, account_id, to_jst_str) for row in rows]
            latest_id = messages[-1]["message_id"] if messages else after_id

            if messages:
                execute(
                    """
                    UPDATE open_chat_members
                    SET last_read_message_id = :message_id
                    WHERE room_id = :room_id AND account_id = :account_id
                    """,
                    {
                        "message_id": latest_id,
                        "room_id": room_id,
                        "account_id": account_id,
                    },
                )

            return jsonify({
                "messages": messages,
                "latest_id": latest_id,
            })
        except Exception as e:
            print(e)
            return jsonify({"error": "メッセージの取得に失敗しました"}), 500

    @app.route("/api/open-chats/<int:room_id>/messages", methods=["POST"])
    def post_open_chat_message(room_id):
        try:
            try:
                account_id = get_session_account_id()
            except ValueError:
                return jsonify({"error": "ログインが必要です"}), 401

            denied = require_fanclub_member(account_id)
            if denied:
                return denied

            data = request.get_json() or {}
            body = (data.get("body") or "").strip()
            message_type = (data.get("message_type") or "text").strip().lower()
            media_path = (data.get("media_path") or "").strip() or None

            if message_type not in MESSAGE_TYPES:
                return jsonify({"error": "不正なメッセージ種別です"}), 400

            if message_type == "text":
                if not body:
                    return jsonify({"error": "メッセージを入力してください"}), 400
                if len(body) > MAX_MESSAGE_LENGTH:
                    return jsonify({"error": f"メッセージは{MAX_MESSAGE_LENGTH}文字以内にしてください"}), 400
                media_path = None
            else:
                if not media_path:
                    return jsonify({"error": "メディアファイルが指定されていません"}), 400
                if not media_path.startswith("/uploads/open-chat/"):
                    return jsonify({"error": "不正なメディアパスです"}), 400
                if message_type == "image" and body and len(body) > MAX_MESSAGE_LENGTH:
                    return jsonify({"error": f"キャプションは{MAX_MESSAGE_LENGTH}文字以内にしてください"}), 400

            room, err = get_room_or_404(room_id)
            if err:
                return err

            if not is_room_member(room_id, account_id):
                display_name = get_account_display_name(fetch_account_row, account_id)
                execute(
                    """
                    INSERT INTO open_chat_members (room_id, account_id, display_name)
                    VALUES (:room_id, :account_id, :display_name)
                    ON CONFLICT (room_id, account_id) DO NOTHING
                    """,
                    {
                        "room_id": room_id,
                        "account_id": account_id,
                        "display_name": display_name[:64],
                    },
                )

            message_id = execute_insert(
                """
                INSERT INTO open_chat_messages (room_id, account_id, body, message_type, media_path)
                VALUES (:room_id, :account_id, :body, :message_type, :media_path)
                RETURNING message_id
                """,
                {
                    "room_id": room_id,
                    "account_id": account_id,
                    "body": body,
                    "message_type": message_type,
                    "media_path": media_path,
                },
            )

            rows = fetch_all(
                f"""
                SELECT {MESSAGE_SELECT}
                FROM open_chat_messages msg
                LEFT JOIN open_chat_members m
                    ON m.room_id = msg.room_id AND m.account_id = msg.account_id
                LEFT JOIN accounts a ON a.account_id = msg.account_id
                WHERE msg.message_id = :message_id
                """,
                {"message_id": message_id},
            )

            message = serialize_message(rows[0], account_id, to_jst_str)
            return jsonify({"success": True, "message": message}), 201
        except Exception as e:
            print(e)
            return jsonify({"error": "メッセージの送信に失敗しました"}), 500


def _preview_message(body, message_type=None):
    message_type = message_type or "text"
    if message_type == "image":
        caption = _preview_text(body)
        return f"📷 画像{(': ' + caption) if caption else ''}"
    if message_type == "video":
        caption = _preview_text(body)
        return f"🎬 動画{(': ' + caption) if caption else ''}"
    return _preview_text(body)


def _preview_text(body):
    if not body:
        return ""
    text_value = str(body).replace("\n", " ").strip()
    if len(text_value) > 60:
        return text_value[:60] + "…"
    return text_value
