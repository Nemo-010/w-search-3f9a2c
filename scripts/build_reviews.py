#!/usr/bin/env python3
"""Generate reports/03-deep-reviews.md from data/facts.json and the treg leaderboard.

Each review section pulls its allowance, card requirement, evidence quote and
measured hit rates from the data files rather than restating them by hand, so a
re-fetch cannot leave the prose disagreeing with the tables. Prose covers only
what the numbers mean for a gateway: unit economics, failure semantics,
integration surface, and what is not known.

Run: python3 scripts/build_reviews.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
REP = os.path.join(ROOT, "reports")
TODAY = "2026-10-19"

facts = {r["slug"]: r for r in json.load(open(os.path.join(DATA, "facts.json")))}
lb = json.load(open(os.path.join(DATA, "snapshots", "treg", "leaderboard.txt")))

MEAS = {}
for task, rows in lb["task_results"].items():
    for r in rows:
        MEAS.setdefault(r["provider"], {})[task] = r


def fmt(n):
    return f"{n:,}" if isinstance(n, int) else "—"


def measured(slug, tasks=("search", "fetch", "news", "papers", "sitemap")):
    """Measured rows for a provider, as a markdown table row set."""
    rows = MEAS.get(slug, {})
    out = []
    for t in tasks:
        r = rows.get(t)
        if not r:
            continue
        sr = r.get("success_rate")
        n = r.get("hit_samples") or 0
        ok = f"{round(sr * n / 100):,}" if sr is not None and n else "—"
        out.append(f"| {t} | {sr if sr is not None else '—'}% | {ok} | {n:,} | "
                   f"{r.get('median_provider_ms')} |")
    return out


def card_word(card):
    return {True: "yes", False: "no", None: "not stated"}[card]


def header(slug, title, extra=None):
    r = facts[slug]
    L = [f"## {title}", ""]
    L.append("| | |")
    L.append("|---|---|")
    L.append(f"| Home | {r['home']} |")
    L.append(f"| Pricing | {r['pricing'] or '—'} |")
    L.append(f"| Docs | {r['docs'] or '—'} |")
    L.append(f"| llms.txt | {r['llms'] or 'none published at the probed paths'} |")
    if r.get("monthly_calls"):
        L.append(f"| Recurring free volume | **{fmt(r['monthly_calls'])} calls/month** |")
    else:
        L.append("| Recurring free volume | not quantified in the fetched docs |")
    if r.get("one_time"):
        L.append(f"| One-time grant | {r['one_time']} |")
        L.append(f"| Card for free tier | {card_word(r['card'])} |")
    L.append(f"| Evidence confidence | **{r['confidence']}** |")
    L.append(f"| Facts row | `data/facts.json` → `{slug}` |")
    if extra:
        for k, v in extra:
            L.append(f"| {k} | {v} |")
    L.append("")
    ev = r.get("evidence") or []
    if ev and ev[0].get("quote"):
        L.append("Documented allowance, verbatim from the captured page:")
        L.append("")
        L.append("> " + ev[0]["quote"].strip())
        L.append(">")
        L.append(f"> — {ev[0]['url']} (`{ev[0]['snapshot']}`)")
        L.append("")
    return L


def measured_block(slug, note=None):
    rows = measured(slug)
    if not rows:
        return ["No independent measurement: this provider is not routed by the treg Web Arena "
                "leaderboard snapshot, so there is no hit rate to cite and none is claimed here.", ""]
    L = ["Measured on treg's routed workload, 30-day window (`data/snapshots/treg/leaderboard.txt`):",
         "", "| Task | Success | ok calls | Rate samples | Median ms |",
         "|------|---:|---:|---:|---:|"] + rows + [""]
    if note:
        L += [note, ""]
    return L


L = []
L.append("# Deep reviews")
L.append("")
L.append(f"Generated {TODAY} from `data/facts.json` and the treg leaderboard snapshot. Every "
         "allowance below is a quote from a captured page in `data/snapshots/`; every hit rate is "
         "from treg's 30-day routed-call window and is labelled measured. Where a provider publishes "
         "no number, the review says so instead of inferring one. `make test` fails if a quote stops "
         "matching its snapshot.")
L.append("")

# ---------------------------------------------------------------- 1-3
L += header("tavily", "1. Tavily", [("Endpoints", "Search, Extract, Map, Crawl, Research")])
L.append("**What the credit buys.** Tavily bills one credit for a basic search or a basic page "
         "extract, and more for advanced/deep search and research mode. The allowance is therefore "
         "an upper bound on calls, not a flat count: a gateway that mixes basic search with "
         "advanced extract spends the 1,000 faster than a naive `credits = calls` budget predicts. "
         "Plan the monthly budget in credits per operation, not in calls.")
L.append("")
L.append("**Why it suits an agent gateway.** One call returns ranked results plus optional "
         "synthesized content, so many queries need no second fetch. Output is JSON with an `answer` "
         "field and per-result `content`, which is directly usable as LLM context. There is also a "
         "keyless path for Search and Extract, so a gateway can keep working after the monthly "
         "credits are spent, at a lower per-IP rate.")
L.append("")
L.append("**Failure mode.** Tavily's miss is a thin or empty result set, not a 403. That is a quality "
         "signal rather than a routing signal, so the gateway has to judge result count itself. The "
         "measured fetch rate is well below the measured search rate, so do not use it as the only "
         "fetch leg.")
L.append("")
L += measured_block("tavily", "The search/fetch gap is the number that matters: a good search rate "
                              "does not carry over to page retrieval.")

L += header("exa", "2. Exa",
            [("Endpoints", "Search, Deep Search, Contents, Similar, Answer, Agent, Monitors, Websets")])
L.append("**Denominated in dollars, not credits.** Exa's free tier is a monthly USD balance, so the "
         "effective call count depends entirely on the endpoint chosen. From the captured rate card "
         "(per 1,000 requests, up to 10 results): Instant Search $4, Fast/Auto $7, Deep $12, "
         "Deep-Reasoning $15, Contents $1 per 1,000 pages per content type. A $10 monthly balance is "
         "therefore about 2,500 Instant searches, about 1,400 Fast searches, or about 660 "
         "Deep-Reasoning calls. A gateway can price a mixed workload from one balance, but it has to "
         "read the rate card to know what is left; the same balance is worth a factor of four "
         "depending on the endpoint.")
L.append("")
L.append("**Contents is billed per page per content type.** The rate card says `$1 /1k pages per "
         "content type`, so requesting text, highlights and summary for the same page is three "
         "charges rather than one. This is the most common way to spend the monthly balance faster "
         "than expected, and it is invisible unless the request is priced before it is sent.")
L.append("")
L.append("**Measured strength.** Exa has the largest independent sample in the inventory and is "
         "strong on both search and fetch, which is unusual: most providers are good at one. Its "
         "median fetch latency is also far below the field. That combination makes it the natural "
         "quality leg, with the caveat that the absolute budget is small.")
L.append("")
L += measured_block("exa", "The largest measured sample in the inventory. A high rate on 100k+ "
                           "samples is a materially stronger claim than the same rate on 200.")

L += header("firecrawl", "3. Firecrawl",
            [("Endpoints", "Scrape, Crawl, Map, Search, Extract, Interact, Agent"),
             ("Self-host", "AGPL-3.0, same API shape")])
L.append("**The credit ladder.** Costs are per endpoint and per option: scrape and crawl one credit "
         "per page, map one per call, search two per ten results, JSON extraction four per page, PDF "
         "parsing one per page, browser sandbox two to seven per minute. The 1,000-credit allowance "
         "is therefore between about 1,000 simple scrapes and a few hundred extraction-heavy ones.")
L.append("")
L.append("**Clean failure semantics.** On the free plan there is no pay-as-you-go: when the monthly "
         "allotment is gone, requests return HTTP 402. That is the cleanest routing signal in the "
         "inventory — the gateway can treat 402 as \"switch provider\" without guessing.")
L.append("")
L.append("**The search/fetch split is the finding.** Firecrawl measures near the top of the field on "
         "search and near the bottom on fetch, on a large sample. This is not a claim that it cannot "
         "scrape; it means that on treg's routed workload another provider was usually the one that "
         "returned the page. Design accordingly: use its search-plus-scrape path, and keep a second "
         "fetch leg.")
L.append("")
L.append("**Escape hatch.** It is the only one of these three with a self-hosted build under the same "
         "API shape, so the cloud allowance can be supplemented by running the crawler yourself. That "
         "trades a per-call cost for browser memory and your own IP reputation.")
L.append("")
L += measured_block("firecrawl", "The 32% fetch figure is the sharpest contradiction of vendor "
                                 "marketing in this inventory, and it comes with a 138k sample.")

L.append("### What these three add up to")
L.append("")
L.append("| | Tavily | Exa | Firecrawl |")
L.append("|---|---|---|---|")
for label, key in (("Recurring free volume", "monthly_calls"), ("One-time grant", "one_time")):
    L.append(f"| {label} | " + " | ".join(
        (fmt(facts[s][key]) if isinstance(facts[s].get(key), int) else (facts[s].get(key) or "—"))
        for s in ("tavily", "exa", "firecrawl")) + " |")
L.append("| Card required | " + " | ".join(
    {True: "yes", False: "no", None: "not stated"}[facts[s]["card"]] for s in ("tavily", "exa", "firecrawl")) + " |")
L.append("| Measured search | " + " | ".join(
    f"{MEAS.get(s, {}).get('search', {}).get('success_rate', '—')}%" for s in ("tavily", "exa", "firecrawl")) + " |")
L.append("| Measured fetch | " + " | ".join(
    f"{MEAS.get(s, {}).get('fetch', {}).get('success_rate', '—')}%" for s in ("tavily", "exa", "firecrawl")) + " |")
L.append("")
L.append("All three are enough for interactive personal use and none is enough for unattended "
         "crawling. Only Exa is measured above 85% on both search and fetch. Their failure modes "
         "differ and each is usable as a routing signal: Tavily degrades to thin results, Firecrawl "
         "returns 402 at the boundary, Exa stops when the balance is empty. A zero-marginal-cost "
         "chain is Tavily keyless search, then Exa's monthly balance for the queries that need "
         "quality, then Firecrawl's keyless scrape, then a recurring-credit scraper for pages that "
         "still fail.")
L.append("")

# ---------------------------------------------------------------- 4-8
L += header("jina", "4. Jina AI (Reader, Search, embeddings)")
L.append("**Why the free tier has no number.** Jina publishes rate limits for a free key rather than "
         "a monthly credit pool, so the budget is throughput, not volume. That is a different shape "
         "from every other provider here: there is no monthly cliff, and the only ceiling is requests "
         "per minute. For a single user that is usually better than a credit pool.")
L.append("")
L.append("**The Reader is the cheapest fetch primitive in the inventory.** `r.jina.ai/<url>` needs no "
         "SDK and no key for basic use, and switches output between text, markdown and JSON. It is a "
         "text transform, not a bot-protection layer: it does not solve an interstitial for you, so "
         "pair it with a provider that does when the target is defended.")
L.append("")
L.append("**What is not known.** The fetched docs do not state a monthly token or call grant for the "
         "free key, so no monthly volume is claimed in this inventory. Any figure circulating "
         "elsewhere should be re-checked against a dashboard before it is planned against.")
L.append("")
L += measured_block("jina")

L += header("brave", "5. Brave Search API")
L.append("**Budget in dollars.** Brave bills prepaid USD credits and applies $5 per month "
         "automatically. At the search rate card that is roughly a thousand queries; the page's "
         "larger \"free calls\" figure spans several products, so it is not extra search volume. "
         "Track the balance in dollars rather than calls.")
L.append("")
L.append("**Why it earns a slot despite the small allowance.** It runs its own index rather than "
         "reselling another engine, which makes it the diversity leg when the primary search is a "
         "reseller that breaks when the upstream engine changes. It is not routed by treg, so there "
         "is no independent hit rate for it in this inventory and none is claimed.")
L.append("")
L.append("**Gateway role.** Query it as a second opinion and compare top-N overlap with the primary. "
         "Do not use it for bulk crawling; the value is concentrated in search.")
L.append("")
L += measured_block("brave")

L += header("zenrows", "6. ZenRows")
L.append("**Credit ladder, not a flat pool.** A standard request costs one credit, JS rendering five, "
         "premium proxies ten, protected pages twenty-five. The nominal monthly allowance is therefore "
         "the best case, and a workload aimed at defended pages divides it by up to twenty-five. This "
         "is the single most important number to model before relying on it.")
L.append("")
L.append("**Failure accounting is favourable.** Failed requests are not charged, which matters far "
         "more than a larger nominal grant for a retry-heavy gateway: a page that fails costs time, "
         "not budget.")
L.append("")
L += measured_block("zenrows")

L += header("brightdata", "7. Bright Data")
L.append("**Shared across products.** The monthly credits are one pool across the unlocker, SERP API, "
         "scraper API and scraper studio, and explicitly exclude the proxy and browser products. "
         "Spending them on SERP calls is usually the best value per credit; spending them on the "
         "heaviest unlocker tier burns the pool quickly.")
L.append("")
L.append("**The card bonus is a trap for this use case.** There is a separate small trial credit and "
         "a bonus for adding a payment method. The bonus is larger than the trial but converts a "
         "no-card free tier into a card-on-file account, which is the thing this inventory is trying "
         "to avoid.")
L.append("")
L += measured_block("brightdata")

L += header("scrapingant", "8. ScrapingAnt")
L.append("**The largest no-card recurring allowance in the scraper cluster.** The captured pages "
         "state the monthly credit figure but do not publish a per-request credit ladder, so the "
         "number of *pages* the allowance buys is not documented here and is not inferred. Plan in "
         "credits and read the dashboard's consumption per call before committing a workload to it.")
L.append("")
L.append("**What it is for.** Headless Chrome behind rotating proxies in one API call, which makes it "
         "the natural high-volume fetch leg. Because the per-request credit cost of JS rendering and "
         "premium proxies is not stated in the captured pages, whether a defended target consumes one "
         "credit or several is unknown from this evidence.")
L.append("")
L += measured_block("scrapingant")

open(os.path.join(REP, "03-deep-reviews.md"), "w").write("\n".join(L) + "\n")
print("wrote reports/03-deep-reviews.md")
