import pytest
from src.parser import parse_line


def test_valid_line():
    r = parse_line("2026-09-01T00:08:59Z | WARN | auth-api | AUTH_LOGIN_OK | User session created", 1)
    assert r["level"] == "WARN"
    assert r["source"] == "auth-api"
    assert r["event_code"] == "AUTH_LOGIN_OK"


def test_invalid_timestamp():
    r = parse_line("not-a-timestamp | ERROR | orders-api | ORDER_REJECTED | x", 2)
    assert r["error"] == "invalid timestamp"
    assert r["line_number"] == 2


def test_invalid_level():
    r = parse_line("2026-09-02T08:12:00Z | NOTICE | gateway | HTTP_502 | x", 3)
    assert r["error"] == "invalid level"


def test_wrong_field_count():
    r = parse_line("2026-09-05T11:10:00Z | ERROR | payment-worker | PAYMENT_TIMEOUT", 4)
    assert r["error"] == "wrong field count"


def test_empty_field():
    r = parse_line("2026-09-03T09:00:00Z | INFO | auth-api |  | x", 5)
    assert r["error"] == "empty field"


def test_empty_line():
    r = parse_line("\n", 6)
    assert r["error"] == "empty line"