#!/usr/bin/env python3
"""Generate the report set from data/facts.json, data/maturity.json and the
treg leaderboard snapshot.

Outputs:
  reports/01-top-100.md          ranked free-tier inventory
  reports/02-post-analysis.md    five post-analysis sections
  providers/<slug>.md            one report per provider (198)
  README.md
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
REP = os.path.join(ROOT, "reports")
PROV = os.path.join(ROOT, "providers")
TODAY = "2026-10-19"

facts = json.load(open(os.path.join(DATA, "facts.json")))
mat = json.load(open(os.path.join(DATA, "maturity.json")))
LEADERBOARD = os.path.join(DATA, "snapshots", "treg", "leaderboard.txt")
leader = json.load(open(LEADERBOARD)) if os.path.exists(LEADERBOARD) else None
if leader is None:
    raise SystemExit("missing %s: section 2 of the post-analysis needs the treg leaderboard "
                     "snapshot. Run scripts/fetch_url.py treg leaderboard "
                     "https://treg.to/web-arena/api/leaderboard" % LEADERBOARD)

CATS = {"ai-search": "AI search / web access APIs", "serp-scrape": "SERP + scrape/crawl APIs",
        "browser": "Browser automation clouds", "search-engine": "Search engines / metasearch",
        "reader": "Reader, markdown & metadata APIs", "archive": "Archives & discovery",
        "news": "News APIs", "academic": "Academic / research APIs",
        "misc-api": "General free web/reference APIs", "llm-search": "LLM-native web search",
        "oss": "Open-source stacks (self-host)", "marketplace": "Marketplaces"}


def fmt(n):
    return f"{n:,}" if isinstance(n, int) else "—"


def pct(r):
    return f"{r['monthly_calls']:,}" if r["monthly_calls"] else "—"


def prov_md(r):
    L = []
    L.append(f"# {r['name']}")
    L.append("")
    L.append(f"- Category: `{r['category']}` — {CATS.get(r['category'], '')}")
    L.append(f"- Home: {r['home'] or '—'}")
    L.append(f"- Pricing: {r['pricing'] or '—'}")
    L.append(f"- Docs: {r['docs'] or '—'}")
    if r["llms"]:
        L.append(f"- llms.txt: {r['llms']}")
    elif r.get("llms_reject"):
        L.append(f"- llms.txt: none usable — {r['llms_reject']}")
    else:
        L.append("- llms.txt: none found at the probed locations")
    if r.get("github"):
        g = r["github"]
        L.append(f"- GitHub: {g['full_name']} — ★{g['stargazers_count']}, created {g['created_at'][:10]}, last push {g['pushed_at'][:10]}, license {g['license']['spdx_id'] if g.get('license') else 'n/a'}")
    if r["slug"] in mat and mat[r["slug"]].get("first_seen"):
        L.append(f"- First Wayback capture of domain: {mat[r['slug']]['first_seen']} ({mat[r['slug']]['domain']})")
    L.append("")
    L.append("## Free tier")
    L.append("")
    L.append(f"- Documented recurring free volume: **{pct(r)}**" if r["monthly_calls"] else "- Documented recurring free volume: not quantified in fetched sources")
    if r.get("monthly_note"):
        L.append(f"- Detail: {r['monthly_note']}")
    if r.get("one_time"):
        L.append(f"- One-time grant: {r['one_time']}")
    if r.get("card") is True:
        L.append("- Card required for free tier: yes")
    elif r.get("card") is False:
        L.append("- Card required for free tier: no")
    if r.get("bonus"):
        L.append("- Signup extras: " + "; ".join(r["bonus"]))
    L.append(f"- Confidence: **{r['confidence']}**")
    L.append("")
    if r.get("evidence"):
        L.append("## Evidence")
        L.append("")
        for e in r["evidence"]:
            if e.get("quote"):
                L.append("> " + e["quote"].strip())
                L.append("")
            if e.get("url"):
                L.append(f"Source: {e['url']}  ")
            if e.get("snapshot"):
                L.append(f"Snapshot: `{e['snapshot']}`  ")
            L.append("")
    L.append("## Measurement note")
    L.append("")
    L.append(f"`data/facts.json` entry for `{r['slug']}`; fetched {TODAY}. Free tiers change — re-run `make fetch fresh` to re-verify.")
    return "\n".join(L) + "\n"


def rank_key(r):
    return -(r["monthly_calls"] or 0)


# ---------------- top 100 ----------------
def build_top100():
    with_numbers = [r for r in facts if r["monthly_calls"] and r.get("verified", True)]
    with_numbers.sort(key=rank_key)
    unverified = [r for r in facts if r["monthly_calls"] and not r.get("verified", True)]
    unverified.sort(key=rank_key)
    # tier 2: documented one-time grants, ordered by confidence then name
    one_time = [r for r in facts if r["monthly_calls"] is None and r["one_time"] and r["confidence"] != "none"]
    one_time.sort(key=lambda r: ({"high": 0, "medium": 1, "low": 2}[r["confidence"]], r["name"]))
    # tier 3: documented free tier, no number; then unmetered free APIs
    no_number = [r for r in facts if r["monthly_calls"] is None and not r["one_time"]
                 and r["confidence"] in ("high", "medium")]
    no_number.sort(key=lambda r: ({"high": 0, "medium": 1}.get(r["confidence"], 2), r["name"]))
    ranked = with_numbers + unverified + one_time + no_number
    ranked = ranked[:100]

    L = ["# Top 100 web fetch / search / crawl providers by free-tier allowance", ""]
    L.append(f"Compiled {TODAY}. Scope: providers usable by an agent gateway for web **search**, "
             "page **fetch/extract** or **crawl**. Ranking is by documented *recurring monthly free "
             "call-equivalent* (searches / requests / pages / credits where the provider documents "
             "1 credit = 1 basic call). Providers with only one-time credits or a free tier without "
             "a published number are ranked below the quantified ones and marked accordingly. "
             "Every number links to the snapshot it came from.")
    L.append("")
    L.append("Columns: **Free/mo** = documented recurring free volume; **Basis** = unit and "
             "conversion; **One-time** = first-month credits; **Card** = card demanded for the "
             "free tier; **Conf** = evidence confidence (high = explicit number in official docs).")
    L.append("")
    L.append("| # | Provider | Category | Free/mo | Basis | One-time | Card | Conf | Links |")
    L.append("|---|----------|----------|--------:|-------|----------|:----:|:----:|-------|")
    for i, r in enumerate(ranked, 1):
        basis = ""
        if r["monthly_calls"] and not r.get("verified", True):
            basis = "REPORTED, NOT RE-VERIFIED — " + r["monthly_note"].split(";")[0][:64]
        elif r["monthly_calls"]:
            basis = r["monthly_note"].split(";")[0][:90]
        elif r["one_time"]:
            basis = "one-time grant only"
        else:
            basis = "free tier, volume not published"
        card = {True: "yes", False: "no", None: "?"}.get(r["card"], "?")
        links = " · ".join(x for x in [
            f"[home]({r['home']})" if r["home"] else "",
            f"[pricing]({r['pricing']})" if r["pricing"] else "",
            f"[llms]({r['llms']})" if r["llms"] else "",
            f"[report](../providers/{r['slug']}.md)"] if x)
        L.append(f"| {i} | **{r['name']}** | {r['category']} | {pct(r)} | {basis} | "
                 f"{r['one_time'] or '—'} | {card} | {r['confidence']} | {links} |")
    L.append("")
    L.append(f"Ranked entries: {len(ranked)}. Remaining {len(facts)-len(ranked)} providers are in the "
             "full inventory below (no free tier documented in the fetched sources).")
    L.append("")

    for cat, label in CATS.items():
        rows = [r for r in facts if r["category"] == cat]
        if not rows:
            continue
        L.append(f"## {label}")
        L.append("")
        for r in rows:
            L.append(f"### {r['name']}")
            L.append("")
            line = f"- Free: {r['monthly_note'] or 'no free tier documented in fetched sources'}"
            if r["one_time"]:
                line += f" — one-time: {r['one_time']}"
            L.append(line)
            L.append(f"- Links: home {r['home'] or '—'} · pricing {r['pricing'] or '—'} · llms.txt {r['llms'] or '—'}")
            L.append(f"- Confidence: {r['confidence']} · [full report](../providers/{r['slug']}.md)")
            L.append("")
    open(os.path.join(REP, "01-top-100.md"), "w").write("\n".join(L))
    return ranked


def build_post_analysis(ranked):
    L = ["# Post-analysis", ""]
    L.append(f"All figures derive from `data/facts.json` (fetched {TODAY}). "
             "Nothing here is an estimate unless the row says so.")
    L.append("")

    # 1. five accounts
    L.append("## 1. Total volume with 5 accounts per provider")
    L.append("")
    L.append("Method: documented recurring monthly free volume × 5. One-time grants are kept "
             "separate and are not mixed into the recurring total. Providers whose free tier is a "
             "rate limit with no published monthly cap are excluded from the sum (their row says so).")
    L.append("")
    total = 0
    L.append("| Provider | Per account /mo | ×5 | Basis |")
    L.append("|----------|---:|---:|-------|")
    for r in sorted([x for x in facts if x["monthly_calls"] and x.get("verified", True)], key=rank_key):
        total += r["monthly_calls"] * 5
        L.append(f"| {r['name']} | {fmt(r['monthly_calls'])} | **{fmt(r['monthly_calls']*5)}** | {r['monthly_note'].split(';')[0][:80]} |")
    L.append(f"| **Total** | | **{fmt(total)}** | |")
    L.append("")
    L.append(f"Documented recurring free volume across all re-verified providers, 5 accounts each: "
             f"**{fmt(total)} calls/month**. The largest single contributors: "
             + ", ".join(f"{r['name']} {fmt(r['monthly_calls']*5)}" for r in sorted(
                 [x for x in facts if x["monthly_calls"] and x.get("verified", True)], key=rank_key)[:6]) + ".")
    L.append("")
    # the sum is a call count, not a page-fetch count: say what the big rows are
    L.append("**Read the total as calls, not as pages.** It adds allowances that are not "
             "interchangeable: a DOI lookup, a news search, a weather reading and a rendered page all "
             "count as one call here. The two largest rows are the clearest cases:")
    L.append("")
    for slug in ("unpaywall", "naver"):
        r = next((x for x in facts if x["slug"] == slug), None)
        if r and r["monthly_calls"] and r.get("verified", True):
            L.append(f"- {r['name']} ({fmt(r['monthly_calls']*5)}/month at 5 accounts) — "
                     f"{r['monthly_note']}")
    L.append("")
    web_only = [x for x in facts if x["monthly_calls"] and x.get("verified", True)
                and x["category"] in ("ai-search", "serp-scrape", "browser", "search-engine", "reader")]
    L.append("Restricting the sum to categories that actually fetch or search the open web "
             f"(`ai-search`, `serp-scrape`, `browser`, `search-engine`, `reader`) gives "
             f"**{fmt(sum(x['monthly_calls'] * 5 for x in web_only))} calls/month** across "
             f"{len(web_only)} providers. That is the number to plan a web gateway against; the "
             "larger total above is only meaningful as a ceiling.")
    L.append("")
    unver = [r for r in facts if r["monthly_calls"] and not r.get("verified", True)]
    if unver:
        L.append("Reported but not re-verified in this snapshot run (excluded from the total above):")
        L.append("")
        for r in sorted(unver, key=rank_key):
            L.append(f"- {r['name']}: {fmt(r['monthly_calls'])}/month reported — {r['monthly_note']} "
                     f"(`{r['slug']}`, confidence {r['confidence']})")
        L.append("")
    ot = [r for r in facts if r["one_time"]]
    L.append("One-time, first-month totals (not recurring, ×5 accounts where the grant is per account):")
    L.append("")
    for r in sorted(ot, key=lambda x: x["name"]):
        L.append(f"- {r['name']}: {r['one_time']}")
    L.append("")
    L.append("Providers with a documented free tier but no published monthly cap (excluded from the "
             "sum): " + ", ".join(r["name"] for r in facts
                                  if r["monthly_calls"] is None and not r["one_time"]
                                  and r["confidence"] in ("high", "medium")) + ".")
    zero = [r for r in facts if r["monthly_calls"] == 0]
    L.append("")
    L.append("Providers with **no free tier** documented in this run (excluded): "
             + ", ".join(r["name"] for r in zero) + ".")
    L.append("")

    # 2. best results / bot protection
    L.append("## 2. Best results and hardest bot protection")
    L.append("")
    L.append("Two separate evidence classes, kept apart.")
    L.append("")
    L.append("**Measured (independent).** treg's Web Arena leaderboard aggregates live routed calls "
             "over a 30-day window: per provider, per task, the share of calls that returned a usable "
             "result, plus median provider latency and the catalog price at capture time. Snapshot: "
             "`data/snapshots/treg/leaderboard.txt`, `updated_at` "
             f"`{leader['updated_at']}`, window {leader['window_days']} days, observed since "
             f"`{leader['observed_since'][:10]}`, cached calls and treg refusals excluded, minimum "
             f"{leader['minimum_comparable_runs']} comparable runs and "
             f"{leader['minimum_hit_samples']} hit samples per row.")
    L.append("")
    L.append("`success_rate` is successes over `hit_samples` (the calls where a hit or miss was "
             "recorded); `runs` is every routed run including the ones without a recorded hit, so the "
             "two denominators differ. `ok calls` is `success_rate × hit_samples`, rounded.")
    L.append("")
    L.append("| Task | Provider | Success rate | ok calls | Rate samples | Routed runs | Median ms | Price/call |")
    L.append("|------|----------|---:|---:|---:|---:|---:|---:|")
    for task, rows in leader["task_results"].items():
        for r in rows:
            sr = r.get("success_rate")
            n = r.get("hit_samples") or 0
            price = r.get("current_catalog_price_usd")
            unit = r.get("price_unit") or ""
            ok = f"{round(sr * n / 100):,}" if sr is not None and n else "—"
            L.append(f"| {task} | {r['provider']} | {sr if sr is not None else '—'}% | {ok} | "
                     f"{n:,} | {r.get('runs'):,} | {r.get('median_provider_ms')} | "
                     f"{('$' + format(price, '.6g') + ' / ' + unit) if price is not None else '—'} |")
    L.append("")
    L.append("Read the rate-sample column before the percentage. Rates cover the provider's own answer "
             "on treg's routed workload, not a controlled head-to-head scrape of identical URLs.")
    L.append("")

    # measured leaderboards per task, with the volume caveat made explicit
    L.append("**Who actually returns results, by task.** Derived from the table above.")
    L.append("")
    for task, rows in leader["task_results"].items():
        best = max(rows, key=lambda r: (r.get("success_rate") or 0))
        heaviest = max(rows, key=lambda r: r.get("runs") or 0)
        top = sorted(rows, key=lambda r: -(r.get("success_rate") or 0))[:3]
        L.append(f"- `{task}`: best measured "
                 + ", ".join(f"{r['provider']} {r.get('success_rate')}% (n={r.get('hit_samples'):,})"
                             for r in top)
                 + f". Highest routed volume: {heaviest['provider']} "
                   f"({heaviest.get('runs'):,} runs, {heaviest.get('success_rate')}%).")
    L.append("")

    # bot protection: fetch is the discriminating task
    fetch_rows = leader["task_results"].get("fetch", [])
    if fetch_rows:
        L.append("**Hardest bot protection.** The `fetch` task is the one that exercises anti-bot "
                 "defences: it asks a provider to retrieve a real page, so a challenge page, a 403 or "
                 "an empty body counts as a miss. Measured spread on that task:")
        L.append("")
        L.append("| Provider | Fetch success | ok calls | Rate samples | Routed runs | Median ms |")
        L.append("|----------|---:|---:|---:|---:|---:|")
        for r in fetch_rows:
            n = r.get("hit_samples") or 0
            sr = r.get("success_rate")
            ok = f"{round(sr * n / 100):,}" if sr is not None and n else "—"
            L.append(f"| {r['provider']} | {sr}% | {ok} | {n:,} | {r.get('runs'):,} | "
                     f"{r.get('median_provider_ms')} |")
        L.append("")
        hi = max(fetch_rows, key=lambda r: (r.get("success_rate") or 0))
        lo = min(fetch_rows, key=lambda r: (r.get("success_rate") or 0))
        search_rows = leader["task_results"].get("search", [])
        gap = ""
        for srow in search_rows:
            if srow["provider"] == hi["provider"] and srow.get("success_rate") is not None:
                gap = (f" {hi['provider']} scores {srow.get('success_rate')}% on `search` against "
                       f"{hi.get('success_rate')}% on `fetch`, so a search hit rate says nothing "
                       "about page retrieval.")
        L.append(f"Spread: {hi['provider']} {hi.get('success_rate')}% down to {lo['provider']} "
                 f"{lo.get('success_rate')}%, on {hi.get('hit_samples'):,} and "
                 f"{lo.get('hit_samples'):,} rate samples respectively.{gap}")
        L.append("")
        L.append("What this does and does not show. It shows which provider was the one that returned "
                 "the page when treg routed a fetch to it. It does not isolate the defence that was "
                 "hit (Cloudflare interstitial, DataDome, plain 403, JS-only shell), it does not "
                 "separate a residential from a datacenter egress, and a provider that fails is not "
                 "necessarily blocked — it may simply have timed out or returned an empty body. No "
                 "vendor publishes a per-defence breakdown, so any claim of the form \"provider X "
                 "beats Cloudflare\" is not testable from this data and is not made here.")
        L.append("")

    L.append("**Vendor-claimed (not independently measured here).** Quotes from the providers' own "
             "pages that assert a success or unblocking rate:")
    L.append("")
    claimed = 0
    for r in facts:
        q = (r["evidence"][0]["quote"] if r.get("evidence") else "") or ""
        if re.search(r"\d+(\.\d+)?%\s*(success|of requests)|99\.\d+%", q):
            L.append(f"- {r['name']}: “{q[:200]}” — {r['evidence'][0]['url']}")
            claimed += 1
    if not claimed:
        L.append("- None of the fetched pages in this snapshot states a numeric success rate.")
    L.append("")

    # 3. one-time vs monthly
    L.append("## 3. One-time vs monthly credits")
    L.append("")
    monthly_only = [r for r in facts if r["monthly_calls"] and not r["one_time"]]
    onetime = [r for r in facts if r["one_time"] and r["monthly_calls"] is None]
    both = [r for r in facts if r["one_time"] and r["monthly_calls"]]
    monthly = monthly_only + both
    nofree = [r for r in facts if r["monthly_calls"] == 0]
    silent = [r for r in facts if r["monthly_calls"] is None and not r["one_time"]
              and r["confidence"] in ("high", "medium")]
    unknown = [r for r in facts if r["monthly_calls"] is None and not r["one_time"]
               and r["confidence"] in ("low", "none")]
    parts = len(monthly_only) + len(onetime) + len(both) + len(nofree) + len(silent) + len(unknown)
    assert parts == len(facts), (parts, len(facts))
    L.append("The six buckets below partition all "
             f"{len(facts)} providers, so no row is counted twice or dropped.")
    L.append("")
    L.append(f"- **Recurring monthly free volume documented:** {len(monthly)} providers, "
             f"{len(monthly_only)} of them recurring only.")
    L.append(f"- **Recurring volume plus a one-time bonus:** {len(both)} providers "
             f"({', '.join(r['name'] for r in both) or '—'}).")
    L.append(f"- **One-time grant only, no recurring volume:** {len(onetime)} providers "
             f"({', '.join(r['name'] for r in onetime) or '—'}).")
    L.append(f"- **Free tier documented but no published number:** {len(silent)} providers "
             "(rate-limited or unpriced free access; excluded from every total).")
    L.append(f"- **No free tier, priced only:** {len(nofree)} providers "
             f"({', '.join(r['name'] for r in nofree) or '—'}).")
    L.append(f"- **Nothing usable found in the captured pages:** {len(unknown)} providers.")
    L.append("")
    L.append("Practical reading: a grant that resets monthly is a standing budget; a one-time grant "
             "is a trial with an expiry. Five providers document both. The distinction that matters "
             "for a gateway is not the size of the grant but whether the allowance returns: a "
             "provider with a small monthly reset is usable indefinitely, while a large one-time "
             "grant buys a fixed number of calls and then stops.")
    L.append("")
    if both:
        L.append("| Provider | Recurring /month | One-time grant |")
        L.append("|----------|---:|-------|")
        for r in sorted(both, key=rank_key):
            L.append(f"| {r['name']} | {fmt(r['monthly_calls'])} | {r['one_time']} |")
        L.append("")

    # 4. maturity
    L.append("## 4. Maturity, popularity, market awareness")
    L.append("")
    L.append("Signals used: first Wayback Machine capture of the primary domain (longevity), GitHub "
             "stars where the project is open source (community size), and funding claims made in the "
             "providers' own docs (market awareness; vendor-announced, not audited).")
    L.append("")
    fund = {
        "firecrawl": "$75M Series B (announced on site)",
        "nimble": "$47M Series B (blog)",
        "linkup": "$10M seed led by Gradient (blog)",
        "keenable": "$26M from Accel and Conviction (site)",
    }
    def first_of(slug):
        m = mat.get(slug) or {}
        if m.get("first_seen"):
            return m["first_seen"]
        if "error" in m:
            return "lookup failed"
        return "no capture"

    rows = sorted(facts, key=lambda x: (
        -(int((mat.get(x["slug"]) or {}).get("first_seen") or 0)),
        -(x["github"]["stargazers_count"] if x.get("github") else 0),
        x["name"]))
    L.append("Rows with a first capture, oldest domain first; OSS projects with a star count but no "
             "dated domain follow. `no capture` and `lookup failed` are different claims and are "
             "printed differently: the first means the archive answered and has nothing, the second "
             "means the archive did not answer and nothing is known.")
    L.append("")
    L.append("| Provider | First web capture | GitHub stars | Funding / company signal |")
    L.append("|----------|-------------------|--------------|--------------------------|")
    for r in rows:
        first = first_of(r["slug"])
        stars = f"★{r['github']['stargazers_count']}" if r.get("github") else "—"
        if first in ("no capture", "lookup failed") and stars == "—":
            continue
        L.append(f"| {r['name']} | {first} | {stars} | {fund.get(r['slug'], '—')} |")
    L.append("")
    dated = [r for r in facts if (mat.get(r["slug"]) or {}).get("first_seen")]
    L.append(f"{len(dated)} of {len(facts)} providers have a dated first capture. Oldest domains: "
             + ", ".join(f"{r['name']} {mat[r['slug']]['first_seen'][:4]}" for r in sorted(
                 dated, key=lambda x: mat[x["slug"]]["first_seen"])[:6]) + ". Youngest: "
             + ", ".join(f"{r['name']} {mat[r['slug']]['first_seen'][:4]}" for r in sorted(
                 dated, key=lambda x: mat[x["slug"]]["first_seen"])[-6:]) + ".")
    L.append("")
    L.append("Caveats: a first capture only proves a domain existed at that date, not that the same "
             "company or product was operating it — several of these domains changed hands. A domain "
             "registered recently says nothing about the API's reliability, and stars measure "
             "attention, not uptime. Neither signal is evidence about free-tier terms.")
    L.append("")

    # 5. signup bonuses
    L.append("## 5. Post-signup bonuses")
    L.append("")
    L.append("Documented extras beyond the base free tier (as stated in the fetched pricing/docs pages).")
    L.append("")
    L.append("| Provider | Extra | Source |")
    L.append("|----------|-------|--------|")
    for r in facts:
        if not r.get("bonus"):
            continue
        src = r["evidence"][0]["url"] if r.get("evidence") else (r["home"] or "")
        L.append(f"| {r['name']} | {'; '.join(r['bonus'])} | {src} |")
    L.append("")
    L.append("Common patterns, and what each is actually worth: work-email upgrades (Valyu doubles "
             "the signup grant to $20), payment-method bonuses (Bright Data adds $5 but converts a "
             "no-card free tier into a card-on-file account), startup programmes (Exa up to $1,000; "
             "Linkup up to $5,000, but application-based rather than automatic), agent-payment rails "
             "that need no account at all (x402 on Tavily, Exa and Keenable), and free tiers that "
             "require no card from the start.")
    L.append("")
    L.append("The last group is the one that matters for a gateway that must not stop working: a "
             "keyless path (Tavily keyless Search/Extract, Jina Reader, Firecrawl keyless scrape, "
             "Keenable keyless calls) keeps a fallback alive after every monthly allowance is spent, "
             "at a lower rate and with no account to lose.")
    L.append("")
    open(os.path.join(REP, "02-post-analysis.md"), "w").write("\n".join(L))


def build_readme(ranked):
    L = ["# w-search — free web search / fetch / crawl provider inventory", ""]
    L.append(f"Compiled {TODAY}. Every claim is tied to a snapshot in `data/snapshots/`.")
    L.append("")
    L.append("## What this is")
    L.append("")
    L.append("- `reports/01-top-100.md` — 198 providers, ranked: documented recurring monthly free "
             "volume first, one-time grants second, unquantified free tiers last.")
    L.append("- `reports/02-post-analysis.md` — 5-account totals, measured hit rates vs vendor "
             "claims, one-time vs monthly, maturity, signup bonuses.")
    L.append("- `providers/<slug>.md` — one report per provider with links, free-tier facts, "
             "evidence quote and snapshot path.")
    L.append("")
    L.append("## Method")
    L.append("")
    L.append("1. Candidate list: 198 providers across AI-search, SERP/scrape, browser automation, "
             "search engines, readers, archives, news, academic and general free APIs "
             "(`data/candidates.json`).")
    L.append("2. Public pages fetched: home, pricing, docs and `llms.txt`/`llms-full.txt` where "
             "published (683 successful fetches). An `llms.txt` is counted only when "
             "`scripts/llms.py` verifies the body is a markdown index served by the provider's own "
             "domain: of 198 probes, 99 pass. Probes returning 200 but serving an HTML page, an "
             "empty body, a robots-style rules file, or GitHub's own docs file are rejected, and the "
             "reject reason is recorded per provider in `data/llms.json`. "
             "Raw bytes are gzipped in `data/snapshots/<slug>/` with SHA-256, HTTP status and "
             "final URL in `meta.json`.")
    L.append("3. Facts: `data/facts.json`, one entry per provider; each quantified number carries "
             "the verbatim quote and source URL. Confidence: `high` = explicit official number, "
             "`medium` = official statement without a number, `low` = not present in fetched pages, "
             "`none` = no free tier found.")
    L.append("4. Maturity: first Wayback capture per domain (`data/maturity.json`) and GitHub stars "
             "for OSS entries.")
    L.append("5. Hit rates: treg Web Arena leaderboard snapshot (30-day live routing data) in "
             "`data/snapshots/treg/leaderboard.txt`.")
    L.append("")
    L.append("## Re-verify")
    L.append("")
    L.append("```sh")
    L.append("make fetch        # re-download every provider page (refreshes snapshots)")
    L.append("make digest       # rebuild per-provider fact digests")
    L.append("make llms         # re-verify llms.txt availability from the snapshots")
    L.append("make reports      # rebuild all reports from data/facts.json")
    L.append("make test         # integrity tests: every quote verbatim, every path resolves")
    L.append("make check        # verify every source URL still resolves and hashes match")
    L.append("```")
    L.append("")
    L.append("`make fetch fresh` wipes snapshots first. Verification is non-destructive: `make check` "
             "only reports.")
    L.append("")
    L.append("## Limits")
    L.append("")
    L.append("- Free tiers change without notice; numbers are as of the fetch date in each snapshot.")
    L.append("- Where a provider publishes prices in JS-rendered tables only, the number may be "
             "marked `low`/`none` even if a plan exists.")
    L.append("- Credit-to-call conversions use the provider's own rate card; they are noted per row.")
    L.append("- No terms-of-service analysis is included; this is a technical inventory.")
    L.append("")
    L.append("License: 0BSD (see `LICENSE`).")
    open(os.path.join(ROOT, "README.md"), "w").write("\n".join(L) + "\n")


def main():
    os.makedirs(PROV, exist_ok=True)
    ranked = build_top100()
    build_post_analysis(ranked)
    build_readme(ranked)
    for r in facts:
        open(os.path.join(PROV, r["slug"] + ".md"), "w").write(prov_md(r))
    print("reports written; ranked:", len(ranked), "provider files:", len(facts))


if __name__ == "__main__":
    main()
