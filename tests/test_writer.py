import json
import csv
from pathlib import Path
from src.writer import write_json, write_csv


def test_write_json(tmp_path):
    p = tmp_path / "out.json"
    data = {"matched": 1, "by_level": {"ERROR": 1}, "by_source": {}, "top_errors": []}
    write_json(str(p), data)
    assert json.loads(p.read_text())["matched"] == 1


def test_write_csv(tmp_path):
    p = tmp_path / "out.csv"
    data = {"matched": 2, "by_level": {"ERROR": 2}, "by_source": {"gw": 2}, "top_errors": []}
    write_csv(str(p), data)
    rows = list(csv.reader(p.open()))
    assert rows[0] == ["section", "key", "value"]
    assert len(rows) >= 4