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

# TOP
@app.route("/")
def index():

    return render_template(
        "index.html"
    )

# ルーム一覧取得
@app.route("/rooms")
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
@app.route("/messages/<int:room_id>")
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


@app.route("/chat", methods=["POST"])
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


############################################################################
### 実行制御
############################################################################
if __name__ == "__main__":
    app.run(debug=True)
