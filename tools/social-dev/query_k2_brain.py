#!/usr/bin/env python3
"""Query the staged K2 brain acceptance chains without importing source code."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
QUERY_PATH = ROOT / "knowledge/brain/acceptance/query-results.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", help="query id, or 'all'", default="all")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    if not QUERY_PATH.exists():
        raise SystemExit("K2 query results are not built yet")
    payload = json.loads(QUERY_PATH.read_text(encoding="utf-8"))
    if args.query != "all":
        query = payload.get("queries", {}).get(args.query)
        if query is None:
            raise SystemExit(f"unknown K2 query: {args.query}")
        result = {"query_id": args.query, **query}
    else:
        result = payload
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
