import datetime
from typing import Dict, Optional
from .security import generate_session_id
from .utils import get_default_user_id


class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}

    def add_session(self, user_id: Optional[str] = None, duration_seconds: int = 3600) -> str:
        session_id = generate_session_id()
        user_id = user_id or get_default_user_id()
        now = datetime.datetime.now()
        self.sessions[session_id] = {
            "user_id": user_id,
            "start_time": now,
            "end_time": now + datetime.timedelta(seconds=duration_seconds)
        }
        return session_id

    def remove_session(self, session_id: str):
        self.sessions.pop(session_id, None)

    def get_session(self, session_id: str) -> Optional[Dict]:
        return self.sessions.get(session_id)

    def is_active(self, session_id: str) -> bool:
        session = self.get_session(session_id)
        if session:
            now = datetime.datetime.now()
            return session["start_time"] <= now <= session["end_time"]
        return False

    def get_time_remaining(self, session_id: str) -> float:
        session = self.get_session(session_id)
        if session:
            return (session["end_time"] - datetime.datetime.now()).total_seconds()
        return 0.0
    
    def time_passed(self, session_id: str) -> float:
        session = self.get_session(session_id)
        if session:
            return (datetime.datetime.now() - session["end_time"]).total_seconds()
        return 0.0
    

    def get_all_sessions(self):
        return self.sessions
