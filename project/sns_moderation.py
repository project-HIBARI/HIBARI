"""
Music Memories SNS フェーズ7: 通報 / ブロック

管理画面（通報一覧の閲覧・対応）は今回のスコープ外（DB保存のみ）。
sns.py と同じ依存注入パターンで app.py からルートを登録する。
"""
from __future__ import annotations

from flask import jsonify, request

MAX_REASON_LENGTH = 500
TARGET_TYPES = {"post", "comment", "user", "dm_message"}


def _row_val(row, key):
    mapping = row._mapping if hasattr(row, "_mapping") else row
    return mapping[key]


def register_sns_moderation_routes(app, engine, **deps):
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

    @app.route("/api/sns/reports", methods=["POST"])
    def sns_create_report():
        account_id, err = _require_login()
        if err:
            return err

        data = request.get_json(silent=True) or {}
        target_type = data.get("target_type")
        target_id = data.get("target_id")
        reason = (data.get("reason") or "").strip()

        if target_type not in TARGET_TYPES:
            return jsonify({"error": "通報対象の種別が不正です"}), 400
        if not isinstance(target_id, int):
            return jsonify({"error": "通報対象を指定してください"}), 400
        if not reason:
            return jsonify({"error": "通報理由を入力してください"}), 400
        if len(reason) > MAX_REASON_LENGTH:
            return jsonify({"error": f"通報理由は{MAX_REASON_LENGTH}文字以内で入力してください"}), 400

        try:
            report_id = execute_insert(
                """
                INSERT INTO sns_reports (reporter_account_id, target_type, target_id, reason)
                VALUES (:reporter_account_id, :target_type, :target_id, :reason)
                RETURNING report_id
                """,
                {
                    "reporter_account_id": account_id,
                    "target_type": target_type,
                    "target_id": target_id,
                    "reason": reason,
                },
            )
            return jsonify({"message": "通報を受け付けました", "report_id": report_id}), 201
        except Exception as e:
            print(e)
            return jsonify({"error": "通報の送信に失敗しました"}), 500

    @app.route("/api/sns/block/<int:target_id>", methods=["POST"])
    def sns_toggle_block(target_id):
        account_id, err = _require_login()
        if err:
            return err

        if account_id == target_id:
            return jsonify({"error": "自分自身をブロックすることはできません"}), 400

        target = fetch_account_row(target_id)
        if not target:
            return jsonify({"error": "ユーザーが見つかりません"}), 404

        try:
            rows = fetch_all(
                "SELECT block_id FROM sns_blocks WHERE blocker_account_id = :a AND blocked_account_id = :b",
                {"a": account_id, "b": target_id},
            )
            if rows:
                execute(
                    "DELETE FROM sns_blocks WHERE block_id = :id",
                    {"id": _row_val(rows[0], "block_id")},
                )
                blocked = False
            else:
                execute(
                    """
                    INSERT INTO sns_blocks (blocker_account_id, blocked_account_id)
                    VALUES (:a, :b)
                    ON CONFLICT (blocker_account_id, blocked_account_id) DO NOTHING
                    """,
                    {"a": account_id, "b": target_id},
                )
                blocked = True
                # ブロックすると同時にフォロー関係も解除する
                execute(
                    """
                    DELETE FROM sns_follows
                    WHERE (follower_account_id = :a AND following_account_id = :b)
                       OR (follower_account_id = :b AND following_account_id = :a)
                    """,
                    {"a": account_id, "b": target_id},
                )
            return jsonify({"blocked": blocked})
        except Exception as e:
            print(e)
            return jsonify({"error": "ブロック処理に失敗しました"}), 500

    @app.route("/api/sns/blocks", methods=["GET"])
    def sns_list_blocks():
        account_id, err = _require_login()
        if err:
            return err

        rows = fetch_all(
            """
            SELECT b.blocked_account_id AS account_id, a.name,
                   pr.avatar_path
            FROM sns_blocks b
            JOIN accounts a ON a.account_id = b.blocked_account_id
            LEFT JOIN sns_profiles pr ON pr.account_id = b.blocked_account_id
            WHERE b.blocker_account_id = :account_id
            ORDER BY b.created_at DESC
            """,
            {"account_id": account_id},
        )
        users = [{
            "account_id": _row_val(r, "account_id"),
            "name": _row_val(r, "name"),
            "avatar_path": _row_val(r, "avatar_path"),
        } for r in rows]
        return jsonify({"users": users})
