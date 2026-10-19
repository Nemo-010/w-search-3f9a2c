# New York Times API

- Category: `news` — News APIs
- Home: https://developer.nytimes.com/
- Pricing: https://developer.nytimes.com/pricing
- Docs: https://developer.nytimes.com/docs/
- llms.txt: none usable — empty body
- First Wayback capture of domain: 20080912 (developer.nytimes.com)

## Free tier

- Documented recurring free volume: **500**
- Detail: Free API key per API: 500 requests/day and 5 requests/minute (per API, so several APIs multiply the daily budget)
- Confidence: **high**

## Evidence

> Yes, there are two rate limits per API: 500 requests per day and 5 requests per minute. You should sleep 12 seconds between calls to avoid hitting the per minute rate limit.

Source: https://developer.nytimes.com/faq  
Snapshot: `data/snapshots/nyt/faq.txt`  

## Measurement note

`data/facts.json` entry for `nyt`; fetched 2026-10-19. Free tiers change — re-run `make fetch fresh` to re-verify.
