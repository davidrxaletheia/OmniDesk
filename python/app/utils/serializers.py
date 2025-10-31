from pydantic.json import pydantic_encoder
import json
from datetime import datetime

def parse_iso_datetime(value: str | None):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

def to_jsonable(obj):
    return json.loads(json.dumps(obj, default=pydantic_encoder))