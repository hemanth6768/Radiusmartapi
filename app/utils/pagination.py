import base64
import json
from fastapi import HTTPException


def encode_cursor(data: dict) -> str:
    try:
        json_str = json.dumps(data)
        return base64.urlsafe_b64encode(json_str.encode()).decode()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to encode cursor")


def decode_cursor(cursor: str):
    try:
        decoded = base64.urlsafe_b64decode(cursor.encode()).decode()
        return json.loads(decoded)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid cursor")