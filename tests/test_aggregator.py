from datetime import datetime
from src.aggregator import aggregate


def rec(level, source, code):
    return {"timestamp": datetime.now(), "level": level, "source": source,
            "event_code": code, "message": "", "line_number": 1}


def test_aggregate_basic():
    data = [
        rec("ERROR", "gw", "HTTP_502"),
        rec("ERROR", "gw", "HTTP_502"),
        rec("ERROR", "pay", "TIMEOUT"),
        rec("INFO", "auth", "LOGIN"),
    ]
    s = aggregate(data, top_n=2)
    assert s["matched"] == 4
    assert s["by_level"]["ERROR"] == 3
    assert s["by_source"]["gw"] == 2
    assert s["top_errors"][0]["code"] == "HTTP_502"
    assert len(s["top_errors"]) == 2