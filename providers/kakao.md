# Kakao/Daum Search API

- Category: `search-engine` — Search engines / metasearch
- Home: https://developers.kakao.com/docs/latest/en/daum-search/common
- Pricing: https://developers.kakao.com/docs/latest/en/daum-search/common
- Docs: https://developers.kakao.com/docs/latest/en/daum-search/common
- llms.txt: none usable — no response (connection failed or refused)
- First Wayback capture of domain: 20040102 (kakao.com)

## Free tier

- Documented recurring free volume: **900,000**
- Detail: Daum Search: 30,000 calls/day per endpoint (web/video/image/blog/book/cafe each ~30k/day => ~900k/month for the web endpoint); plus an app-wide free quota of 3,000,000 calls/month
- Signup extras: each Daum endpoint (image/blog/book/cafe/video) has its own 30,000/day quota
- Confidence: **high**

## Evidence

> Daum Search 50,000 calls Search web document 30,000 calls Search video 30,000 calls Search image 30,000 calls Search blog 30,000 calls Search book 30,000 calls Search cafe 30,000 calls

Source: https://developers.kakao.com/docs/latest/en/getting-started/quota  
Snapshot: `data/snapshots/kakao/quota-en.txt`  

## Measurement note

`data/facts.json` entry for `kakao`; fetched 2026-10-19. Free tiers change — re-run `make fetch fresh` to re-verify.
