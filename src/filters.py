cat > ~/log_analyzer/src/filters.py << 'EOF'
from datetime import datetime, timezone
from typing import Iterable, Dict, Any, Optional


def matches_filters(
    record: Dict[str, Any],
    from_dt: Optional[datetime],
    to_dt: Optional[datetime],
    level: Optional[str],
    source: Optional[str],
) -> bool:
    ts = record["timestamp"]
    
    # Приводим к одному типу (оба timezone-aware или оба naive)
    if from_dt is not None:
        if ts.tzinfo is None and from_dt.tzinfo is not None:
            # ts naive, from_dt aware - делаем ts aware
            ts = ts.replace(tzinfo=timezone.utc)
        elif ts.tzinfo is not None and from_dt.tzinfo is None:
            # ts aware, from_dt naive - делаем from_dt naive
            from_dt = from_dt.replace(tzinfo=None)
    
    if to_dt is not None:
        if ts.tzinfo is None and to_dt.tzinfo is not None:
            ts = ts.replace(tzinfo=timezone.utc)
        elif ts.tzinfo is not None and to_dt.tzinfo is None:
            to_dt = to_dt.replace(tzinfo=None)
    
    if from_dt and ts < from_dt:
        return False
    if to_dt and ts >= to_dt:
        return False
    if level and record["level"] != level.upper():
        return False
    if source and record["source"] != source:
        return False
    return True


def filter_stream(
    records: Iterable[Dict[str, Any]],
    from_dt: Optional[datetime],
    to_dt: Optional[datetime],
    level: Optional[str],
    source: Optional[str],
):
    for r in records:
        if matches_filters(r, from_dt, to_dt, level, source):
            yield r
EOF