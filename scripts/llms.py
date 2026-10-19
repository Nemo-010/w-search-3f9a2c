#!/usr/bin/env python3
"""Recompute llms.txt availability from the snapshots, honestly.

fetch.py records llms_ok=True whenever a probe returned HTTP 200. That counts
three kinds of non-answer as success:

  * an HTML page served at a *.txt path (a 200 soft-404 or a site shell)
  * an empty body
  * a file belonging to a different site (the probe falls back to
    docs.<host>/llms.txt, and for github-hosted projects that is GitHub's own
    docs file, not the project's)

This script rewrites data/llms.json with one record per provider:
    url      the URL that actually served the file, or null
    bytes    size of the served body
    reason   why it was accepted or rejected

and prints the corrected count. build_reports.py reads data/llms.json for the
links it prints, so the inventory stops advertising files that do not exist.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
SNAP = os.path.join(DATA, "snapshots")

HTML_START = ("<!doctype", "<html", "<head", "<?xml")


def registrable(host):
    host = host.lower()
    for pre in ("www.", "docs.", "help.", "api.", "api-docs.", "developers.", "platform.",
                "console.", "developer."):
        if host.startswith(pre):
            host = host[len(pre):]
            break
    return host


def host_of(url):
    m = re.match(r"https?://([^/]+)", url or "")
    return m.group(1).lower() if m else ""


def judge(slug, entry, home_host):
    url = entry.get("url") or ""
    if entry.get("status") != 200:
        return None, None, f"HTTP {entry.get('status')}"
    path = os.path.join(SNAP, slug, "llms.txt")
    body = b""
    if os.path.exists(path):
        body = open(path, "rb").read()
    if not body:
        return None, 0, "empty body"
    text = body[:400].decode("utf-8", "replace").lstrip().lower()
    if text.startswith(HTML_START):
        return None, len(body), "served HTML at a .txt path"
    if home_host and registrable(host_of(url)) != registrable(home_host):
        served = registrable(host_of(url))
        # a project may legitimately publish on its own product domain; GitHub's
        # docs file is never the project's, so that one is always rejected
        if served in ("github.com",):
            return None, len(body), f"belongs to {served}, not the provider"
        if registrable(served) not in body[:2000].decode("utf-8", "replace").lower():
            return None, len(body), f"belongs to {served}, not the provider"
    # a real llms.txt is a markdown index: it has headings or a blockquote near the top
    head = body[:1500].decode("utf-8", "replace")
    if not re.search(r"^#{1,3} |^> ", head, re.M):
        return None, len(body), "not a markdown index (no heading or summary)"
    return url, len(body), "ok"


def main():
    cands = {p["slug"]: p for p in json.load(open(os.path.join(DATA, "candidates.json")))["providers"]}
    out = {}
    for slug in sorted(cands):
        mp = os.path.join(SNAP, slug, "meta.json")
        if not os.path.exists(mp):
            continue
        meta = json.load(open(mp))
        home = host_of(cands[slug].get("home") or "")
        best = None
        for kind, entry in sorted(meta.get("sources", {}).items()):
            if not kind.startswith("llms"):
                continue
            url, size, reason = judge(slug, entry, home)
            if url:
                best = {"url": url, "bytes": size, "reason": reason}
                break
            if best is None:
                best = {"url": None, "bytes": size or 0, "reason": reason}
        if best is None:
            best = {"url": None, "bytes": 0, "reason": "no llms.txt probed"}
        out[slug] = best

    with open(os.path.join(DATA, "llms.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    ok = [s for s, v in out.items() if v["url"]]
    print(f"llms.json written: {len(ok)} providers with a real llms.txt "
          f"out of {len(out)} probed")
    rejected = [(s, v["reason"]) for s, v in out.items() if not v["url"]]
    print("rejected:", len(rejected))
    for s, r in rejected[:8]:
        print(f"  {s:22s} {r}")


if __name__ == "__main__":
    main()
