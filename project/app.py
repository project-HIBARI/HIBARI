import os
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Flask のリローダー子プロセスでも同ディレクトリのモジュールを import できるようにする
sys.path.insert(0, str(Path(__file__).resolve().parent))

from flask import Flask, render_template, jsonify, request, session, redirect, send_from_directory
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

from sqlalchemy import create_engine
from sqlalchemy import text

from google import genai

from zoneinfo import ZoneInfo

from password_utils import (
    hash_password,
    normalize_email,
    needs_password_upgrade,
    verify_password,
)


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

# 掲示板メディアアップロード
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POST_UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads", "posts")
ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "webm", "mov"}
MAX_POST_IMAGE_BYTES = 10 * 1024 * 1024
MAX_POST_VIDEO_BYTES = 50 * 1024 * 1024

os.makedirs(POST_UPLOAD_FOLDER, exist_ok=True)

# ユーザーキャッシュ（email -> {user_data, expire_at}）
user_cache = {}


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
    
    
def ensure_post_media_schema():
    """掲示板投稿用の video_path カラムを追加（未作成時のみ）"""
    try:
        execute(
            """
            ALTER TABLE posts
            ADD COLUMN IF NOT EXISTS video_path VARCHAR(500)
            """
        )
    except Exception as e:
        print("post media schema:", e)


def get_post_media_type(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext in ALLOWED_IMAGE_EXTENSIONS:
        return "image"
    if ext in ALLOWED_VIDEO_EXTENSIONS:
        return "video"
    return None


def save_post_media_file(file_storage):
    if not file_storage or not file_storage.filename:
        return None, None

    original_name = secure_filename(file_storage.filename)
    media_type = get_post_media_type(original_name)
    if not media_type:
        raise ValueError("対応していないファイル形式です")

    file_storage.seek(0, os.SEEK_END)
    size = file_storage.tell()
    file_storage.seek(0)

    max_size = MAX_POST_IMAGE_BYTES if media_type == "image" else MAX_POST_VIDEO_BYTES
    if size > max_size:
        limit_mb = max_size // (1024 * 1024)
        raise ValueError(f"ファイルサイズは{limit_mb}MB以下にしてください")

    ext = original_name.rsplit(".", 1)[-1].lower()
    stored_name = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(POST_UPLOAD_FOLDER, stored_name)
    file_storage.save(save_path)

    public_path = f"/uploads/posts/{stored_name}"
    return public_path, media_type


ensure_post_media_schema()
    
    
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
    

# UTCを日本時間に変換する関数
def utc_to_jst(utc_dt):
    jst_tz = ZoneInfo("Asia/Tokyo")
    return utc_dt.astimezone(jst_tz)


# datetime を受け取り JST の ISO 文字列にするヘルパー
def to_jst_str(dt):
    if dt is None:
        return None
    # タイムゾーン情報が無い場合は UTC と見なす
    if dt.tzinfo is None:
        from datetime import timezone
        dt = dt.replace(tzinfo=timezone.utc)
    try:
        jst_dt = utc_to_jst(dt)
        return jst_dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return str(dt)


# ユーザーキャッシュ管理
#   キャッシュからユーザーを取得
def get_cached_user(email):
    key = normalize_email(email)
    if key not in user_cache:
        return None
    
    cached_data = user_cache[key]
    
    # 有効期限チェック
    if datetime.now() > cached_data['expire_at']:
        del user_cache[key]
        return None
    
    return cached_data['user']


#   ユーザーをキャッシュに保存
def cache_user(email, user):
    key = normalize_email(email)
    user_cache[key] = {
        'user': user,
        'expire_at': datetime.now() + timedelta(minutes=30) # 有効期限: 30分
    }


# セッションからユーザー情報取得
#   全体取得
def get_current_user_from_session():
    if "account_id" not in session:
        return None

    return {
        "account_id": session["account_id"],
        "name": session.get("name"),
        "email": session.get("email")
    }

#   アカウントIDのみ取得
def get_session_account_id():
    account_id = session.get("account_id")
    if account_id is None:
        raise ValueError("ログインが必要です")
    return account_id


def get_membership_for_account(account_id):
    rows = fetch_all(
        """
        SELECT is_premium
        FROM fanclub_join_historys
        WHERE account_id = :account_id
        ORDER BY purchased_at DESC
        LIMIT 1
        """,
        {"account_id": account_id}
    )
    if not rows:
        return "general"
    return "premium" if rows[0].is_premium else "general"


def build_user_response(account_id, name, email):
    membership = get_membership_for_account(account_id)
    return {
        "account_id": account_id,
        "name": name,
        "email": email,
        "membership": membership,
        "is_premium": membership == "premium",
    }


def fetch_account_row(account_id):
    rows = fetch_all(
        """
        SELECT account_id, name, email, password, address
        FROM accounts
        WHERE account_id = :account_id
        """,
        {"account_id": account_id},
    )
    if not rows:
        return None
    return dict(rows[0])


############################################################################
### パス
############################################################################

############################################################################
### デバッグページ
############################################################################

# デバッグ用 AI美空ひばり
@app.route("/")
def index():
    try:
        current_user = get_current_user_from_session()
        if not current_user:
            return redirect('/debug/login')
        return render_template(
            "index.html",
            current_user=current_user,
            is_logged_in=True
        )
    except Exception as e:
        print(e)
        return f"テンプレート読み込みエラー: {e}", 500
    

# デバッグ用 ログインページ
@app.route('/debug/login')
def debug_login():
    try:
        current_user = get_current_user_from_session()
        return render_template(
            'debug_login.html',
            current_user=current_user,
            is_logged_in=current_user is not None
        )
    except Exception as e:
        print(e)
        return f"テンプレート読み込みエラー: {e}", 500


# デバッグ用 掲示板呼び出しページ
@app.route('/debug/post')
def debug_post():
    try:
        current_user = get_current_user_from_session()
        if not current_user:
            return redirect('/debug/login')
        return render_template(
            'debug_post.html',
            current_user=current_user,
            is_logged_in=True
        )
    except Exception as e:
        print(e)
        return f"テンプレート読み込みエラー: {e}", 500


# デバッグ用 献花呼び出しページ
@app.route('/debug/flower-offerings')
def debug_flower_offerings():
    try:
        current_user = get_current_user_from_session()
        return render_template(
            'debug_flower.html',
            current_user=current_user,
            is_logged_in=current_user is not None
        )
    except Exception as e:
        print(e)
        return f"テンプレート読み込みエラー: {e}", 500    
    

# デバッグ用 アカウント登録ページ
@app.route('/debug/account')
def debug_account():
    try:
        current_user = get_current_user_from_session()
        return render_template(
            'debug_accounts.html',
            current_user=current_user,
            is_logged_in=current_user is not None
        )
    except Exception as e:
        print(e)
        return f"テンプレート読み込みエラー: {e}", 500


# デバッグ用 ファンクラブ登録ページ
@app.route('/debug/fanclub')
def debug_fanclub():
    try:
        current_user = get_current_user_from_session()
        if not current_user:
            return redirect('/debug/login')
        return render_template(
            'debug_fanclub.html',
            current_user=current_user,
            is_logged_in=True
        )
    except Exception as e:
        print(e)
        return f"テンプレート読み込みエラー: {e}", 500


############################################################################
### API パス
############################################################################

# アカウント新規登録
@app.route("/api/accounts", methods=["POST"])
def create_account():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSONデータが空です"}), 400
            
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        address = data.get("address")
        is_premium = data.get("is_premium", False)

        if not name or not email or not password:
            return jsonify({"error": "名前、メールアドレス、パスワードは必須項目です"}), 400

        name_val = name.strip()
        email_val = normalize_email(email)
        password_val = hash_password(password)
        address_val = address.strip() if isinstance(address, str) and address.strip() else None
        is_premium_val = bool(is_premium)

        account_id = execute_insert(
            """
            INSERT INTO accounts (
                name,
                email,
                password,
                address
            )
            VALUES (
                :name,
                :email,
                :password,
                :address
            )
            RETURNING account_id
            """,
            {
                "name": name_val,
                "email": email_val,
                "password": password_val,
                "address": address_val
            }
        )

        execute_insert(
            """
            INSERT INTO fanclub_join_historys (
                account_id,
                is_premium,
                purchased_at
            )
            VALUES (
                :account_id,
                :is_premium,
                NOW()
            )
            RETURNING fanclub_join_history_id
            """,
            {
                "account_id": account_id,
                "is_premium": is_premium_val
            }
        )

        membership = "premium" if is_premium_val else "general"

        session["account_id"] = account_id
        session["name"] = name_val
        session["email"] = email_val
        session["membership"] = membership

        return jsonify({
            "success": True,
            "message": "登録できました",
            "account_id": account_id,
            "user": {
                "account_id": account_id,
                "name": name_val,
                "email": email_val,
                "membership": membership,
                "is_premium": is_premium_val,
            }
        }), 201

    except Exception as e:
        print(e)
        return jsonify({
            "error": "アカウント登録エラー"
        }), 500
        
        
def complete_login(user, password, stored_hash, cached=False):
    if needs_password_upgrade(stored_hash):
        try:
            execute(
                """
                UPDATE accounts
                SET password = :password
                WHERE account_id = :account_id
                """,
                {
                    "password": hash_password(password),
                    "account_id": user["account_id"],
                },
            )
            user["password"] = hash_password(password)
            cache_user(user["email"], user)
        except Exception as e:
            print("password upgrade:", e)

    membership = get_membership_for_account(user["account_id"])
    session["account_id"] = user["account_id"]
    session["name"] = user["name"]
    session["email"] = user["email"]
    session["membership"] = membership
    return jsonify({
        "success": True,
        "user": build_user_response(
            user["account_id"],
            user["name"],
            user["email"],
        ),
        "cached": cached,
    })


# ログイン
@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSONデータが空です"}), 400
        
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            return jsonify({"error": "メールアドレスとパスワードは必須項目です"}), 400
        
        email_key = normalize_email(email)
        
        # キャッシュからユーザーをチェック
        cached_user = get_cached_user(email_key)
        if cached_user and verify_password(cached_user['password'], password):
            return complete_login(cached_user, password, cached_user['password'], cached=True)
        
        # DB から検索（メールは大文字小文字を区別しない）
        result = fetch_all(
            """
            SELECT account_id, name, email, password
            FROM accounts
            WHERE lower(email) = :email
            """,
            {"email": email_key}
        )
        
        if not result:
            return jsonify({"error": "認証に失敗しました"}), 401
        
        row = result[0]._mapping
        user = {
            "account_id": row["account_id"],
            "name": row["name"],
            "email": row["email"],
            "password": row["password"],
        }
        stored_hash = user["password"] or ""
        
        # パスワード確認（pbkdf2 / 旧 scrypt 両対応）
        if not verify_password(stored_hash, password):
            return jsonify({"error": "認証に失敗しました"}), 401
        
        # キャッシュに保存
        cache_user(email_key, user)
        
        return complete_login(user, password, stored_hash, cached=False)
    
    except Exception as e:
        print(e)
        return jsonify({"error": "ログインエラー"}), 500


# ログアウト
@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    
    return jsonify({
        "success": True
    })


# ログイン確認
@app.route("/api/me", methods=["GET"])
def me():

    if "account_id" not in session:
        return jsonify({
            "login": False
        }), 401

    return jsonify({
        "login": True,
        "user": build_user_response(
            session["account_id"],
            session["name"],
            session["email"]
        )
    })


# アカウント情報取得（会員ページ用）
@app.route("/api/account", methods=["GET"])
def get_account():
    try:
        account_id = get_session_account_id()
    except ValueError:
        return jsonify({"error": "ログインが必要です"}), 401

    row = fetch_account_row(account_id)
    if not row:
        return jsonify({"error": "アカウントが見つかりません"}), 404

    user = build_user_response(row["account_id"], row["name"], row["email"])
    user["address"] = row.get("address") or ""

    return jsonify({"account": user})


# アカウント情報更新（氏名・メール・住所）
@app.route("/api/account", methods=["PATCH"])
def update_account():
    try:
        account_id = get_session_account_id()
    except ValueError:
        return jsonify({"error": "ログインが必要です"}), 401

    data = request.get_json() or {}
    row = fetch_account_row(account_id)
    if not row:
        return jsonify({"error": "アカウントが見つかりません"}), 404

    name = data.get("name", row["name"])
    email = data.get("email", row["email"])
    address = data.get("address", row.get("address"))

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "氏名を入力してください"}), 400
    if not isinstance(email, str) or not email.strip():
        return jsonify({"error": "メールアドレスを入力してください"}), 400

    name_val = name.strip()
    email_val = normalize_email(email)
    address_val = address.strip() if isinstance(address, str) and address.strip() else None

    if email_val != normalize_email(row["email"]):
        existing = fetch_all(
            "SELECT account_id FROM accounts WHERE email = :email AND account_id != :account_id",
            {"email": email_val, "account_id": account_id},
        )
        if existing:
            return jsonify({"error": "このメールアドレスは既に登録されています"}), 409

    execute(
        """
        UPDATE accounts
        SET name = :name, email = :email, address = :address
        WHERE account_id = :account_id
        """,
        {
            "name": name_val,
            "email": email_val,
            "address": address_val,
            "account_id": account_id,
        },
    )

    session["name"] = name_val
    session["email"] = email_val

    user = build_user_response(account_id, name_val, email_val)
    user["address"] = address_val or ""

    return jsonify({
        "success": True,
        "message": "アカウント情報を更新しました",
        "account": user,
        "user": user,
    })


# パスワード変更
@app.route("/api/account/password", methods=["PATCH"])
def update_account_password():
    try:
        account_id = get_session_account_id()
    except ValueError:
        return jsonify({"error": "ログインが必要です"}), 401

    data = request.get_json() or {}
    current_password = data.get("current_password", "")
    new_password = data.get("new_password", "")

    if not current_password or not new_password:
        return jsonify({"error": "現在のパスワードと新しいパスワードを入力してください"}), 400
    if len(new_password) < 8:
        return jsonify({"error": "新しいパスワードは8文字以上で設定してください"}), 400

    row = fetch_account_row(account_id)
    if not row:
        return jsonify({"error": "アカウントが見つかりません"}), 404

    if not verify_password(row["password"], current_password):
        return jsonify({"error": "現在のパスワードが正しくありません"}), 401

    new_hash = hash_password(new_password)
    execute(
        """
        UPDATE accounts
        SET password = :password
        WHERE account_id = :account_id
        """,
        {"password": new_hash, "account_id": account_id},
    )

    row["password"] = new_hash
    cache_user(row["email"], row)

    return jsonify({
        "success": True,
        "message": "パスワードを変更しました",
    })

    
# ルーム一覧取得
@app.route("/api/rooms")
def rooms():
    try:
        try:
            account_id = get_session_account_id()
        except ValueError:
            return jsonify({
                "error": "ログインが必要です",
                "redirect": "/debug/login"
            }), 401

        rows = fetch_all(
            """
            SELECT
                ai_chat_room_id,
                room_name,
                created_at
            FROM ai_chat_rooms
            WHERE account_id = :account_id
            ORDER BY created_at DESC
            """,
            {"account_id": account_id}
        )

        room_list = []

        for row in rows:
            room_list.append({
                "ai_chat_room_id": row.ai_chat_room_id,
                "room_name": row.room_name,
                "created_at": to_jst_str(row.created_at)
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
        try:
            account_id = get_session_account_id()
        except ValueError:
            return jsonify({
                "error": "ログインが必要です",
                "redirect": "/debug/login"
            }), 401

        room_rows = fetch_all(
            """
            SELECT ai_chat_room_id
            FROM ai_chat_rooms
            WHERE ai_chat_room_id = :room_id
            AND account_id = :account_id
            """,
            {
                "room_id": room_id,
                "account_id": account_id
            }
        )

        if not room_rows:
            return jsonify({
                "error": "このルームにはアクセスできません"
            }), 403

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
                "created_at": to_jst_str(row.created_at)
            })

        return jsonify(message_list)

    except Exception as e:
        print(e)
        return jsonify({
            "error": "メッセージ取得エラー"
        }), 500


# AIチャット応答生成
@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        try:
            account_id = get_session_account_id()
        except ValueError:
            return jsonify({
                "error": "ログインが必要です",
                "redirect": "/debug/login"
            }), 401

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
                AND account_id = :account_id
                """,
                {
                    "room_id": room_id,
                    "account_id": account_id
                }
            )

            if not room_rows:
                return jsonify({
                    "error": "このルームにはアクセスできません"
                }), 403

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
                p.video_path,
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
                "created_at": to_jst_str(row.created_at),
                "name": row.name,
                "age": row.age,
                "location": row.location,
                "image_path": row.image_path,
                "video_path": getattr(row, "video_path", None),
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


# 掲示板メディアアップロード
@app.route("/api/posts/upload", methods=["POST"])
def upload_post_media():
    if "account_id" not in session:
        return jsonify({"error": "ログインが必要です"}), 401

    file = request.files.get("file")
    if not file:
        return jsonify({"error": "ファイルがありません"}), 400

    try:
        public_path, media_type = save_post_media_file(file)
        return jsonify({
            "path": public_path,
            "media_type": media_type,
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": "アップロードに失敗しました"}), 500


@app.route("/uploads/posts/<path:filename>")
def serve_post_upload(filename):
    safe_name = secure_filename(filename)
    return send_from_directory(POST_UPLOAD_FOLDER, safe_name)


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
                image_path,
                video_path
            )
            VALUES (
                :song_id,
                :title,
                :content,
                :name,
                :age,
                :location,
                :image_path,
                :video_path
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
                "image_path": data.get("image_path"),
                "video_path": data.get("video_path"),
            }
        )

        return jsonify({
            "message": "投稿しました",
            "post_id": post_id,
            "image_path": data.get("image_path"),
            "video_path": data.get("video_path"),
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
                "created_at": to_jst_str(row.created_at),
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
        try:
            account_id = get_session_account_id()
        except ValueError:
            return jsonify({
                "error": "ログインが必要です",
                "redirect": "/debug/login"
            }), 401
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
        try:
            account_id = get_session_account_id()
        except ValueError:
            return jsonify({
                "error": "ログインが必要です",
                "redirect": "/debug/login"
            }), 401

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
        

# 献花一覧取得
@app.route("/api/flower-offerings", methods=["GET"])
def get_flower_offerings():
    try:
        rows = fetch_all(
            """
            SELECT
                f.flower_offering_id,
                f.content,
                f.offered_at,
                f.name,
                f.age,
                f.location,
                f.flower_type
            FROM flower_offerings f
            ORDER BY f.offered_at DESC
            """
        )
        offering_list = []

        for row in rows:
            offering_list.append({
                "flower_offering_id": row.flower_offering_id,
                "content": row.content,
                "offered_at": to_jst_str(row.offered_at),
                "name": row.name,
                "age": row.age,
                "location": row.location,
                "flower_type": row.flower_type
            })

        return jsonify(offering_list)

    except Exception as e:
        print(e)
        return jsonify({
            "error": "献花情報の取得エラー"
        }), 500
        
        
#新しい献花登録
@app.route("/api/flower-offerings", methods=["POST"])
def create_flower_offering():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSONデータが空です"}), 400
            
        content = data.get("content")
        flower_type = data.get("flower_type")
        name = data.get("name")
        age = data.get("age")
        location = data.get("location")

        if not content or not flower_type:
            return jsonify({"error": "本文と花の種類は必須項目です"}), 400

        name_val = name.strip() if name and name.strip() else "匿名希望"
        age_val = int(age) if age else None
        location_val = location.strip() if location and location.strip() else None

        flower_offering_id = execute_insert(
            """
            INSERT INTO flower_offerings (
                content,
                offered_at,
                name,
                age,
                location,
                flower_type
            )
            VALUES (
                :content,
                NOW(),
                :name,
                :age,
                :location,
                :flower_type
            )
            RETURNING flower_offering_id
            """,
            {
                "content": content,
                "name": name_val,
                "age": age_val,
                "location": location_val,
                "flower_type": flower_type
            }
        )

        return jsonify({
            "message": "献花が完了しました",
            "flower_offering_id": flower_offering_id
        })

    except ValueError:
        return jsonify({"error": "年齢には数値を入力してください"}), 400
    except Exception as e:
        print(e)
        return jsonify({
            "error": "献花登録エラー"
        }), 500


# ファンクラブ登録
@app.route("/api/fanclub", methods=["POST"])
def create_fanclub():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSONデータが空です"}), 400

        current_user = get_current_user_from_session()
        if not current_user:
            return jsonify({"error": "ログインが必要です"}), 401

        account_id = current_user["account_id"]
        is_premium = data.get("is_premium")

        if is_premium is None:
            return jsonify({"error": "is_premiumは必須項目です"}), 400

        fanclub_join_history_id = execute_insert(
            """
            INSERT INTO fanclub_join_historys (
                account_id,
                is_premium,
                purchased_at
            )
            VALUES (
                :account_id,
                :is_premium,
                NOW()
            )
            RETURNING fanclub_join_history_id
            """,
            {
                "account_id": account_id,
                "is_premium": is_premium
            }
        )

        return jsonify({
            "message": "ファンクラブ登録しました",
            "fanclub_join_history_id": fanclub_join_history_id
        }), 201

    except Exception as e:
        print(e)
        return jsonify({"error": "ファンクラブ登録エラー", "detail": str(e)}), 500
 

############################################################################
### 実行制御
############################################################################
if __name__ == "__main__":
    app.run(debug=True)
    