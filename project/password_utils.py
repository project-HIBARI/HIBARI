"""
掲示板・認証向けパスワード検証ユーティリティ

旧 Werkzeug の scrypt ハッシュは現行環境の check_password_hash では
検証できないため、hashlib.scrypt での検証と pbkdf2 への移行を行う。
"""
import hashlib
import hmac

from werkzeug.security import check_password_hash, generate_password_hash


def normalize_email(email: str) -> str:
    return (email or "").strip().lower()


def _verify_werkzeug_scrypt(pwhash: str, password: str) -> bool:
    if pwhash.count("$") < 2:
        return False

    method, salt, hashval = pwhash.split("$", 2)
    parts = method.split(":")
    if len(parts) != 4 or parts[0] != "scrypt":
        return False

    try:
        n, r, p = int(parts[1]), int(parts[2]), int(parts[3])
    except ValueError:
        return False

    password_b = password.encode("utf-8")
    salt_b = salt.encode("utf-8")

    try:
        dk = hashlib.scrypt(
            password_b,
            salt=salt_b,
            n=n,
            r=r,
            p=p,
            maxmem=132 * n * r * p,
        )
    except (ValueError, OSError):
        return False

    return hmac.compare_digest(dk.hex(), hashval)


def verify_password(stored_hash: str, password: str) -> bool:
    if not stored_hash or not password:
        return False

    try:
        if check_password_hash(stored_hash, password):
            return True
    except Exception:
        pass

    if stored_hash.startswith("scrypt:"):
        return _verify_werkzeug_scrypt(stored_hash, password)

    # 旧データ: 平文パスワードが残っている場合（ログイン成功時に pbkdf2 へ移行）
    return hmac.compare_digest(stored_hash, password)


def needs_password_upgrade(stored_hash: str) -> bool:
    if not stored_hash:
        return False
    return not stored_hash.startswith("pbkdf2:")


def hash_password(password: str) -> str:
    return generate_password_hash(password, method="pbkdf2:sha256")
