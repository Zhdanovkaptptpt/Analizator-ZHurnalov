from datetime import datetime
from src.filters import matches_filters


def make_rec(ts_iso, level="INFO", source="svc", code="E1"):
    return {
        "timestamp": datetime.fromisoformat(ts_iso.replace("Z", "+00:00")),
        "level": level, "source": source, "event_code": code, "message": "", "line_number": 1,
    }


def test_from_inclusive_to_exclusive():
    r = make_rec("2026-09-01T10:00:00Z")
    f = datetime.fromisoformat("2026-09-01T10:00:00+00:00")
    t = datetime.fromisoformat("2026-09-01T11:00:00+00:00")
    assert matches_filters(r, f, t, None, None) is True


def test_to_exclusive_boundary():
    r = make_rec("2026-09-01T11:00:00Z")
    t = datetime.fromisoformat("2026-09-01T11:00:00+00:00")
    assert matches_filters(r, None, t, None, None) is False


def test_level_filter():
    r = make_rec("2026-09-01T10:00:00Z", level="ERROR")
    assert matches_filters(r, None, None, "error", None) is True
    assert matches_filters(r, None, None, "INFO", None) is False


def test_source_filter():
    r = make_rec("2026-09-01T10:00:00Z", source="gateway")
    assert matches_filters(r, None, None, None, "gateway") is True
    assert matches_filters(r, None, None, None, "other") is False