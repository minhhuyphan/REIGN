import json
import os
import hashlib
import hmac
import secrets

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'du_lieu', 'save')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
SESSION_FILE = os.path.join(DATA_DIR, 'session.json')


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _hash_password(password: str, salt: str) -> str:
    """Hash password using PBKDF2-HMAC-SHA256 with provided salt."""
    pwd = password.encode('utf-8')
    salt_b = salt.encode('utf-8')
    dk = hashlib.pbkdf2_hmac('sha256', pwd, salt_b, 100_000)
    return dk.hex()


def load_users():
    ensure_data_dir()
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_users(users: dict):
    ensure_data_dir()
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def register_user(username: str, password: str) -> bool:
    """Register a new user. Returns True if created, False if username exists."""
    users = load_users()
    if username in users:
        return False
    salt = secrets.token_hex(16)
    pw_hash = _hash_password(password, salt)
    users[username] = {
        'salt': salt,
        'pw_hash': pw_hash
    }
    save_users(users)
    return True


def authenticate(username: str, password: str) -> bool:
    users = load_users()
    user = users.get(username)
    if not user:
        return False
    salt = user.get('salt')
    expected = user.get('pw_hash')
    if not salt or not expected:
        return False
    pw_hash = _hash_password(password, salt)
    return hmac.compare_digest(pw_hash, expected)


def save_current_user(username: str | None):
    """Save the currently logged-in username (or null to clear)."""
    ensure_data_dir()
    data = {'current_user': username}
    with open(SESSION_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_current_user() -> str | None:
    """Return the remembered username or None."""
    ensure_data_dir()
    if not os.path.exists(SESSION_FILE):
        return None
    try:
        with open(SESSION_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('current_user')
    except Exception:
        return None


def clear_session():
    try:
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
    except Exception:
        pass


if __name__ == '__main__':
    # quick interactive test
    print('Users file:', USERS_FILE)
    print('Existing users:', load_users())
