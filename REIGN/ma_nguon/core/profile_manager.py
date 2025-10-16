import json
import os
from typing import Dict, Any

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'du_lieu', 'save')
PROFILE_FILE = os.path.join(DATA_DIR, 'profiles.json')


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_profiles() -> Dict[str, Any]:
    ensure_data_dir()
    if not os.path.exists(PROFILE_FILE):
        return {}
    try:
        with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_profiles(profiles: Dict[str, Any]):
    ensure_data_dir()
    with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)


def load_profile(username: str) -> Dict[str, Any]:
    profiles = load_profiles()
    default = {
        'gold': 0,
        'purchased_characters': ['chien_binh'],  # grant free warrior by default
        # owned_equipment stores equipment ids the player owns (by default empty)
        'owned_equipment': [],
        # For backward compatibility older profiles may lack these keys
    }
    return profiles.get(username, default)


def save_profile(username: str, profile: Dict[str, Any]):
    profiles = load_profiles()
    profiles[username] = profile
    save_profiles(profiles)
