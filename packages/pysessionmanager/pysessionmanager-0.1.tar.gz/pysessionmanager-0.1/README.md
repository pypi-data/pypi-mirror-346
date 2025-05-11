# PySessionManager

Een uitbreidbare sessiebeheer library voor Python CLI- en webapplicaties.

## Installatie
```bash
pip install pysessionmanager
```

## Voorbeeld
```python
from pysessionmanager import SessionManager

sm = SessionManager()
session_id = sm.add_session("mijn_gebruiker")
print("Gestart:", session_id)
```

## Features
- Start/stop sessies
- TTL support
- Web en CLI bruikbaar
- Flask-demo