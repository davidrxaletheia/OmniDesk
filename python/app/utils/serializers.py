import json
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


def parse_iso_datetime(value: str | None):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _default_encoder(o):
    # Lightweight fallback encoder that handles common types used in the app.
    if isinstance(o, datetime):
        return o.isoformat()
    if isinstance(o, Decimal):
        return float(o)
    # Let json.dumps fall back to string representation
    return str(o)


def to_jsonable(obj):
    # If it's a Pydantic model use model_dump_json for correct serialization
    if isinstance(obj, BaseModel):
        # model_dump_json returns a JSON string
        return json.loads(obj.model_dump_json())
    return json.loads(json.dumps(obj, default=_default_encoder))