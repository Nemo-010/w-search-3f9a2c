# w-search — free web search / fetch / crawl provider inventory

Compiled 2026-10-19. Every claim is tied to a snapshot in `data/snapshots/`.

## What this is

- `reports/01-top-100.md` — 198 providers, ranked: documented recurring monthly free volume first, one-time grants second, unquantified free tiers last.
- `reports/02-deep-reviews-1.md` — deep reviews: Tavily, Exa, Firecrawl.
- `reports/03-post-analysis.md` — 5-account totals, measured hit rates vs vendor claims, one-time vs monthly, maturity, signup bonuses.
- `reports/04-deep-reviews-2.md` — deep reviews: Jina, Brave, SERP scrapers, LLM-native grounding, self-hosted stacks.
- `providers/<slug>.md` — one report per provider with links, free-tier facts, evidence quote and snapshot path.

## Method

1. Candidate list: 198 providers across AI-search, SERP/scrape, browser automation, search engines, readers, archives, news, academic and general free APIs (`data/candidates.json`).
2. Public pages fetched: home, pricing, docs and `llms.txt`/`llms-full.txt` where published (683 successful fetches, 134 providers ship an llms.txt). Raw bytes are gzipped in `data/snapshots/<slug>/` with SHA-256, HTTP status and final URL in `meta.json`.
3. Facts: `data/facts.json`, one entry per provider; each quantified number carries the verbatim quote and source URL. Confidence: `high` = explicit official number, `medium` = official statement without a number, `low` = not present in fetched pages, `none` = no free tier found.
4. Maturity: first Wayback capture per domain (`data/maturity.json`) and GitHub stars for OSS entries.
5. Hit rates: treg Web Arena leaderboard snapshot (30-day live routing data) in `data/snapshots/treg/leaderboard.json`.

## Re-verify

```sh
make fetch        # re-download every provider page (refreshes snapshots)
make digest       # rebuild per-provider fact digests
make reports      # rebuild all reports from data/facts.json
make check        # verify every source URL still resolves and hashes match
```

`make fetch fresh` wipes snapshots first. Verification is non-destructive: `make check` only reports.

## Limits

- Free tiers change without notice; numbers are as of the fetch date in each snapshot.
- Where a provider publishes prices in JS-rendered tables only, the number may be marked `low`/`none` even if a plan exists.
- Credit-to-call conversions use the provider's own rate card; they are noted per row.
- No terms-of-service analysis is included; this is a technical inventory.

License: 0BSD (see `LICENSE`).
