from collections import Counter
from typing import Iterable, Dict, Any, List, Tuple


def aggregate(records: Iterable[Dict[str, Any]], top_n: int = 5) -> Dict[str, Any]:
    level_counts: Counter = Counter()
    source_counts: Counter = Counter()
    error_codes: Counter = Counter()
    matched = 0

    for r in records:
        matched += 1
        level_counts[r["level"]] += 1
        source_counts[r["source"]] += 1
        if r["level"] == "ERROR":
            error_codes[r["event_code"]] += 1

    top_errors: List[Tuple[str, int]] = error_codes.most_common(top_n)

    return {
        "matched": matched,
        "by_level": dict(level_counts),
        "by_source": dict(source_counts),
        "top_errors": [{"code": c, "count": n} for c, n in top_errors],
    }