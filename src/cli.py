import argparse
import sys
from datetime import datetime
from pathlib import Path

from .parser import parse_line
from .filters import filter_stream
from .aggregator import aggregate
from .writer import write_terminal, write_json, write_csv


def parse_dt(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def main(argv=None):
    p = argparse.ArgumentParser(description="Анализатор журналов событий")
    p.add_argument("--input", required=True, help="Путь к файлу лога")
    p.add_argument("--from", dest="from_dt", help="Начало интервала (ISO 8601, включительно)")
    p.add_argument("--to", dest="to_dt", help="Конец интервала (ISO 8601, исключительно)")
    p.add_argument("--level", help="Уровень: TRACE/DEBUG/INFO/WARN/ERROR")
    p.add_argument("--source", help="Источник события")
    p.add_argument("--top", type=int, default=5, help="Top-N кодов ошибок (по умолч. 5)")
    p.add_argument("--format", choices=["json", "csv"], default="json", help="Формат отчёта")
    p.add_argument("--output", help="Путь к файлу отчёта")
    args = p.parse_args(argv)

    path = Path(args.input)
    if not path.exists():
        print(f"Файл не найден: {path}", file=sys.stderr)
        return 1
    if path.stat().st_size == 0:
        print(f"Файл пуст: {path}", file=sys.stderr)
        return 0

    from_dt = parse_dt(args.from_dt) if args.from_dt else None
    to_dt = parse_dt(args.to_dt) if args.to_dt else None

    valid = 0
    invalid = 0
    errors = []
    records = []

    def gen():
        nonlocal valid, invalid
        with path.open("r", encoding="utf-8") as f:
            for i, line in enumerate(f, start=1):
                rec = parse_line(line, i)
                if "error" in rec:
                    invalid += 1
                    errors.append(rec)
                else:
                    valid += 1
                    yield rec

    filtered = filter_stream(gen(), from_dt, to_dt, args.level, args.source)
    summary = aggregate(filtered, top_n=args.top)

    write_terminal(summary, valid, invalid, errors)

    if args.output:
        out = Path(args.output)
        if args.format == "json":
            payload = {**summary, "valid": valid, "invalid": invalid, "errors": errors[:20]}
            write_json(str(out), payload)
        else:
            write_csv(str(out), summary)
        print(f"\nОтчёт сохранён: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())