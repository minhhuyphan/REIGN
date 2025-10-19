import json
import os
from typing import Dict, List, Any

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'du_lieu', 'save')
HIGH_SCORES_FILE = os.path.join(DATA_DIR, 'high_scores.json')


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_high_scores() -> Dict[str, List[Dict[str, Any]]]:
    ensure_data_dir()
    if not os.path.exists(HIGH_SCORES_FILE):
        return {}
    try:
        with open(HIGH_SCORES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_high_scores(data: Dict[str, List[Dict[str, Any]]]):
    ensure_data_dir()
    with open(HIGH_SCORES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_score(level_key: str, username: str, score: int, max_entries: int = 10):
    data = load_high_scores()
    if level_key not in data:
        data[level_key] = []
    entry = {'user': username or 'Guest', 'score': int(score)}
    data[level_key].append(entry)
    data[level_key] = sorted(data[level_key], key=lambda e: e['score'], reverse=True)[:max_entries]
    save_high_scores(data)


def get_top_scores(level_key: str, n: int = 10):
    data = load_high_scores()
    return data.get(level_key, [])[:n]
