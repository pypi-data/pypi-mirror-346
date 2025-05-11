import datetime
import json
from typing import Dict, Optional
from .security import generate_session_id, hash_password, verify_password
from .utils import get_default_user_id


class SessionManager:
    def __init__(self, load: bool = False, protect_all: bool = False):
        """
        Manage user sessions with optional time-based expiration and optional per-session password protection.
        """
        self.sessions: Dict[str, Dict] = {}
        self.filename = "sessions.json"
        self.protect_all = protect_all
        if load:
            self.load_sessions(self.filename)

    def add_session(
        self,
        user_id: str = None,
        duration_seconds: int = 3600,
        protected: bool = False,
        password: Optional[str] = None
    ) -> str:
        """
        Add a new session.

        Args:
            user_id (str): Optional user identifier.
            duration_seconds (int): Lifetime of session in seconds.
            protected (bool): Whether this session is password-protected.
            password (str): Password to unlock the session if protected.

        Returns:
            str: The generated session ID.
        """
        session_id = generate_session_id()
        if user_id is None and not self.sessions:
            user_id = user_id or get_default_user_id()
        
        if protected and not password:
            raise ValueError("Password is required for protected sessions.")
        
        if self.protect_all and not password:
            raise ValueError("Password is required for all sessions due to global protection setting.")
        
        if protected and password or self.protect_all and password:
            if len(password) < 8:
                raise ValueError("Password must be at least 8 characters long.")
            if not any(char.isdigit() for char in password):
                raise ValueError("Password must contain at least one digit.")
            if not any(char.isalpha() for char in password):
                raise ValueError("Password must contain at least one letter.")
            
        if protected and password or self.protect_all and password:
            new_password = hash_password(password) 
        else:
            new_password = None

        now = datetime.datetime.now()
        self.sessions[session_id] = {
            "user_id": user_id,
            "start_time": now,
            "end_time": now + datetime.timedelta(seconds=duration_seconds),
            "protected": protected,
            "password": new_password
        }
        return session_id

    def remove_session(self, session_id: str):
        """
        Remove a session by ID.
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session ID {session_id} not found.")
        self.sessions.pop(session_id)

    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        Get the session dictionary for a given session ID.
        """
        if session_id in self.sessions:
            return self.sessions[session_id]
        else:
            raise ValueError(f"Session ID {session_id} not found.")

    def is_active(self, session_id: str) -> bool:
        """
        Check if the session is currently active.
        """
        session = self.get_session(session_id)
        now = datetime.datetime.now()
        return session["start_time"] <= now <= session["end_time"]

    def get_time_remaining(self, session_id: str) -> float:
        """
        Get the number of seconds remaining before the session expires.
        """
        session = self.get_session(session_id)
        return max((session["end_time"] - datetime.datetime.now()).total_seconds(), 0.0)

    def time_passed(self, session_id: str) -> float:
        """
        Get the number of seconds that have passed since the session started.
        """
        session = self.get_session(session_id)
        return max((datetime.datetime.now() - session["start_time"]).total_seconds(), 0.0)

    def get_all_sessions(self) -> Dict[str, Dict]:
        """
        Return all sessions.
        """
        return self.sessions

    def store_sessions(self, filename: str = None):
        """
        Save sessions to a JSON file.
        """
        filename = filename or self.filename
        sessions_to_save = {
            session_id: {
                "user_id": session["user_id"],
                "start_time": session["start_time"].isoformat(),
                "end_time": session["end_time"].isoformat(),
                "protected": session["protected"],
                "password": session.get("password")
            }
            for session_id, session in self.sessions.items()
        }
        with open(filename, 'w') as f:
            json.dump(sessions_to_save, f)

    def load_sessions(self, filename: str = None):
        """
        Load sessions from a JSON file.
        """
        filename = filename or self.filename
        try:
            with open(filename, 'r') as f:
                self.sessions = json.load(f)
            for session_id, session in self.sessions.items():
                session["start_time"] = datetime.datetime.fromisoformat(session["start_time"])
                session["end_time"] = datetime.datetime.fromisoformat(session["end_time"])
                session["protected"] = session.get("protected", False)
                session["password"] = session.get("password")
                session["user_id"] = session.get("user_id", get_default_user_id())
        except FileNotFoundError:
            self.sessions = {}

    def clear_sessions(self):
        """
        Clear all sessions and overwrite the session file.
        """
        self.sessions.clear()
        with open(self.filename, 'w') as f:
            json.dump(self.sessions, f)

    def get_session_by_user_id(self, user_id: str) -> Optional[str]:
        """
        Get the session ID for a given user ID, if the session is not protected.
        """
        for session_id, session in self.sessions.items():
            if not session.get("protected") and session["user_id"] == user_id:
                return session_id
            if session.get("protected") and session["user_id"] == user_id:
                raise ValueError("Session is protected. Please unlock it first.")
        return None

    def unlock_session(self, user_id: str, password: str):
        """
        Unlock a protected session for a given user_id by verifying the hashed password.
        """
        # Find the protected session by user_id
        for session_id, session in self.sessions.items():
            if session["user_id"] == user_id and session.get("protected"):
                if verify_password(password, session.get("password")):
                    session["protected"] = False
                    session["password"] = None
                    return  # Successfully unlocked
                else:
                    raise ValueError("Incorrect password.")
        
        raise ValueError("Protected session for this user not found.")
