#!/usr/bin/env python3
"""Fetch first Wayback Machine capture per provider domain (maturity proxy).

Writes data/maturity.json: slug -> {domain, first_seen, http_status}.
"""
import concurrent.futures as cf
import json
import os
import re
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
UA = "w-search-research/0.1 (+https://github.com/Nemo-010/w-search-3f9a2c)"


def first_seen(domain):
    q = urllib.parse.urlencode({
        "url": domain, "output": "json", "limit": "1", "fl": "timestamp,statuscode",
        "from": "2004", "collapse": "digest",
    })
    url = f"https://web.archive.org/cdx/search/cdx?{q}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
        if len(d) > 1:
            return {"domain": domain, "first_seen": d[1][0][:8], "http_status": d[1][1]}
    except Exception as e:  # noqa: BLE001
        return {"domain": domain, "error": str(e)[:80]}
    return {"domain": domain, "first_seen": None}


def domain_of(url):
    if not url:
        return None
    m = re.match(r"https?://([^/]+)", url)
    if not m:
        return None
    d = m.group(1).lower()
    for pre in ("www.", "docs.", "api.", "help.", "platform.", "console.", "developers."):
        if d.startswith(pre):
            d = d[len(pre):]
    return d


def main():
    cands = json.load(open(os.path.join(DATA, "candidates.json")))["providers"]
    out = {}
    tasks = {}
    with cf.ThreadPoolExecutor(8) as ex:
        for p in cands:
            d = domain_of(p.get("home"))
            if not d or d in ("github.com",):
                continue
            tasks[ex.submit(first_seen, d)] = (p["slug"], d)
        for f in cf.as_completed(tasks):
            slug, d = tasks[f]
            try:
                out[slug] = f.result()
            except Exception as e:  # noqa: BLE001
                out[slug] = {"domain": d, "error": str(e)[:80]}
            time.sleep(0.02)
    json.dump(out, open(os.path.join(DATA, "maturity.json"), "w"), indent=1)
    print("maturity records:", len(out))


if __name__ == "__main__":
    main()
