#!/usr/bin/env python3
"""Fetch public documentation pages for every candidate provider.

Snapshots are stored gzip-compressed under data/snapshots/<slug>/ as
<kind>.gz plus a plain-text rendering <kind>.txt (HTML stripped) for
grepping. Every fetch is recorded in meta.json with URL, HTTP status,
final URL, byte size, sha256 and fetch time.

Usage: python3 scripts/fetch.py [slug ...]
"""
import concurrent.futures as cf
import datetime
import gzip
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
SNAP = os.path.join(DATA, "snapshots")
UA = ("w-search-research/0.1 (public documentation inventory; "
      "+https://github.com/Nemo-010/w-search-3f9a2c)")
MAX_BYTES = 3_000_000
TIMEOUT = 25
WORKERS = 16

TAG_RE = re.compile(r"<(script|style|svg|noscript)\b.*?</\1>", re.S | re.I)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
ANY_TAG = re.compile(r"<[^>]+>")


def to_text(raw: bytes, ctype: str) -> str:
    if "html" in ctype or raw[:200].lstrip().lower().startswith((b"<!doctype", b"<html")):
        s = raw.decode("utf-8", "replace")
        s = COMMENT_RE.sub(" ", s)
        s = TAG_RE.sub(" ", s)
        s = ANY_TAG.sub(" ", s)
        s = html.unescape(s)
        s = re.sub(r"[ \t\r\f\v]+", " ", s)
        s = re.sub(r"\n\s*\n+", "\n", s)
        return s.strip()
    return raw.decode("utf-8", "replace")


def fetch(url: str) -> dict:
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,text/plain,application/json,*/*",
        "Accept-Language": "en",
    })
    started = datetime.datetime.now(datetime.timezone.utc)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            raw = r.read(MAX_BYTES + 1)
            status = r.status
            ctype = r.headers.get("Content-Type", "")
            final = r.geturl()
    except urllib.error.HTTPError as e:
        try:
            raw = e.read(MAX_BYTES)
        except Exception:
            raw = b""
        status = e.code
        ctype = e.headers.get("Content-Type", "") if e.headers else ""
        final = url
    except Exception as e:  # noqa: BLE001
        status = 0
        ctype = ""
        final = url
        raw = str(e).encode()
    truncated = len(raw) > MAX_BYTES
    raw = raw[:MAX_BYTES]
    return {"url": url, "status": status, "final_url": final, "content_type": ctype,
            "bytes": len(raw), "truncated": truncated,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "fetched_at": started.isoformat(timespec="seconds"),
            "raw": raw}


def save(slug: str, kind: str, res: dict) -> dict:
    d = os.path.join(SNAP, slug)
    os.makedirs(d, exist_ok=True)
    with gzip.open(os.path.join(d, kind + ".gz"), "wb", compresslevel=9) as f:
        f.write(res.pop("raw"))
    txt = to_text(gzip.open(os.path.join(d, kind + ".gz"), "rb").read(), res["content_type"])
    with open(os.path.join(d, kind + ".txt"), "w") as f:
        f.write(txt)
    res["text_bytes"] = len(txt)
    return res


def github_urls(url: str):
    m = re.match(r"https?://github\.com/([^/]+)/([^/#?]+)", url)
    if not m:
        return None
    owner, repo = m.group(1), m.group(2)
    return owner, repo


def github_meta(owner: str, repo: str) -> dict | None:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{owner}/{repo}",
        headers={"User-Agent": UA, "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            d = json.load(r)
        return {k: d.get(k) for k in ("full_name", "stargazers_count", "forks_count",
                                      "created_at", "pushed_at", "license", "archived",
                                      "open_issues_count", "subscribers_count", "description")}
    except Exception:
        return None


def work(p: dict) -> str:
    slug = p["slug"]
    attempts = []
    meta_path = os.path.join(SNAP, slug, "meta.json")
    meta = {"slug": slug, "name": p["name"], "category": p["category"],
            "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "sources": {}}

    jobs = []
    if p.get("llms"):
        jobs.append(("llms", p["llms"]))
    if p.get("pricing"):
        jobs.append(("pricing", p["pricing"]))
    if p.get("docs"):
        jobs.append(("docs", p["docs"]))
    if p.get("home"):
        jobs.append(("home", p["home"]))

    gh = github_urls(p.get("home") or "")
    if gh:
        owner, repo = gh
        jobs = [j for j in jobs if j[0] != "home"]
        jobs.insert(0, ("readme", f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/README.md"))
        gm = github_meta(owner, repo)
        if gm:
            meta["github"] = gm

    # llms.txt probe locations when none configured
    probes = []
    if not p.get("llms"):
        hosts = []
        for u in (p.get("docs"), p.get("home")):
            if u:
                hosts.append(u.rstrip("/"))
        if p.get("docs"):
            probes.append(("llms", p["docs"].rstrip("/") + "/llms.txt"))
        if p.get("home"):
            probes.append(("llms", p["home"].rstrip("/") + "/llms.txt"))
            probes.append(("llms", p["home"].rstrip("/") + "/docs/llms.txt"))
        for u in hosts:
            m = re.match(r"https?://([^/]+)", u)
            if m and not m.group(1).startswith(("www.", "docs.", "api.")):
                probes.append(("llms", f"https://docs.{m.group(1)}/llms.txt"))

    seen_urls = set()
    for kind, url in jobs + probes:
        if url in seen_urls:
            continue
        seen_urls.add(url)
        res = fetch(url)
        if res["status"] == 200:
            meta["sources"][kind if kind not in meta["sources"] else f"{kind}-{res['url']}"] = save(slug, kind, res)
        else:
            res.pop("raw")
            meta["sources"][kind + "-err-" + hashlib.sha1(url.encode()).hexdigest()[:6]] = res
        if kind == "llms" and res.get("status") == 200:
            full = url.replace("llms.txt", "llms-full.txt")
            r2 = fetch(full)
            if r2["status"] == 200:
                meta["sources"]["llms-full"] = save(slug, "llms-full", r2)
            else:
                r2.pop("raw")
        time.sleep(0.05)

    os.makedirs(os.path.dirname(meta_path), exist_ok=True)
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=1)
    ok = sum(1 for v in meta["sources"].values() if v.get("status") == 200)
    return f"{slug:22s} ok={ok:2d} / {len(meta['sources'])}"


def main():
    with open(os.path.join(DATA, "candidates.json")) as f:
        doc = json.load(f)
    provs = doc["providers"]
    want = set(sys.argv[1:])
    if want:
        provs = [p for p in provs if p["slug"] in want]
    os.makedirs(SNAP, exist_ok=True)
    t0 = time.time()
    with cf.ThreadPoolExecutor(WORKERS) as ex:
        futs = {ex.submit(work, p): p["slug"] for p in provs}
        for f in cf.as_completed(futs):
            try:
                print(f.result(), flush=True)
            except Exception as e:  # noqa: BLE001
                print(f"FAIL {futs[f]}: {e}", flush=True)
    print(f"done in {time.time()-t0:.0f}s, {len(provs)} providers")


if __name__ == "__main__":
    main()
