from pysessionmanager.core import SessionManager
import time

def test_session_lifecycle():
    sm = SessionManager()
    session_id = sm.add_session("testuser", duration_seconds=2)
    assert sm.is_active(session_id) is True
    time.sleep(3)
    assert sm.is_active(session_id) is False