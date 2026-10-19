#!/usr/bin/env python3
"""Integrity tests for the generated reports and the fact table.

Every cited path must resolve and every evidence quote must appear verbatim in
the snapshot it points at. The generated reports must not cite a snapshot that
is absent from the repository.

Run: python3 scripts/test_integrity.py -v
"""
import json
import os
import re
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
REP = os.path.join(ROOT, "reports")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def facts():
    with open(os.path.join(DATA, "facts.json")) as f:
        return json.load(f)


class TestEvidence(unittest.TestCase):
    def test_every_evidence_snapshot_exists(self):
        missing = []
        for r in facts():
            for e in r.get("evidence") or []:
                sp = e.get("snapshot") or ""
                if sp and not os.path.exists(os.path.join(ROOT, sp)):
                    missing.append(f"{r['slug']} -> {sp}")
        self.assertEqual([], missing, "evidence points at absent snapshots")

    def test_every_quote_is_verbatim_in_its_snapshot(self):
        bad = []
        for r in facts():
            for e in r.get("evidence") or []:
                q, sp = (e.get("quote") or "").strip(), e.get("snapshot") or ""
                if not q or not sp:
                    continue
                path = os.path.join(ROOT, sp)
                if not os.path.exists(path):
                    continue
                txt = norm(open(path, encoding="utf-8", errors="replace").read())
                # "..." joins fragments that are quoted from separate places
                frags = [f for f in re.split(r"\s*(?:\.\.\.|…)\s*", q) if f.strip()]
                for frag in frags:
                    if norm(frag) not in txt:
                        bad.append(f"{r['slug']}: {frag[:60]!r} not in {sp}")
                        break
        self.assertEqual([], bad, "evidence quotes not present in their snapshot")

    def test_bonus_claims_appear_in_the_providers_own_snapshots(self):
        """A signup bonus is a factual claim about a provider's offer, so the words
        must be in a page captured from that provider."""
        bad = []
        for r in facts():
            if not r.get("bonus"):
                continue
            d = os.path.join(ROOT, "data", "snapshots", r["slug"])
            if not os.path.isdir(d):
                bad.append(f"{r['slug']}: no snapshot dir for bonus {r['bonus']}")
                continue
            body = " ".join(
                open(os.path.join(d, f), encoding="utf-8", errors="replace").read()
                for f in sorted(os.listdir(d)) if f.endswith(".txt"))
            body = body.lower()
            for claim in r["bonus"]:
                words = [w for w in re.findall(r"[A-Za-z]{5,}", claim)]
                hits = [w for w in words if w.lower() in body]
                # require that the distinctive words of the claim are present
                if words and len(hits) < max(1, len(set(w.lower() for w in words)) // 2):
                    bad.append(f"{r['slug']}: {claim!r} not found in snapshots")
        self.assertEqual([], bad, "bonus claims not supported by a captured page")

    def test_quantified_facts_cite_an_evidence_url(self):
        bad = [r["slug"] for r in facts()
               if r["monthly_calls"] and not any(e.get("url") for e in r.get("evidence") or [])]
        self.assertEqual([], bad)


class TestLeaderboard(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(DATA, "snapshots", "treg", "leaderboard.txt")
        self.gz = os.path.join(DATA, "snapshots", "treg", "leaderboard.gz")

    def test_leaderboard_snapshot_present(self):
        self.assertTrue(os.path.exists(self.path) or os.path.exists(self.gz),
                        "treg leaderboard snapshot missing; post-analysis section 2 cites it")

    def test_leaderboard_parses_and_has_tasks(self):
        import gzip
        if os.path.exists(self.path):
            raw = open(self.path, "rb").read()
        else:
            raw = gzip.open(self.gz, "rb").read()
        d = json.loads(raw)
        self.assertIn("task_results", d)
        self.assertGreaterEqual(len(d["task_results"]), 5)
        self.assertTrue(d.get("updated_at"))


class TestReports(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pa = open(os.path.join(REP, "02-post-analysis.md"), encoding="utf-8").read()
        cls.top = open(os.path.join(REP, "01-top-100.md"), encoding="utf-8").read()

    def test_post_analysis_has_measured_hit_rates(self):
        section = self.pa.split("## 2. Best results")[1].split("## 3.")[0]
        self.assertIn("| Task | Provider | Success rate |", section)
        rows = [l for l in section.splitlines() if l.startswith("| ") and "%" in l]
        self.assertGreaterEqual(len(rows), 20, "measured hit-rate table is empty or short")

    def test_post_analysis_does_not_cite_absent_leaderboard_json(self):
        self.assertNotIn("leaderboard.json", self.pa)

    def test_every_cited_report_path_resolves(self):
        bad = []
        for f in ("01-top-100.md", "02-post-analysis.md"):
            txt = open(os.path.join(REP, f), encoding="utf-8").read()
            for rel in re.findall(r"\((providers/[^)]+\.md)\)", txt):
                if not os.path.exists(os.path.join(REP, rel)):
                    bad.append(f"{f} -> {rel}")
        self.assertEqual([], bad)

    def test_provider_files_cover_every_fact(self):
        slugs = {r["slug"] for r in facts()}
        on_disk = {f[:-3] for f in os.listdir(os.path.join(ROOT, "providers")) if f.endswith(".md")}
        self.assertEqual(set(), slugs - on_disk)

    def test_deep_reviews_exist_and_cite_snapshots(self):
        path = os.path.join(REP, "03-deep-reviews.md")
        self.assertTrue(os.path.exists(path), "reports/03-deep-reviews.md missing")
        txt = open(path, encoding="utf-8").read()
        cited = re.findall(r"`(data/snapshots/[^`]+)`", txt)
        self.assertGreaterEqual(len(cited), 8, "deep reviews cite too few snapshots")
        missing = [c for c in cited if not os.path.exists(os.path.join(ROOT, c))]
        self.assertEqual([], missing, "deep reviews cite absent snapshots")

    def test_deep_reviews_cover_the_requested_providers(self):
        txt = open(os.path.join(REP, "03-deep-reviews.md"), encoding="utf-8").read()
        for n in range(1, 9):
            self.assertIn(f"## {n}. ", txt, f"deep review {n} missing")

    def test_deep_review_quotes_match_their_snapshot(self):
        """Every blockquote in the deep reviews must be verbatim in the cited snapshot."""
        txt = open(os.path.join(REP, "03-deep-reviews.md"), encoding="utf-8").read()
        bad = []
        # a review quote is a "> text" line followed by "> — url (`snapshot`)"
        lines = txt.splitlines()
        for i, line in enumerate(lines):
            if not line.startswith("> ") or line.startswith("> —"):
                continue
            quote = line[2:].strip()
            if not quote:
                continue
            att = next((l for l in lines[i + 1:i + 4] if l.startswith("> —")), None)
            if not att or "`data/snapshots/" not in att:
                bad.append(f"unattributed quote: {quote[:50]!r}")
                continue
            snap = "data/snapshots/" + att.split("`data/snapshots/", 1)[1].split("`", 1)[0]
            path = os.path.join(ROOT, snap)
            if not os.path.exists(path):
                bad.append(f"{snap}: absent")
                continue
            body = norm(open(path, encoding="utf-8", errors="replace").read())
            if norm(quote) not in body:
                bad.append(f"{snap}: {quote[:50]!r}")
        self.assertEqual([], bad)

    def test_reports_are_reproducible(self):
        names = ("01-top-100.md", "02-post-analysis.md", "03-deep-reviews.md")

        def snap():
            out = {}
            for f in names:
                with open(os.path.join(REP, f), "rb") as fh:
                    out[f] = fh.read()
            return out

        before = snap()
        for script in ("build_reports.py", "build_reviews.py"):
            subprocess.run([sys.executable, os.path.join(ROOT, "scripts", script)],
                           cwd=ROOT, check=True, capture_output=True)
        after = snap()
        for f in before:
            self.assertEqual(before[f], after[f], f"{f} is not reproducible from data/")


if __name__ == "__main__":
    unittest.main()
