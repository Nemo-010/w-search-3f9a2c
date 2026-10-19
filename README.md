# w-search — free web search / fetch / crawl provider inventory

Compiled 2026-10-19. Every claim is tied to a snapshot in `data/snapshots/`.

## What this is

- `reports/01-top-100.md` — 198 providers, ranked: documented recurring monthly free volume first, one-time grants second, unquantified free tiers last.
- `reports/02-post-analysis.md` — 5-account totals, measured hit rates vs vendor claims, one-time vs monthly, maturity, signup bonuses.
- `reports/03-deep-reviews.md` — 8 provider reviews (Tavily, Exa, Firecrawl, Jina, Brave, ZenRows, Bright Data, ScrapingAnt) generated from the same data.
- `providers/<slug>.md` — one report per provider with links, free-tier facts, evidence quote and snapshot path.

## Method

1. Candidate list: 198 providers across AI-search, SERP/scrape, browser automation, search engines, readers, archives, news, academic and general free APIs (`data/candidates.json`).
2. Public pages fetched: home, pricing, docs and `llms.txt`/`llms-full.txt` where published (683 successful fetches). An `llms.txt` is counted only when `scripts/llms.py` verifies the body is a markdown index served by the provider's own domain: of 198 probes, 99 pass. Probes returning 200 but serving an HTML page, an empty body, a robots-style rules file, or GitHub's own docs file are rejected, and the reject reason is recorded per provider in `data/llms.json`. Raw bytes are gzipped in `data/snapshots/<slug>/` with SHA-256, HTTP status and final URL in `meta.json`.
3. Facts: `data/facts.json`, one entry per provider; each quantified number carries the verbatim quote and source URL. Confidence: `high` = explicit official number, `medium` = official statement without a number, `low` = not present in fetched pages, `none` = no free tier found.
4. Maturity: first Wayback capture per domain (`data/maturity.json`) and GitHub stars for OSS entries.
5. Hit rates: treg Web Arena leaderboard snapshot (30-day live routing data) in `data/snapshots/treg/leaderboard.txt`.

## Re-verify

```sh
make fetch        # re-download every provider page (refreshes snapshots)
make digest       # rebuild per-provider fact digests
make llms         # re-verify llms.txt availability from the snapshots
make reports      # rebuild all reports from data/facts.json
make test         # integrity tests: every quote verbatim, every path resolves
make check        # verify every source URL still resolves and hashes match
```

`make fetch fresh` wipes snapshots first. Verification is non-destructive: `make check` only reports.

## Limits

- Free tiers change without notice; numbers are as of the fetch date in each snapshot.
- Where a provider publishes prices in JS-rendered tables only, the number may be marked `low`/`none` even if a plan exists.
- Credit-to-call conversions use the provider's own rate card; they are noted per row.
- No terms-of-service analysis is included; this is a technical inventory.
- An allowance is a documented call count, not a page count: a DOI lookup and a rendered page both count as one call, so the headline total is a ceiling. `reports/02-post-analysis.md` section 1 gives the web-only subtotal as well.
- Measured hit rates come from one third-party router's workload (treg). They say which provider returned the page when it was asked, not which anti-bot system was in the way, and they are not a controlled head-to-head scrape of identical URLs.
- A provider with no number here may still have a free tier: a JS-rendered pricing table, a login wall or a region block can hide it from capture. Absence of a number is not evidence of absence of a free tier.
- This inventory lists what providers document. It makes no claim that any given use of them is permitted by their terms.

License: 0BSD (see `LICENSE`).
