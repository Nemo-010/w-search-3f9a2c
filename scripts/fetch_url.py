#!/usr/bin/env python3
"""Fetch one extra URL into a provider's snapshot dir (with meta update).

Usage: python3 scripts/fetch_url.py <slug> <kind> <url> [via]
"""
import gzip
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch import fetch, to_text, SNAP  # noqa: E402


def main():
    slug, kind, url = sys.argv[1], sys.argv[2], sys.argv[3]
    via = sys.argv[4] if len(sys.argv) > 4 else None
    d = os.path.join(SNAP, slug)
    os.makedirs(d, exist_ok=True)
    res = fetch(url)
    raw = res.pop("raw")
    if res["status"] == 200:
        with gzip.open(os.path.join(d, kind + ".gz"), "wb", compresslevel=9) as f:
            f.write(raw)
        txt = to_text(raw, res["content_type"])
        with open(os.path.join(d, kind + ".txt"), "w") as f:
            f.write(txt)
        res["text_bytes"] = len(txt)
        if via:
            res["via"] = via
    meta_path = os.path.join(d, "meta.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {"slug": slug, "sources": {}}
    meta["sources"][kind] = res
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=1)
    print(slug, kind, res["status"], res.get("bytes"), res.get("final_url"))


if __name__ == "__main__":
    main()
