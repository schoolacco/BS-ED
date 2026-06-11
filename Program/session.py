import os
import json
import time
import db
import hmac
import hashlib
import dotenv
from data import global_path_reference
dotenv.load_dotenv(f"{global_path_reference}bsed.env")
ANTICHEAT = os.getenv("ANTICHEAT")
SESSION_FILE = f"{global_path_reference}/session.json"
SESSION_DURATION = 60 * 60 * 24 * 30  # 30 days

def create_session(username: str):
    session = {
        "username": username,
        "created_at": time.time(),
    }
    session["signature"] = generate_signature(json.dumps(session, sort_keys=True))
    with open(SESSION_FILE, "w") as f:
        json.dump(session, f)

def load_session():
    if not os.path.exists(SESSION_FILE):
        return None

    try:
        with open(SESSION_FILE, "r") as f:
            session = json.load(f)
        sig = session["signature"]
        del session["signature"]
        if not hmac.compare_digest(generate_signature(json.dumps(session, sort_keys=True)), sig):
            raise ValueError("You tampered with my stuff D:<")
        # expiry check
        if time.time() - session["created_at"] > SESSION_DURATION:
            delete_session()
            return None

        return session

    except Exception:
        return None

def validate_session() -> str|None:
    session = load_session()
    if not session:
        return None

    username: str = session.get("username")
    if not username:
        return None

    # confirm user still exists in DB
    account = db.get_account(username)
    if not account:
        delete_session()
        return None

    return username

def delete_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
def generate_signature(data: str) -> str:
    return hmac.new(ANTICHEAT.encode(), data.encode(), hashlib.sha256).hexdigest()