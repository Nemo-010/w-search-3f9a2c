#!/usr/bin/env python3
"""Fetch one URL into a provider's snapshot dir using curl.

Same output layout as fetch_url.py (gzip bytes + text rendering + meta.json
update) for hosts where the Python HTTP client cannot open a socket.

Usage: python3 scripts/fetch_url_curl.py <slug> <kind> <url>
"""
import gzip
import hashlib
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch import to_text, SNAP, UA  # noqa: E402


def main():
    slug, kind, url = sys.argv[1], sys.argv[2], sys.argv[3]
    d = os.path.join(SNAP, slug)
    os.makedirs(d, exist_ok=True)
    hdr = os.path.join(d, kind + ".hdr")
    body = os.path.join(d, kind + ".raw")
    out = subprocess.run(
        ["curl", "-sSL", "-A", UA, "-D", hdr, "-o", body,
         "-w", "%{http_code} %{url_effective}", url],
        capture_output=True, text=True)
    code, _, final = out.stdout.partition(" ")
    raw = open(body, "rb").read() if os.path.exists(body) else b""
    os.remove(body)
    ctype = ""
    for line in open(hdr, encoding="utf-8", errors="replace"):
        if line.lower().startswith("content-type:"):
            ctype = line.split(":", 1)[1].strip()
    os.remove(hdr)
    res = {"url": url, "status": int(code or 0), "final_url": final or url,
           "content_type": ctype, "bytes": len(raw), "truncated": False,
           "sha256": hashlib.sha256(raw).hexdigest(),
           "fetched_at": __import__("datetime").datetime.now(
               __import__("datetime").timezone.utc).isoformat(timespec="seconds")}
    if res["status"] == 200:
        with gzip.open(os.path.join(d, kind + ".gz"), "wb", compresslevel=9) as f:
            f.write(raw)
        txt = to_text(raw, ctype)
        with open(os.path.join(d, kind + ".txt"), "w") as f:
            f.write(txt)
        res["text_bytes"] = len(txt)
    mp = os.path.join(d, "meta.json")
    meta = json.load(open(mp)) if os.path.exists(mp) else {"slug": slug, "sources": {}}
    meta["sources"][kind] = res
    with open(mp, "w") as f:
        json.dump(meta, f, indent=1)
    print(slug, kind, res["status"], res["bytes"], res["final_url"])


if __name__ == "__main__":
    main()
