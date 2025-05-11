import os

def get_default_user_id() -> str:
    return os.getenv("DEFAULT_USER_ID", "default_user").lower()

# File: pysessionmanager/persistence.py
import json
from typing import Dict


def save_sessions_to_file(sessions: Dict, filepath: str):
    with open(filepath, 'w') as f:
        json.dump(sessions, f, default=str)


def load_sessions_from_file(filepath: str) -> Dict:
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}