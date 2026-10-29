import json
import csv
from typing import Dict, Any


def write_terminal(summary: Dict[str, Any], valid: int, invalid: int, errors: list):
    print(f"=== Отчёт ===")
    print(f"Корректных строк : {valid}")
    print(f"Ошибочных строк  : {invalid}")
    print(f"Событий после фильтра: {summary['matched']}")
    print("\nПо уровням:", summary["by_level"])
    print("По источникам:", summary["by_source"])
    print("\nTop-N ошибок:")
    for e in summary["top_errors"]:
        print(f"  {e['code']}: {e['count']}")
    if errors:
        print(f"\nПримеры ошибочных строк (первые 5):")
        for e in errors[:5]:
            print(f"  строка {e['line_number']}: {e['error']} — {e['raw'][:80]}")


def write_json(path: str, data: Dict[str, Any]):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def write_csv(path: str, summary: Dict[str, Any]):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["section", "key", "value"])
        w.writerow(["summary", "matched", summary["matched"]])
        for k, v in summary["by_level"].items():
            w.writerow(["by_level", k, v])
        for k, v in summary["by_source"].items():
            w.writerow(["by_source", k, v])
        for e in summary["top_errors"]:
            w.writerow(["top_error", e["code"], e["count"]])