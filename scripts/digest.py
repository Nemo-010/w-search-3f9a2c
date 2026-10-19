#!/usr/bin/env python3
"""Build per-provider fact digests from fetched snapshots.

For every provider, scan the plain-text snapshots for pricing/free-tier
sentences, rank them, and write data/digest/<slug>.txt. Also writes
data/fetch_summary.json with one record per provider and source.

Usage: python3 scripts/digest.py
"""
import glob
import json
import os
import re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
SNAP = os.path.join(DATA, "snapshots")
DIG = os.path.join(DATA, "digest")

STRONG = re.compile(
    r"(free tier|free plan|free trial|free credits?|free of charge|for free|no credit card|"
    r"starts? free|start for free|free forever|free usage|free quota|free requests?|"
    r"monthly (credits?|quota|allowance|requests?|searches|calls|pages)|per month|/month|"
    r"\bcredits?\b|\btrial\b|\bsignup\b|sign[- ]up|newsletter|verify|verified|"
    r"monthly|annually|billing|subscription|pay[- ]as[- ]you[- ]go|pricing|plans?|"
    r"rate limits?|requests? per|tokens? per|\bquota\b|\ballowance\b|\bbonus\b)", re.I)
MONEY = re.compile(r"(\$|€|£)\s?\d|\d+\s?(usd|eur|gbp)|per 1,?000|per 1k|per call|per request", re.I)
NUM = re.compile(r"\b\d[\d,.]*\b")
BAD = re.compile(r"(cookie|privacy policy|terms of service|all rights reserved|subscribe to our|"
                 r"javascript|enable js|skip to content|accept all|manage preferences)", re.I)


def rank(line: str) -> int:
    s = 0
    if MONEY.search(line):
        s += 4
    if re.search(r"\bfree\b", line, re.I):
        s += 3
    if re.search(r"\b(credits?|quota|allowance|tokens?)\b", line, re.I):
        s += 2
    if re.search(r"\b(month|day|week)\b", line, re.I):
        s += 1
    if NUM.search(line):
        s += 1
    if len(line) > 360 or len(line) < 12:
        s -= 5
    if BAD.search(line):
        s -= 6
    return s


def lines_of(path):
    try:
        with open(path, errors="replace") as f:
            return f.read().split("\n")
    except Exception:
        return []


def main():
    os.makedirs(DIG, exist_ok=True)
    summary = []
    for meta_path in sorted(glob.glob(os.path.join(SNAP, "*", "meta.json"))):
        slug = os.path.basename(os.path.dirname(meta_path))
        meta = json.load(open(meta_path))
        cand = {p["slug"]: p for p in json.load(open(os.path.join(DATA, "candidates.json")))["providers"]}
        p = cand.get(slug, {})
        out = []
        out.append(f"# {p.get('name', slug)} ({slug}) category={p.get('category')}")
        out.append(f"home={p.get('home')} pricing={p.get('pricing')} docs={p.get('docs')} llms={p.get('llms')}")
        if "github" in meta:
            g = meta["github"]
            out.append(f"github stars={g['stargazers_count']} forks={g['forks_count']} created={g['created_at'][:10]} pushed={g['pushed_at'][:10]} archived={g['archived']} desc={g.get('description')}")
        srcs = []
        for name, s in meta["sources"].items():
            if s.get("status") != 200:
                continue
            kind = name.split("-err-")[0]
            srcs.append((kind, name, s.get("url")))
        out.append("sources_ok: " + ", ".join(f"{k}:{u}" for k, n, u in srcs))
        seen = set()
        all_ranked = []
        for kind, name, url in srcs:
            txt_path = os.path.join(SNAP, slug, name.split("-err-")[0] + ".txt")
            if not os.path.exists(txt_path):
                txt_path = os.path.join(SNAP, slug, kind + ".txt")
            ls = lines_of(txt_path)
            for i, line in enumerate(ls):
                line = line.strip()
                if not line or len(line) < 12:
                    continue
                s = rank(line)
                if s >= 3 and line not in seen:
                    seen.add(line)
                    all_ranked.append((s, kind, line))
        all_ranked.sort(key=lambda x: -x[0])
        # keep a spread: top 50 by score, plus first lines of llms
        out.append("--- ranked fact lines ---")
        for s, kind, line in all_ranked[:50]:
            out.append(f"[{kind}] {line[:400]}")
        # head of llms.txt for context
        for lp in (os.path.join(SNAP, slug, "llms.txt"), os.path.join(SNAP, slug, "readme.txt")):
            if os.path.exists(lp):
                head = [l.strip() for l in lines_of(lp)[:25] if l.strip()]
                out.append("--- llms/readme head ---")
                out.extend(head[:18])
                break
        with open(os.path.join(DIG, slug + ".txt"), "w") as f:
            f.write("\n".join(out) + "\n")
        codes = Counter(v.get("status") for v in meta["sources"].values())
        summary.append({
            "slug": slug, "name": p.get("name"), "category": p.get("category"),
            "home": p.get("home"), "pricing": p.get("pricing"), "docs": p.get("docs"), "llms": p.get("llms"),
            "ok_sources": sum(1 for v in meta["sources"].values() if v.get("status") == 200),
            "llms_ok": any(k.split("-err-")[0].startswith("llms") and v.get("status") == 200 for k, v in meta["sources"].items()),
            "github": meta.get("github"),
            "status_codes": dict(codes),
        })
    with open(os.path.join(DATA, "fetch_summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print("digests:", len(summary), "-> data/digest/")


if __name__ == "__main__":
    main()
