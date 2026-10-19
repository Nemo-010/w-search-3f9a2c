# Post-analysis

All figures derive from `data/facts.json` (fetched 2026-10-19). Nothing here is an estimate unless the row says so.

## 1. Total volume with 5 accounts per provider

Method: documented recurring monthly free volume × 5. One-time grants are kept separate and are not mixed into the recurring total. Providers whose free tier is a rate limit with no published monthly cap are excluded from the sum (their row says so).

| Provider | Per account /mo | ×5 | Basis |
|----------|---:|---:|-------|
| Unpaywall | 3,000,000 | **15,000,000** | Free API: 100,000 calls/day (~3M/month) with an email in the request |
| Naver Search API | 750,000 | **3,750,000** | Naver search API: 25,000 calls/day free (~750k/month) with client ID/secret |
| TinyFish | 360,000 | **1,800,000** | Search free up to 12,000 requests/day (~360k/month) |
| Open-Meteo | 300,000 | **1,500,000** | Free API: 10,000 calls/day non-commercial (~300k/month), no key or signup |
| Keenable | 100,000 | **500,000** | 100,000 requests/month free, resets monthly |
| The Guardian Open Platform | 15,000 | **75,000** | Free tier: up to 1 call/second and 500 calls/day (~15,000/month), non-commercial |
| ScrapingAnt | 10,000 | **50,000** | 10,000 free credits every month, no card |
| CoinGecko | 10,000 | **50,000** | Demo (free) key: 100 calls/min, 10,000 calls/month cap |
| Diffbot | 9,500 | **47,500** | Free plan $0: 9,500 credits/month (2,000 pages + 5,000 KG + 500 NLP + 2,000 web  |
| Currents API | 7,500 | **37,500** | Free developer plan: 250 requests/day, no card |
| Parallel | 5,000 | **25,000** | Up to 5,000 requests/month free |
| Bright Data | 5,000 | **25,000** | 5,000 credits/month (~$7.50) shared across Web Unlocker, SERP API, Web Scraper A |
| ZenRows | 5,000 | **25,000** | 5,000 credits/month recurring, no card |
| Hyperbrowser | 5,000 | **25,000** | Free account: 5,000 credits (enough for ~50 browser hours or 5,000 fetched pages |
| Google Gemini Grounding | 5,000 | **25,000** | Free tier: 5,000 requests/month shared across Gemini 3+ models for Grounding wit |
| Linkup | 4,000 | **20,000** | 'Run 4,000 queries for free' (Standard search at $0.001-0.006/request) |
| Google Programmable Search | 3,000 | **15,000** | 100 free queries/day (~3,000/month) |
| GNews | 3,000 | **15,000** | Free plan: 100 requests/day, 10 articles/request, 12h delay, 30-day archive |
| NewsAPI | 3,000 | **15,000** | Developer plan: 100 requests/day, delayed/non-commercial |
| Exa | 2,500 | **12,500** | $10 credits/month (Search from $4/1k => ~2,500 searches) |
| Brave Search API | 1,000 | **5,000** | $5 free credits every month on the $5/1k-requests Search API (~1,000 requests) |
| Context.dev | 1,000 | **5,000** | 1,000 credits/month refilled monthly on the grant-anchor day |
| Firecrawl | 1,000 | **5,000** | 1,000 credits/month, resets monthly |
| Tavily AI | 1,000 | **5,000** | 1,000 credits/month, resets monthly |
| HasData | 1,000 | **5,000** | Free plan: 1,000 credits every month, no card |
| Scrape.do | 1,000 | **5,000** | Free plan: 1,000 successful API calls per month, full proxies/captcha/JS, no car |
| Airtop | 1,000 | **5,000** | Free plan: 1,000 credits/month, renews monthly |
| Browserless | 1,000 | **5,000** | Free plan: 1k sessions/month, no card |
| Cohere | 1,000 | **5,000** | Trial (free) keys: 1,000 API calls/month, 20 req/min |
| Cloro | 500 | **2,500** | Free plan $0/month: 500 credits/month |
| SerpStack | 100 | **500** | Free plan: 100 searches/month, non-commercial, JSON only |
| ApiFlash | 100 | **500** | 100 screenshots/month free, no card |
| Microlink | 100 | **500** | Free plan: 100 requests/month, no card |
| ScreenshotOne | 100 | **500** | Free: up to 100 screenshots of any URL per month, including rendering HTML and P |
| Mediastack | 100 | **500** | Free plan: 100 requests/month, delayed news, all sources/languages, HTTPS |
| Zenserp | 50 | **250** | 50 free searches/month, no strings attached |
| **Total** | | **23,062,750** | |

Documented recurring free volume across all re-verified providers, 5 accounts each: **23,062,750 calls/month**. The largest single contributors: Unpaywall 15,000,000, Naver Search API 3,750,000, TinyFish 1,800,000, Open-Meteo 1,500,000, Keenable 500,000, The Guardian Open Platform 75,000.

**Read the total as calls, not as pages.** It adds allowances that are not interchangeable: a DOI lookup, a news search, a weather reading and a rendered page all count as one call here. The two largest rows are the clearest cases:

- Unpaywall (15,000,000/month at 5 accounts) — Free API: 100,000 calls/day (~3M/month) with an email in the request
- Naver Search API (3,750,000/month at 5 accounts) — Naver search API: 25,000 calls/day free (~750k/month) with client ID/secret

Restricting the sum to categories that actually fetch or search the open web (`ai-search`, `serp-scrape`, `browser`, `search-engine`, `reader`) gives **6,339,750 calls/month** across 26 providers. That is the number to plan a web gateway against; the larger total above is only meaningful as a ceiling.

Reported but not re-verified in this snapshot run (excluded from the total above):

- Kakao/Daum Search API: 900,000/month reported — Kakao/Daum search API: 30,000 calls/day free (~900k/month) (not re-verified in this snapshot run) (`kakao`, confidence low)
- ipapi.co: 30,000/month reported — Free: 1,000 requests/day (~30k/month), no key, HTTPS on free tier (`ipapi-co`, confidence low)
- StackExchange API: 9,000/month reported — Free: 300 requests/day without key, 10,000/day with a free key (`stackexchange`, confidence medium)
- NewsData.io: 6,000/month reported — Free tier commonly 200 credits/day (~6,000/month); not captured in this snapshot run (`newsdata`, confidence low)
- TheNewsAPI: 3,000/month reported — Free plan (100 requests/day commonly advertised); free plan needs no payment details (`thenewsapi`, confidence medium)
- Google Books API: 3,000/month reported — Free: 1,000 requests/day per project (Google Books API quota; not captured) (`googlebooks`, confidence low)
- ScrapeNinja: 550/month reported — RapidAPI free tier: 50 non-JS requests/month + 500 JS requests/month (`scrapeninja`, confidence medium)
- New York Times API: 500/month reported — Free API keys with per-endpoint daily limits (commonly 500/day); not captured (`nyt`, confidence low)
- SerpWow: 100/month reported — Free trial (100 requests commonly advertised; number not in fetched snapshot) (`serpwow`, confidence low)
- ValueSERP: 100/month reported — Free trial plan (100 searches/month commonly advertised; number not present in fetched snapshot) (`valueserp`, confidence low)

One-time, first-month totals (not recurring, ×5 accounts where the grant is per account):

- Airtop: 30,000 credits one-time signup grant (starts at 31,000)
- Apify: $500 of prepaid usage for the first 6 months, for Actor developers on the Creator plan (not a general signup grant)
- Bright Data: $2 trial credit (7 days) + $5 bonus when payment method added
- Crawlbase: up to 5,000 requests
- DataForSEO: $1 trial credit
- Exa: $10 onboarding bonus credits
- Hyperbrowser: 5,000 credits
- NewsCatcher: free credits at signup (amount not published in fetched docs)
- Notte: $10 credits
- Octen: $5 free balance on registration
- Parallel: signup credit for new accounts
- ScrapeGraphAI: 500 credits one-time
- ScrapeOps: 1,000 requests
- ScraperAPI: 1,000 free API credits (free plan) / 5,000 credits (7-day trial)
- Scrapfly: 1,000 credits
- ScrapingBee: 1,000 credits
- ScrapingDog: 100 free credits (7-day trial)
- Search1API: 100 free credits
- SearchCans: 100 credits
- Serply: 2,500 credits (30-day expiry)
- Skyvern: 5,000 credits
- Steel.dev: $30 credits
- TikHub: $0.05 signup credit (~50 requests)
- Valyu: $10 free credits ($20 with a work email)
- Web Scraper: 7-day trial
- You.com: free credits at signup (amount not published in fetched docs)
- Zyte: $5 credit
- treg: $1.00 free once for new verified accounts/teams

Providers with a documented free tier but no published monthly cap (excluded from the sum): Jina AI, Litescrape, Olostep, Spider, Browserbase, Cloudflare Browser Rendering, Kernel, DuckDuckGo Instant Answer, Marginalia, Mwmbl, Stract, Arquivo.pt, Common Crawl, urlscan.io, Wayback Machine CDX, GDELT, arXiv API, bioRxiv API, CORE, Crossref REST API, DataCite API, DOAJ API, Europe PMC, Figshare API, HAL API, OpenAIRE, OpenAlex, OSF API, PubMed E-utilities, Semantic Scholar, Zenodo API, Bluesky AT Protocol, crt.sh, DBpedia, FRED, GitHub Search API, Hacker News (Algolia), ip-api, iTunes Search API, Mastodon API, Nominatim (OSM), Open Library, RDAP, REST Countries, USPTO, Wikidata SPARQL, Wikimedia REST, World Bank, Mistral, OpenRouter.

Providers with **no free tier** documented in this run (excluded): Perplexity, Bing Web Search API, Urlbox, Anthropic Web Search, DeepSeek, OpenAI Web Search.

## 2. Best results and hardest bot protection

Two separate evidence classes, kept apart.

**Measured (independent).** treg's Web Arena leaderboard aggregates live routed calls over a 30-day window: per provider, per task, the share of calls that returned a usable result, plus median provider latency and the catalog price at capture time. Snapshot: `data/snapshots/treg/leaderboard.txt`, `updated_at` `2026-10-19T07:18:11.566849Z`, window 30 days, observed since `2026-09-23`, cached calls and treg refusals excluded, minimum 20 comparable runs and 20 hit samples per row.

`success_rate` is successes over `hit_samples` (the calls where a hit or miss was recorded); `runs` is every routed run including the ones without a recorded hit, so the two denominators differ. `ok calls` is `success_rate × hit_samples`, rounded.

| Task | Provider | Success rate | ok calls | Rate samples | Routed runs | Median ms | Price/call |
|------|----------|---:|---:|---:|---:|---:|---:|
| search | tinyfish | 86.8% | 447,972 | 516,097 | 568,415 | 1712 | $0 / call |
| search | serper | 89.5% | 482,021 | 538,571 | 539,041 | 1415 | $0.001 / call |
| search | crawl4ai | 84.9% | 126,992 | 149,578 | 158,610 | 1654 | $0.00015 / call |
| search | exa | 98.1% | 102,629 | 104,617 | 125,272 | 1633 | $0.007 / call |
| search | perplexity | 94.1% | 28,649 | 30,445 | 30,570 | 281 | $0.001 / call |
| search | search1api | 51.8% | 7,868 | 15,190 | 15,307 | 4668 | $0.001 / call |
| search | spidercloud | 35.4% | 5,315 | 15,014 | 15,065 | 3591 | $0.001 / call |
| search | keenable | 99.1% | 14,649 | 14,782 | 14,814 | 841 | $0.004 / call |
| search | firecrawl | 99.8% | 9,471 | 9,490 | 9,604 | 687 | $0.01 / call |
| search | branddev | 78.1% | 5,496 | 7,037 | 7,148 | 1258 | $0.002534 / call |
| search | parallel | 45.8% | 805 | 1,757 | 3,075 | 600 | $0.001 / call |
| search | tavily | 87.2% | 2,333 | 2,676 | 2,865 | 2300 | $0.016 / call |
| search | olostep | 97.0% | 2,417 | 2,492 | 2,499 | 1803 | $0.01 / call |
| search | you | 79.2% | 647 | 817 | 834 | 586 | $0.005 / call |
| search | linkup | 94.1% | 658 | 699 | 704 | 1603 | $0.055 / call |
| search | octen | 86.9% | 153 | 176 | 178 | 270 | $0.005 / call |
| search | scrapegraphai | 69.0% | 120 | 174 | 174 | 10466 | $0.16 / result |
| search | diffbot | 32.0% | 32 | 100 | 100 | 162 | $0.001196 / call |
| maps | dataforseo | 100.0% | 333,244 | 333,244 | 345,842 | 5574 | $0.002 / call |
| maps | serpapi | 100.0% | 5,079 | 5,079 | 5,350 | 1005 | $0.015 / call |
| maps | apify | 91.8% | 1,136 | 1,238 | 2,362 | 20086 | $0.009 / result |
| news | serper | 70.7% | 97,032 | 137,244 | 137,244 | 860 | $0.001 / call |
| news | tinyfish | 80.4% | 82,150 | 102,176 | 106,120 | 1298 | $0 / call |
| news | dataforseo | 100.0% | 47,732 | 47,732 | 56,521 | 3955 | $0.002 / call |
| news | anyapi | 85.0% | 23,758 | 27,950 | 28,036 | 948 | $0.00099 / call |
| news | exa | 99.4% | 9,942 | 10,002 | 10,408 | 507 | $0.007 / call |
| news | litescrape | 46.4% | 1,536 | 3,311 | 4,077 | 4927 | $0.00015 / call |
| news | cloro | 15.9% | 263 | 1,657 | 1,657 | 10700 | $0.002 / call |
| news | search1api | 82.9% | 1,090 | 1,315 | 1,320 | 2239 | $0.001 / call |
| news | serpapi | —% | — | 26 | 988 | 3311 | $0.015 / call |
| news | tavily | —% | — | 193 | 419 | 1419 | $0.008 / call |
| youtube | tikhub | 96.3% | 17,634 | 18,312 | 19,242 | 1558 | $0.002 / call |
| youtube | justoneapi | 70.5% | 539 | 764 | 886 | 2414 | $0.01476 / call |
| youtube | serpapi | 100.0% | 721 | 721 | 793 | 2489 | $0.015 / call |
| sitemap | anyapi | 95.8% | 205 | 214 | 221 | 9078 | $0.001 / call |
| sitemap | firecrawl | 100.0% | 155 | 155 | 188 | 7859 | $0.005 / call |
| sitemap | search1api | 91.5% | 75 | 82 | 83 | 3568 | $0.001 / call |
| sitemap | tavily | 78.1% | 25 | 32 | 41 | 2554 | $0.0016 / page |
| sitemap | branddev | —% | — | 7 | 7 | None | $0.002534 / call |
| fetch | crawl4ai | 45.2% | 394,672 | 873,168 | 1,107,727 | 1771 | $0.00015 / page |
| fetch | tinyfish | 81.8% | 294,598 | 360,144 | 513,708 | 2704 | $0 / call |
| fetch | firecrawl | 32.2% | 44,490 | 138,169 | 148,841 | 2085 | $0.005 / page |
| fetch | exa | 89.2% | 102,389 | 114,786 | 117,266 | 87 | $0.001 / page |
| fetch | anyapi | 37.4% | 29,699 | 79,408 | 115,636 | 3578 | $0.0009 / call |
| fetch | olostep | 79.5% | 18,326 | 23,052 | 29,251 | 6073 | $0.002 / call |
| fetch | search1api | 41.7% | 9,182 | 22,018 | 27,390 | 5001 | $0.001 / call |
| fetch | you | 43.3% | 7,339 | 16,950 | 16,960 | 1812 | $0.001 / page |
| fetch | linkup | 100.0% | 6,013 | 6,013 | 14,705 | 1644 | $0.01 / call |
| fetch | branddev | 63.5% | 8,094 | 12,746 | 12,877 | 2282 | $0.002534 / call |
| fetch | tavily | 75.1% | 8,899 | 11,849 | 12,765 | 1204 | $0.0032 / result |
| fetch | parallel | 26.6% | 1,262 | 4,746 | 4,848 | 4194 | $0.001 / page |
| fetch | keenable | 17.8% | 765 | 4,297 | 4,758 | 345 | $0.004 / call |
| fetch | scrapegraphai | 63.3% | 1,244 | 1,965 | 4,339 | 2385 | $0.004 / call |
| fetch | serper | 67.0% | 274 | 409 | 527 | 1180 | $0.01 / call |
| papers | serper | 97.9% | 1,069 | 1,092 | 1,092 | 761 | $0.001 / call |
| papers | exa | 100.0% | 473 | 473 | 497 | 571 | $0.007 / call |
| papers | tinyfish | 98.4% | 424 | 431 | 447 | 947 | $0 / call |

Read the rate-sample column before the percentage. Rates cover the provider's own answer on treg's routed workload, not a controlled head-to-head scrape of identical URLs.

**Who actually returns results, by task.** Derived from the table above.

- `search`: best measured firecrawl 99.8% (n=9,490), keenable 99.1% (n=14,782), exa 98.1% (n=104,617). Highest routed volume: tinyfish (568,415 runs, 86.8%).
- `maps`: best measured dataforseo 100.0% (n=333,244), serpapi 100.0% (n=5,079), apify 91.8% (n=1,238). Highest routed volume: dataforseo (345,842 runs, 100.0%).
- `news`: best measured dataforseo 100.0% (n=47,732), exa 99.4% (n=10,002), anyapi 85.0% (n=27,950). Highest routed volume: serper (137,244 runs, 70.7%).
- `youtube`: best measured serpapi 100.0% (n=721), tikhub 96.3% (n=18,312), justoneapi 70.5% (n=764). Highest routed volume: tikhub (19,242 runs, 96.3%).
- `sitemap`: best measured firecrawl 100.0% (n=155), anyapi 95.8% (n=214), search1api 91.5% (n=82). Highest routed volume: anyapi (221 runs, 95.8%).
- `fetch`: best measured linkup 100.0% (n=6,013), exa 89.2% (n=114,786), tinyfish 81.8% (n=360,144). Highest routed volume: crawl4ai (1,107,727 runs, 45.2%).
- `papers`: best measured exa 100.0% (n=473), tinyfish 98.4% (n=431), serper 97.9% (n=1,092). Highest routed volume: serper (1,092 runs, 97.9%).

**Hardest bot protection.** The `fetch` task is the one that exercises anti-bot defences: it asks a provider to retrieve a real page, so a challenge page, a 403 or an empty body counts as a miss. Measured spread on that task:

| Provider | Fetch success | ok calls | Rate samples | Routed runs | Median ms |
|----------|---:|---:|---:|---:|---:|
| crawl4ai | 45.2% | 394,672 | 873,168 | 1,107,727 | 1771 |
| tinyfish | 81.8% | 294,598 | 360,144 | 513,708 | 2704 |
| firecrawl | 32.2% | 44,490 | 138,169 | 148,841 | 2085 |
| exa | 89.2% | 102,389 | 114,786 | 117,266 | 87 |
| anyapi | 37.4% | 29,699 | 79,408 | 115,636 | 3578 |
| olostep | 79.5% | 18,326 | 23,052 | 29,251 | 6073 |
| search1api | 41.7% | 9,182 | 22,018 | 27,390 | 5001 |
| you | 43.3% | 7,339 | 16,950 | 16,960 | 1812 |
| linkup | 100.0% | 6,013 | 6,013 | 14,705 | 1644 |
| branddev | 63.5% | 8,094 | 12,746 | 12,877 | 2282 |
| tavily | 75.1% | 8,899 | 11,849 | 12,765 | 1204 |
| parallel | 26.6% | 1,262 | 4,746 | 4,848 | 4194 |
| keenable | 17.8% | 765 | 4,297 | 4,758 | 345 |
| scrapegraphai | 63.3% | 1,244 | 1,965 | 4,339 | 2385 |
| serper | 67.0% | 274 | 409 | 527 | 1180 |

Spread: linkup 100.0% down to keenable 17.8%, on 6,013 and 4,297 rate samples respectively. linkup scores 94.1% on `search` against 100.0% on `fetch`, so a search hit rate says nothing about page retrieval.

What this does and does not show. It shows which provider was the one that returned the page when treg routed a fetch to it. It does not isolate the defence that was hit (Cloudflare interstitial, DataDome, plain 403, JS-only shell), it does not separate a residential from a datacenter egress, and a provider that fails is not necessarily blocked — it may simply have timed out or returned an empty body. No vendor publishes a per-defence breakdown, so any claim of the form "provider X beats Cloudflare" is not testable from this data and is not made here.

**Vendor-claimed (not independently measured here).** Quotes from the providers' own pages that assert a success or unblocking rate:

- None of the fetched pages in this snapshot states a numeric success rate.

## 3. One-time vs monthly credits

The six buckets below partition all 198 providers, so no row is counted twice or dropped.

- **Recurring monthly free volume documented:** 46 providers, 41 of them recurring only.
- **Recurring volume plus a one-time bonus:** 5 providers (Exa, Parallel, Bright Data, Airtop, Hyperbrowser).
- **One-time grant only, no recurring volume:** 23 providers (Octen, ScrapeGraphAI, Search1API, TikHub, treg, Valyu, You.com, Apify, Crawlbase, DataForSEO, ScrapeOps, ScraperAPI, Scrapfly, ScrapingBee, ScrapingDog, SearchCans, Serply, Web Scraper, Zyte, Notte, Skyvern, Steel.dev, NewsCatcher).
- **Free tier documented but no published number:** 50 providers (rate-limited or unpriced free access; excluded from every total).
- **No free tier, priced only:** 6 providers (Perplexity, Bing Web Search API, Urlbox, Anthropic Web Search, DeepSeek, OpenAI Web Search).
- **Nothing usable found in the captured pages:** 73 providers.

Practical reading: a grant that resets monthly is a standing budget; a one-time grant is a trial with an expiry. Five providers document both. The distinction that matters for a gateway is not the size of the grant but whether the allowance returns: a provider with a small monthly reset is usable indefinitely, while a large one-time grant buys a fixed number of calls and then stops.

| Provider | Recurring /month | One-time grant |
|----------|---:|-------|
| Parallel | 5,000 | signup credit for new accounts |
| Bright Data | 5,000 | $2 trial credit (7 days) + $5 bonus when payment method added |
| Hyperbrowser | 5,000 | 5,000 credits |
| Exa | 2,500 | $10 onboarding bonus credits |
| Airtop | 1,000 | 30,000 credits one-time signup grant (starts at 31,000) |

## 4. Maturity, popularity, market awareness

Signals used: first Wayback Machine capture of the primary domain (longevity), GitHub stars where the project is open source (community size), and funding claims made in the providers' own docs (market awareness; vendor-announced, not audited).

Rows with a first capture, oldest domain first; OSS projects with a star count but no dated domain follow. `no capture` and `lookup failed` are different claims and are printed differently: the first means the archive answered and has nothing, the second means the archive did not answer and nothing is known.

| Provider | First web capture | GitHub stars | Funding / company signal |
|----------|-------------------|--------------|--------------------------|
| Litescrape | 20261009 | — | — |
| treg | 20260825 | — | — |
| Octen | 20260214 | — | — |
| SearchCans | 20260121 | — | — |
| Keenable | 20251231 | — | $26M from Accel and Conviction (site) |
| Cloro | 20251105 | — | — |
| Just One API | 20250712 | — | — |
| Marginalia | 20241206 | — | — |
| Anchor Browser | 20241128 | — | — |
| Hyperbrowser | 20241121 | — | — |
| Browser Use (OSS) | 20241113 | — | — |
| Bocha AI | 20241011 | — | — |
| Notte | 20240925 | — | — |
| TinyFish | 20240821 | — | — |
| Airtop | 20240811 | — | — |
| Steel.dev | 20240724 | — | — |
| ScrapeCreators | 20240517 | — | — |
| ScrapeGraphAI | 20240509 | — | — |
| Linkup | 20240501 | — | $10M seed led by Gradient (blog) |
| Spider | 20240422 | — | — |
| Firecrawl | 20240413 | — | $75M Series B (announced on site) |
| Search1API | 20240402 | — | — |
| Lightpanda (OSS) | 20240322 | — | — |
| Google Gemini Grounding | 20231213 | — | — |
| LibreY (OSS) | 20230831 | — | — |
| Brand.dev | 20230724 | — | — |
| Olostep | 20230724 | — | — |
| OpenRouter | 20230525 | — | — |
| TikHub | 20230316 | — | — |
| arXiv API | 20221207 | — | — |
| Bluesky AT Protocol | 20221018 | — | — |
| Serper | 20221006 | — | — |
| Crawlee (OSS) | 20220804 | — | — |
| Serpdog | 20220711 | — | — |
| iTunes Search API | 20220513 | — | — |
| URLtoMarkdown | 20220505 | — | — |
| ScreenshotOne | 20220210 | — | — |
| ScrapeNinja | 20220126 | — | — |
| SearXNG (OSS) | 20220103 | — | — |
| AnyAPI | 20211229 | — | — |
| Mwmbl | 20211226 | — | — |
| Serply | 20211221 | — | — |
| Mistral | 20211218 | — | — |
| Perplexity | 20211218 | — | — |
| MiniMax | 20211217 | — | — |
| ScrapeOps | 20211207 | — | — |
| ScrapeOps Proxy | 20211207 | — | — |
| Fiber AI | 20211204 | — | — |
| Moonshot Kimi | 20211202 | — | — |
| Context.dev | 20211129 | — | — |
| Trafilatura (OSS) | 20210510 | — | — |
| NewsData.io | 20210417 | — | — |
| REST Countries | 20210228 | — | — |
| TheNewsAPI | 20210228 | — | — |
| ValueSERP | 20210220 | — | — |
| ZenRows | 20210208 | — | — |
| Right Dao | 20201202 | — | — |
| Scrapfly | 20201104 | — | — |
| Scrape.do | 20201031 | — | — |
| Internet Archive Scholar | 20201004 | — | — |
| Valyu | 20200626 | — | — |
| Rainforest API | 20200610 | — | — |
| NewsCatcher | 20200512 | — | — |
| Playwright (OSS) | 20200509 | — | — |
| Jina AI | 20200505 | — | — |
| ScrapingDog | 20200430 | — | — |
| ScrapingAnt | 20200411 | — | — |
| Currents API | 20200104 | — | — |
| Simplescraper | 20191024 | — | — |
| ScreenshotAPI.net | 20191014 | — | — |
| ScrapingBee | 20191006 | — | — |
| SerpWow | 20190719 | — | — |
| Zenserp | 20190314 | — | — |
| Tavily AI | 20180807 | — | — |
| Nodemaven | 20180805 | — | — |
| SerpStack | 20180805 | — | — |
| ApiFlash | 20180726 | — | — |
| Browse AI | 20180724 | — | — |
| ScraperAPI | 20180612 | — | — |
| Scite | 20180527 | — | — |
| Microlink | 20171120 | — | — |
| Webz.io | 20171101 | — | — |
| Browserless | 20170911 | — | — |
| Wiby | 20170816 | — | — |
| DataCite API | 20170708 | — | — |
| Kernel | 20170616 | — | — |
| OSF API | 20170606 | — | — |
| Mastodon API | 20170603 | — | — |
| Parallel | 20170521 | — | — |
| Unpaywall | 20170314 | — | — |
| urlscan.io | 20170314 | — | — |
| DataForSEO | 20170307 | — | — |
| NetNut | 20170114 | — | — |
| FRED | 20160617 | — | — |
| Octoparse | 20160324 | — | — |
| USPTO | 20160322 | — | — |
| Oxylabs | 20160227 | — | — |
| Exa | 20160204 | — | — |
| crt.sh | 20151224 | — | — |
| Semantic Scholar | 20151103 | — | — |
| Wikidata SPARQL | 20150919 | — | — |
| 4get (OSS) | 20150801 | — | — |
| GNews | 20150130 | — | — |
| Web Scraper | 20140917 | — | — |
| ScrapeHero Cloud | 20140804 | — | — |
| CoinGecko | 20140410 | — | — |
| GDELT | 20140131 | — | — |
| Hacker News (Algolia) | 20140127 | — | — |
| Crawlbase | 20131122 | — | — |
| ParseHub | 20131028 | — | — |
| ScraperBox | 20130806 | — | — |
| Nimble | 20130717 | — | $47M Series B (blog) |
| bioRxiv API | 20130715 | — | — |
| OpenAlex | 20130711 | — | — |
| RapidAPI | 20130617 | — | — |
| Zenodo API | 20130531 | — | — |
| Skyvern | 20130424 | — | — |
| SerpApi | 20130413 | — | — |
| World Bank | 20130401 | — | — |
| NewsAPI | 20121230 | — | — |
| Event Registry | 20121223 | — | — |
| ip-api | 20120801 | — | — |
| RDAP | 20111118 | — | — |
| Europe PMC | 20110704 | — | — |
| Nominatim (OSM) | 20110514 | — | — |
| xAI Live Search | 20110222 | — | — |
| HasData | 20110207 | — | — |
| Groq Compound | 20110202 | — | — |
| Open-Meteo | 20110202 | — | — |
| Figshare API | 20110113 | — | — |
| Z.ai / Zhipu | 20100712 | — | — |
| OpenAIRE | 20100116 | — | — |
| FiveFilters Full-Text RSS | 20091111 | — | — |
| Cloudflare Browser Rendering | 20090901 | — | — |
| Arquivo.pt | 20090211 | — | — |
| SauceNAO | 20081101 | — | — |
| Scrapy (OSS) | 20081015 | — | — |
| New York Times API | 20080912 | — | — |
| DuckDuckGo Instant Answer | 20080820 | — | — |
| Common Crawl | 20080328 | — | — |
| Alibaba Qwen (DashScope) | 20071017 | — | — |
| Apify | 20070531 | — | — |
| BASE | 20070427 | — | — |
| DBpedia | 20070207 | — | — |
| Diffbot | 20070203 | — | — |
| HAL API | 20070110 | — | — |
| Open Library | 20051028 | — | — |
| Reddit JSON | 20050725 | — | — |
| Mojeek Search API | 20041127 | — | — |
| DeepSeek | 20040827 | — | — |
| You.com | 20040626 | — | — |
| Wikimedia REST | 20040413 | — | — |
| Urlbox | 20040401 | — | — |
| Wayback Machine CDX | 20040401 | — | — |
| OpenAI Web Search | 20040328 | — | — |
| Crossref REST API | 20040325 | — | — |
| Presearch | 20040324 | — | — |
| StackExchange API | 20040324 | — | — |
| Decodo | 20040317 | — | — |
| Kagi Search API | 20040304 | — | — |
| Stract | 20040228 | — | — |
| Bright Data | 20040210 | — | — |
| Zyte | 20040208 | — | — |
| CORE | 20040206 | — | — |
| Naver Search API | 20040130 | — | — |
| DOAJ API | 20040129 | — | — |
| Teclis | 20040128 | — | — |
| Cohere | 20040127 | — | — |
| Mediastack | 20040124 | — | — |
| Anthropic Web Search | 20040123 | — | — |
| Openverse API | 20040123 | — | — |
| Browserbase | 20040121 | — | — |
| Yep | 20040121 | — | — |
| Bing Web Search API | 20040110 | — | — |
| PubMed E-utilities | 20040105 | — | — |
| Agenty | 20040103 | — | — |
| Google Books API | 20040103 | — | — |
| Google Programmable Search | 20040103 | — | — |
| Brave Search API | 20040102 | — | — |
| Kakao/Daum Search API | 20040102 | — | — |
| Firecrawl self-host (OSS) | no capture | ★192859 | — |
| MarkItDown (OSS) | no capture | ★190961 | — |
| Crawl4AI (OSS) | no capture | ★85801 | — |
| MinerU (OSS) | no capture | ★82013 | — |
| Docling (OSS) | no capture | ★69086 | — |
| Khoj (OSS) | no capture | ★37741 | — |
| Perplexica (OSS) | no capture | ★37392 | — |
| STORM (OSS) | no capture | ★31665 | — |
| GPT Researcher (OSS) | no capture | ★30164 | — |
| Stagehand (OSS) | no capture | ★25729 | — |
| Maxun (OSS) | no capture | ★17901 | — |
| Katana (OSS) | no capture | ★17686 | — |
| Whoogle (OSS) | no capture | ★11564 | — |
| Morphic (OSS) | no capture | ★9176 | — |

180 of 198 providers have a dated first capture. Oldest domains: Brave Search API 2004, Kakao/Daum Search API 2004, Agenty 2004, Google Programmable Search 2004, Google Books API 2004, PubMed E-utilities 2004. Youngest: Cloro 2025, Keenable 2025, SearchCans 2026, Octen 2026, treg 2026, Litescrape 2026.

Caveats: a first capture only proves a domain existed at that date, not that the same company or product was operating it — several of these domains changed hands. A domain registered recently says nothing about the API's reliability, and stars measure attention, not uptime. Neither signal is evidence about free-tier terms.

## 5. Post-signup bonuses

Documented extras beyond the base free tier (as stated in the fetched pricing/docs pages).

| Provider | Extra | Source |
|----------|-------|--------|
| Brave Search API | prepaid, no subscription; Goggles custom reranking | https://brave.com/search/api/ |
| Context.dev | earn free credits / redeem codes in dashboard | https://docs.context.dev/account/credits.md |
| Exa | startup/education grants up to $1,000; x402/MPP pay-per-request without key | https://exa.ai/pricing |
| Firecrawl | keyless free tier for Scrape/Search/Interact (per-IP daily cap); 2 months free on annual paid plans | https://docs.firecrawl.dev/billing.md |
| Jina AI | keyless r.jina.ai usage; open-weight models on HuggingFace | https://jina.ai/ |
| Keenable | keyless calls consume no credits; x402 pay-per-request at $0.01 | https://docs.keenable.ai/credits.md |
| Linkup | $5,000 startup credits program | https://www.linkup.so/pricing |
| Parallel | free Search MCP server for hobbyist use | https://parallel.ai/ |
| Tavily AI | keyless Search/Extract without an API key (rate-limited); x402 pay-per-request with no account | https://docs.tavily.com/llms.txt |
| TikHub | volume discounts up to 50% | https://tikhub.io/pricing |
| TinyFish | Search and Fetch free within daily allowance | https://docs.tinyfish.ai/search-api/index.md |
| treg | free trial pools: finnhub 50/day, twelvedata 20/day, tiingo 20/day | https://treg.to/llms.txt |
| Valyu | 50% off first month (first 24h after signup) | https://docs.valyu.ai/pricing |
| You.com | free MCP tier with no signup | https://you.com/docs/llms.txt |
| Apify | $5/month platform credits; store discount on paid plans | https://apify.com/pricing |
| Bright Data | no card, no promo code; $5 bonus on adding payment method | https://docs.brightdata.com/general/account/billing-and-pricing/free-tier.md |
| Crawlbase | one rate card for all products; pay only for successful requests | https://crawlbase.com/pricing |
| HasData | free plan covers all tools | https://hasdata.com/pricing |
| Scrape.do | residential and mobile proxies included on free plan | https://scrape.do/pricing/ |
| ScrapeOps | free plan includes monitoring and scheduler | https://scrapeops.io/ |
| Scrapfly | free tier usable forever for prototypes | https://scrapfly.io/pricing |
| ScrapingAnt | every tier includes 10,000 credits to start | https://scrapingant.com/ |
| ScrapingBee | no card required to try | https://www.scrapingbee.com/ |
| SerpApi | cached searches are free and do not count toward monthly searches | https://serpapi.com/pricing |
| Serply | credits do not auto-expire after purchase | https://serply.io/pricing |
| ZenRows | every primitive unlocked on free plan; budget preview per request | https://www.zenrows.com/ |
| Zenserp | only successful requests billed | https://zenserp.com/ |
| Zyte | pay per successful response | https://www.zyte.com/pricing/ |
| Airtop | one-time signup grant of 30,000 credits | https://www.airtop.ai/help/billing/billing.md |
| Browserbase | runtime included; Stagehand framework open source | https://www.browserbase.com/pricing |
| Cloudflare Browser Rendering | works on Workers Free plan | https://developers.cloudflare.com/browser-rendering/platform/pricing/ |
| Hyperbrowser | all four products included on free tier | https://www.hyperbrowser.ai/pricing |
| Notte | no Notte markup; credits cover sessions, proxies, LLMs, functions | https://www.notte.cc/pricing |
| Skyvern | open-source Skyvern available | https://www.skyvern.com/pricing |
| Steel.dev | open-source browser infra | https://steel.dev/pricing |
| Google Programmable Search | Programmable Search Engine UI free | https://developers.google.com/custom-search/v1/overview |
| Marginalia | no ads, no tracking | https://api.marginalia.nu/ |
| Mwmbl | open source | https://mwmbl.org/ |
| Microlink | every feature unlocked on free plan | https://microlink.io/pricing |
| Common Crawl | petabytes of crawl data free | https://commoncrawl.org/cc-index |
| Currents API | real-time and historical news on free tier | https://currentsapi.services/en/pricing |
| The Guardian Open Platform | free for non-commercial usage | https://open-platform.theguardian.com/access/ |
| OpenAlex | free API key issued in one call for agents | https://help.openalex.org/access/pricing/ |
| Bluesky AT Protocol | open protocol | https://docs.bsky.app/ |
| CoinGecko | free demo key for all users | https://docs.coingecko.com/ |
| Open Library | free monthly data dumps | https://openlibrary.org/developers/api |
| Open-Meteo | no key, no sign-up | https://open-meteo.com/en/pricing |
| StackExchange API | free app key raises quota | https://api.stackexchange.com/docs |
| Wikimedia REST | free community access on Enterprise | https://api.wikimedia.org/ |
| Cohere | evaluation keys free | https://docs.cohere.com/docs/rate-limits |
| Google Gemini Grounding | Gemini free tier includes grounding quota | https://ai.google.dev/gemini-api/docs/pricing |
| OpenRouter | free model pool; deposit raises daily free-model cap | https://openrouter.ai/docs |

Common patterns, and what each is actually worth: work-email upgrades (Valyu doubles the signup grant to $20), payment-method bonuses (Bright Data adds $5 but converts a no-card free tier into a card-on-file account), startup programmes (Exa up to $1,000; Linkup up to $5,000, but application-based rather than automatic), agent-payment rails that need no account at all (x402 on Tavily, Exa and Keenable), and free tiers that require no card from the start.

The last group is the one that matters for a gateway that must not stop working: a keyless path (Tavily keyless Search/Extract, Jina Reader, Firecrawl keyless scrape, Keenable keyless calls) keeps a fallback alive after every monthly allowance is spent, at a lower rate and with no account to lose.
