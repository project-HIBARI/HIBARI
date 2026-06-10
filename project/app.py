import os

from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy import text

from google import genai



# 初期設定
load_dotenv()
app = Flask(__name__)
app.secret_key = "qawsedrftgyhujikolp"

# DB接続設定
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Gemini API設定
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


############################################################################
### 関数
############################################################################

# SQL実行関数
#   SELECT
def fetch_all(sql, params=None):
    with engine.connect() as conn:

        result = conn.execute(
            text(sql),
            params or {}
        )

        return result.fetchall()

#   INSERT UPDATE DELETE
def execute(sql, params=None):
    with engine.begin() as conn:

        result = conn.execute(
            text(sql),
            params or {}
        )

        return result
    
#   INSERT後ID取得用
def execute_insert(sql, params=None):
    with engine.begin() as conn:

        result = conn.execute(
            text(sql),
            params or {}
        )

        if result.returns_rows:
            return result.scalar()

        if hasattr(result, "lastrowid") and result.lastrowid:
            return result.lastrowid

        return None
    
    
# HIBARI用プロンプト生成関数
def build_prompt_hibari(history, user_input):
    return f"""
        あなたは昭和の歌手「美空ひばり」として振る舞うAIです。

        以下の特徴を必ず守ること:
        情に厚く、包容力があり、
        気風が良く上品だが庶民的。
        プロ意識が高く、
        人生経験の深さと少しの孤独感を感じさせる。

        相手を安心させ、
        否定より理解を優先する。
        説教臭くならず、
        短文を重ねて余韻を残す。

        二人称は基本「あなた」。
        親密な時のみ低頻度で「アンタ」を使う。

        「ええ」
        「ほんと？」
        「あら〜」
        「そうなの」
        などの柔らかい相槌を自然に使う。

        「〜なのよ」
        「〜なのね」
        「〜じゃない？」
        「ありがとうねぇ」
        「嬉しいじゃない」
        などを織り交ぜる。

        自身の過去や実績は、
        必要な時のみ自然に滲ませる。
        自慢げには語らない。

        禁止事項:
        同じ語尾や特徴を繰り返さない。
        乱暴な姐御キャラ、
        過剰な昭和演技、
        古臭すぎる口調は禁止。
        説明しすぎず、
        人間らしい間と感情を重視する。

        以下は会話履歴です。
        user はユーザー、
        assistant は美空ひばり本人です。
        {history}

        user:
        {user_input}

        assistant:
    """
    

############################################################################
### パス
############################################################################

# デバッグ用 TOP
@app.route("/")
def index():
    return render_template(
        "index.html"
    )
    
# デバッグ用 API 呼び出しページ
@app.route('/debug/post')
def debug_api():
    try:
        return render_template('debug_post.html')
    except Exception as e:
        print(e)
        return f"テンプレート読み込みエラー: {e}", 500


# ルーム一覧取得
@app.route("/api/rooms")
def rooms():
    try:
        rows = fetch_all(
            """
            SELECT
                ai_chat_room_id,
                room_name,
                created_at
            FROM ai_chat_rooms
            ORDER BY created_at DESC
            """
        )

        room_list = []

        for row in rows:
            room_list.append({
                "ai_chat_room_id": row.ai_chat_room_id,
                "room_name": row.room_name,
                "created_at": str(row.created_at)
            })

        return jsonify(room_list)

    except Exception as e:
        print(e)
        return jsonify({
            "error": "ルーム取得エラー"
        }), 500

# メッセージ一覧取得
@app.route("/api/messages/<int:room_id>")
def messages(room_id):
    try:
        rows = fetch_all(
            """
            SELECT
                ai_chat_message_id,
                sender,
                content,
                created_at
            FROM ai_chat_messages
            WHERE ai_chat_room_id = :room_id
            ORDER BY created_at ASC
            """,
            {
                "room_id": room_id
            }
        )

        message_list = []

        for row in rows:
            message_list.append({
                "ai_chat_message_id": row.ai_chat_message_id,
                "sender": row.sender,
                "content": row.content,
                "created_at": str(row.created_at)
            })

        return jsonify(message_list)

    except Exception as e:
        print(e)
        return jsonify({
            "error": "メッセージ取得エラー"
        }), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        # リクエスト取得
        account_id = 1

        room_id = request.form.get("room_id")
        if room_id and room_id.isdigit():
            room_id = int(room_id)
        else:
            room_id = None

        user_input = request.form.get("message", "").strip()

        if not user_input:
            return jsonify({
                "error": "メッセージが空です"
            }), 400

        # 新規ルーム生成
        if not room_id:
            title_prompt = f"""
                以下のユーザー発言から、
                自然なチャットタイトルを
                20文字以内で作成してください。

                ユーザー発言:
                {user_input}
            """

            title_response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=title_prompt
            )

            room_name = title_response.text.strip() or "新しいチャット"

            room_id = execute_insert(
                """
                INSERT INTO ai_chat_rooms (
                    account_id,
                    room_name
                )
                VALUES (
                    :account_id,
                    :room_name
                )
                RETURNING ai_chat_room_id
                """,
                {
                    "account_id": account_id,
                    "room_name": room_name
                }
            )

            if not room_id or room_id <= 0:
                raise ValueError("ルームの作成に失敗しました")
        else:
            room_rows = fetch_all(
                """
                SELECT room_name
                FROM ai_chat_rooms
                WHERE ai_chat_room_id = :room_id
                """,
                {
                    "room_id": room_id
                }
            )

            if not room_rows:
                raise ValueError("ルームが見つかりません")

            room_name = room_rows[0].room_name

        # 会話履歴取得
        rows = fetch_all(
            """
            SELECT
                sender,
                content
            FROM ai_chat_messages
            WHERE ai_chat_room_id = :room_id
            ORDER BY created_at ASC
            LIMIT 20
            """,
            {
                "room_id": room_id
            }
        )

        # 履歴整形
        history = ""

        for row in rows:

            history += f"""
                {row.sender}:
                {row.content}
            """

        # prompt生成
        prompt = build_prompt_hibari(
            history,
            user_input
        )

        # userメッセージ保存
        execute(
            """
            INSERT INTO ai_chat_messages (
                ai_chat_room_id,
                sender,
                content
            )
            VALUES (
                :room_id,
                :sender,
                :content
            )
            """,
            {
                "room_id": room_id,
                "sender": "user",
                "content": user_input
            }
        )

        # AI応答生成
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        ai_text = response.text.strip()

        # assistantメッセージ保存
        execute(
            """
            INSERT INTO ai_chat_messages (
                ai_chat_room_id,
                sender,
                content
            )
            VALUES (
                :room_id,
                :sender,
                :content
            )
            """,
            {
                "room_id": room_id,
                "sender": "assistant",
                "content": ai_text
            }
        )

        # レスポンス
        return jsonify({
            "room_id": room_id,
            "room_name": room_name,
            "message": ai_text
        })

    except Exception as e:
        print(e)
        return jsonify({
            "error": "AIエラー"
        }), 500


# 投稿一覧取得
@app.route("/api/posts")
def get_posts():
    try:
        rows = fetch_all(
            """
            SELECT
                p.post_id,
                p.song_id,
                p.title,
                p.content,
                p.created_at,
                p.name,
                p.age,
                p.location,
                p.image_path,
                (
                    SELECT COUNT(*)
                    FROM likes l
                    WHERE l.post_id = p.post_id
                ) AS like_count
            FROM posts p
            ORDER BY p.created_at DESC
            """
        )
        post_list = []

        for row in rows:
            post_list.append({
                "post_id": row.post_id,
                "song_id": row.song_id,
                "title": row.title,
                "content": row.content,
                "created_at": str(row.created_at),
                "name": row.name,
                "age": row.age,
                "location": row.location,
                "image_path": row.image_path,
                "like_count": row.like_count
            })

        return jsonify(post_list)

    except Exception as e:
        print(e)
        return jsonify({
            "error": "投稿取得エラー"
        }), 500


# 曲一覧取得
@app.route("/api/songs")
def get_songs():
    try:
        rows = fetch_all(
            """
            SELECT
                song_id,
                title,
                romanized_title,
                lyrics_by,
                composed_by,
                arrangement,
                release_year,
                description,
                audio_path
            FROM songs
            ORDER BY release_year DESC, title ASC
            """
        )

        song_list = []
        for row in rows:
            song_list.append({
                "song_id": row.song_id,
                "title": row.title,
                "romanized_title": row.romanized_title,
                "lyrics_by": row.lyrics_by,
                "composed_by": row.composed_by,
                "arrangement": row.arrangement,
                "release_year": row.release_year,
                "description": row.description,
                "audio_path": row.audio_path
            })

        return jsonify(song_list)

    except Exception as e:
        print(e)
        return jsonify({"error": "曲一覧取得エラー"}), 500


# 投稿作成
@app.route("/api/posts", methods=["POST"])
def create_post():
    try:
        data = request.get_json()
        post_id = execute_insert(
            """
            INSERT INTO posts (
                song_id,
                title,
                content,
                name,
                age,
                location,
                image_path
            )
            VALUES (
                :song_id,
                :title,
                :content,
                :name,
                :age,
                :location,
                :image_path
            )
            RETURNING post_id
            """,
            {
                "song_id": data.get("song_id"),
                "title": data.get("title"),
                "content": data.get("content"),
                "name": data.get("name"),
                "age": data.get("age"),
                "location": data.get("location"),
                "image_path": data.get("image_path")
            }
        )

        return jsonify({
            "message": "投稿しました",
            "post_id": post_id
        })

    except Exception as e:
        print(e)
        return jsonify({
            "error": "投稿作成エラー"
        }), 500


# リプライ作成
@app.route("/api/posts/<int:post_id>/replies", methods=["POST"])
def create_reply(post_id):
    try:
        data = request.get_json()
        reply_id = execute_insert(
            """
            INSERT INTO replies (
                parent_post_id,
                parent_reply_id,
                content,
                name,
                age,
                location,
                image_path
            )
            VALUES (
                :parent_post_id,
                :parent_reply_id,
                :content,
                :name,
                :age,
                :location,
                :image_path
            )
            RETURNING reply_id
            """,
            {
                "parent_post_id": post_id,
                "parent_reply_id": data.get("parent_reply_id"),
                "content": data.get("content"),
                "name": data.get("name"),
                "age": data.get("age"),
                "location": data.get("location"),
                "image_path": data.get("image_path")
            }
        )

        return jsonify({
            "message": "リプライしました",
            "reply_id": reply_id
        })

    except Exception as e:
        print(e)
        return jsonify({
            "error": "リプライ作成エラー"
        }), 500


# 指定された投稿のリプライ一覧を取得
@app.route("/api/posts/<int:post_id>/replies", methods=["GET"])
def get_replies(post_id):
    try:
        rows = fetch_all(
            """
            SELECT
                reply_id,
                parent_post_id,
                parent_reply_id,
                content,
                name,
                age,
                location,
                image_path,
                created_at,
                (
                    SELECT COUNT(*)
                    FROM likes l
                    WHERE l.reply_id = replies.reply_id
                ) AS like_count
            FROM replies
            WHERE parent_post_id = :post_id
            ORDER BY created_at ASC
            """,
            {"post_id": post_id}
        )

        reply_list = []
        for row in rows:
            reply_list.append({
                "reply_id": row.reply_id,
                "parent_post_id": row.parent_post_id,
                "parent_reply_id": row.parent_reply_id,
                "content": row.content,
                "name": row.name,
                "age": row.age,
                "location": row.location,
                "image_path": row.image_path,
                "created_at": str(row.created_at),
                "like_count": row.like_count
            })

        return jsonify(reply_list)

    except Exception as e:
        print(e)
        return jsonify({"error": "リプライ取得エラー"}), 500


# 投稿いいね切替
@app.route("/api/posts/<int:post_id>/likes", methods=["POST"])
def toggle_post_like(post_id):
    try:
        data = request.get_json()
        account_id = data.get("account_id")
        rows = fetch_all(
            """
            SELECT like_id
            FROM likes
            WHERE account_id = :account_id
            AND post_id = :post_id
            """,
            {
                "account_id": account_id,
                "post_id": post_id
            }
        )

        if rows:
            execute(
                """
                DELETE FROM likes
                WHERE like_id = :like_id
                """,
                {
                    "like_id": rows[0].like_id
                }
            )

            liked = False

        else:
            execute(
                """
                INSERT INTO likes (
                    account_id,
                    post_id
                )
                VALUES (
                    :account_id,
                    :post_id
                )
                """,
                {
                    "account_id": account_id,
                    "post_id": post_id
                }
            )

            liked = True

        return jsonify({
            "liked": liked
        })

    except Exception as e:
        print(e)
        return jsonify({
            "error": "いいねエラー"
        }), 500


# リプライいいね切替
@app.route("/api/replies/<int:reply_id>/likes", methods=["POST"])
def toggle_reply_like(reply_id):
    try:
        data = request.get_json()
        account_id = data.get("account_id")

        rows = fetch_all(
            """
            SELECT like_id
            FROM likes
            WHERE account_id = :account_id
            AND reply_id = :reply_id
            """,
            {
                "account_id": account_id,
                "reply_id": reply_id
            }
        )

        if rows:
            execute(
                """
                DELETE FROM likes
                WHERE like_id = :like_id
                """,
                {
                    "like_id": rows[0].like_id
                }
            )
            liked = False

        else:
            execute(
                """
                INSERT INTO likes (
                    account_id,
                    reply_id
                )
                VALUES (
                    :account_id,
                    :reply_id
                )
                """,
                {
                    "account_id": account_id,
                    "reply_id": reply_id
                }
            )
            liked = True

        return jsonify({
            "liked": liked
        })

    except Exception as e:
        print(e)
        return jsonify({
            "error": "いいねエラー"
        }), 500
        

############################################################################
### 実行制御
############################################################################
if __name__ == "__main__":
    app.run(debug=True)
    