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


RETRIES = 3


def first_seen(domain):
    """First CDX capture for a domain.

    Distinguishes three outcomes, because they are not the same claim:
      first_seen set  -> the archive has a capture, with its timestamp
      first_seen None -> the archive answered and has no capture
      error set       -> the lookup failed; nothing can be said about the domain
    A failed lookup must never be recorded as "no capture".
    """
    q = urllib.parse.urlencode({
        "url": domain, "output": "json", "limit": "1", "fl": "timestamp,statuscode",
        "from": "2004", "collapse": "digest",
    })
    url = f"https://web.archive.org/cdx/search/cdx?{q}"
    last = None
    for attempt in range(RETRIES):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.load(r)
            if len(d) > 1:
                return {"domain": domain, "first_seen": d[1][0][:8], "http_status": d[1][1]}
            return {"domain": domain, "first_seen": None, "captured": False}
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5 * (attempt + 1))
    return {"domain": domain, "error": str(last)[:120]}


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


PATH_OUT = os.path.join(DATA, "maturity.json")


def main():
    """Resumable: keeps successful lookups, retries the ones that errored.

    The CDX endpoint refuses connections under sustained load, so this runs with
    low concurrency and a delay, and re-running it only re-attempts failures.
    """
    cands = json.load(open(os.path.join(DATA, "candidates.json")))["providers"]
    out = json.load(open(PATH_OUT)) if os.path.exists(PATH_OUT) else {}
    todo = []
    for p in cands:
        d = domain_of(p.get("home"))
        if not d or d == "github.com":
            continue
        prev = out.get(p["slug"]) or {}
        if prev.get("first_seen") or (prev.get("first_seen") is None and "error" not in prev):
            continue
        todo.append((p["slug"], d))
    print("records kept:", len(out) - len(todo), "to retry:", len(todo), flush=True)
    for slug, d in todo:
        out[slug] = first_seen(d)
        status = out[slug].get("first_seen") or ("no capture" if "error" not in out[slug] else "ERROR")
        print(f"  {slug:22s} {d:32s} {status}", flush=True)
        json.dump(out, open(PATH_OUT, "w"), indent=1)
        time.sleep(4.0)
    json.dump(out, open(PATH_OUT, "w"), indent=1)
    got = sum(1 for v in out.values() if v.get("first_seen"))
    err = sum(1 for v in out.values() if v.get("error"))
    print(f"maturity records: {len(out)} with capture: {got} unresolved: {err}")


if __name__ == "__main__":
    main()
