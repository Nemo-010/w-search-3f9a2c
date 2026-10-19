# StackExchange API

- Category: `misc-api` — General free web/reference APIs
- Home: https://api.stackexchange.com/
- Pricing: —
- Docs: https://api.stackexchange.com/docs
- llms.txt: none usable — HTTP 400
- First Wayback capture of domain: 20040324 (stackexchange.com)

## Free tier

- Documented recurring free volume: **300,000**
- Detail: Free: 300 requests/day per IP without key; 10,000/day per user/app pair with a free key
- Card required for free tier: no
- Signup extras: free app key raises quota
- Confidence: **high**

## Evidence

> If an application does have an access_token, then the application is on a distinct user/app pair daily quota (default size of 10,000).

Source: https://api.stackexchange.com/docs/throttle  
Snapshot: `data/snapshots/stackexchange/throttle.txt`  

## Measurement note

`data/facts.json` entry for `stackexchange`; fetched 2026-10-19. Free tiers change — re-run `make fetch fresh` to re-verify.
