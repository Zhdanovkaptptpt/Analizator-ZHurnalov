from datetime import datetime
from typing import Optional, Dict, Any

VALID_LEVELS = {"TRACE", "DEBUG", "INFO", "WARN", "ERROR"}


def parse_line(line: str, line_number: int) -> Dict[str, Any]:
    """Парсит строку лога. Возвращает dict или None при ошибке."""
    line = line.rstrip("\n")
    if not line.strip():
        return {"error": "empty line", "line_number": line_number, "raw": line}

    parts = line.split("|")
    if len(parts) != 5:
        return {"error": "wrong field count", "line_number": line_number, "raw": line}

    ts_str, level, source, event_code, message = [p.strip() for p in parts]

    # timestamp
    try:
        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except ValueError:
        return {"error": "invalid timestamp", "line_number": line_number, "raw": line}

    level_up = level.upper()
    if level_up not in VALID_LEVELS:
        return {"error": "invalid level", "line_number": line_number, "raw": line}

    if not source or not event_code:
        return {"error": "empty field", "line_number": line_number, "raw": line}

    return {
        "timestamp": ts,
        "level": level_up,
        "source": source,
        "event_code": event_code,
        "message": message,
        "line_number": line_number,
    }