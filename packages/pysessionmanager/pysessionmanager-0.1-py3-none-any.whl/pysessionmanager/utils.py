import os

def get_default_user_id() -> str:
    return os.getenv("DEFAULT_USER_ID", "default_user").lower()