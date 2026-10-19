#!/usr/bin/env python3
"""Verify recorded sources: re-fetch and compare SHA-256 against meta.json.

Non-destructive. Exit code 1 if a source that was 200 is now unreachable, else 0.
Changed content is reported but does not fail the run (free tiers change).

Usage: python3 scripts/check.py [--llms-only] [--slug S]... [--limit N]
"""
import argparse
import concurrent.futures as cf
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch import fetch, SNAP  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--llms-only", action="store_true")
    ap.add_argument("--slug", action="append", default=[])
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    metas = sorted(glob.glob(os.path.join(SNAP, "*", "meta.json")))
    if a.slug:
        metas = [m for m in metas if os.path.basename(os.path.dirname(m)) in a.slug]
    jobs = []
    for mp in metas:
        meta = json.load(open(mp))
        for kind, s in meta["sources"].items():
            if s.get("status") != 200:
                continue
            if a.llms_only and not kind.startswith("llms"):
                continue
            jobs.append((meta["slug"], kind, s))
    if a.limit:
        jobs = jobs[: a.limit]

    changed = same = dead = 0
    with cf.ThreadPoolExecutor(16) as ex:
        futs = {ex.submit(fetch, s["url"]): (slug, kind, s) for slug, kind, s in jobs}
        for f in cf.as_completed(futs):
            slug, kind, old = futs[f]
            try:
                new = f.result()
            except Exception as e:  # noqa: BLE001
                dead += 1
                print(f"DEAD  {slug}/{kind} {old['url']}: {e}")
                continue
            new.pop("raw", None)
            if new["status"] != 200:
                dead += 1
                print(f"DEAD  {slug}/{kind} {old['url']} -> HTTP {new['status']}")
            elif new["sha256"] == old["sha256"]:
                same += 1
            else:
                changed += 1
                print(f"CHANGED {slug}/{kind} {old['url']} (re-fetch {new['fetched_at']})")
    print(f"\nchecked={len(jobs)} unchanged={same} changed={changed} dead={dead}")
    sys.exit(1 if dead else 0)


if __name__ == "__main__":
    main()
