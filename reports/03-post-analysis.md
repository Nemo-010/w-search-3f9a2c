# Post-analysis

All figures derive from `data/facts.json` (fetched 2026-10-19). Nothing here is an estimate unless the row says so.

## 1. Total volume with 5 accounts per provider

Method: documented recurring monthly free volume × 5. One-time grants are kept separate and are not mixed into the recurring total. Providers whose free tier is a rate limit with no published monthly cap are excluded from the sum (their row says so).

| Provider | Per account /mo | ×5 | Basis |
|----------|---:|---:|-------|
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
| Airtop | 1,000 | **5,000** | Free plan: 1,000 credits every month, renews monthly |
| Browserless | 1,000 | **5,000** | Free plan: 1k sessions/month, no card |
| Cohere | 1,000 | **5,000** | Trial (free) keys: 1,000 API calls/month, 20 req/min |
| Cloro | 500 | **2,500** | Free plan $0/month: 500 credits/month |
| SerpStack | 100 | **500** | Free plan: 100 searches/month, non-commercial, JSON only |
| ApiFlash | 100 | **500** | 100 screenshots/month free, no card |
| Microlink | 100 | **500** | Free plan: 100 requests/month, no card |
| Mediastack | 100 | **500** | Free plan: 100 requests/month, delayed news, all sources/languages, HTTPS |
| Zenserp | 50 | **250** | 50 free searches/month, no strings attached |
| **Total** | | **8,062,250** | |

Documented recurring free volume across all re-verified providers, 5 accounts each: **8,062,250 calls/month**. The largest single contributors: Naver Search API 3,750,000, TinyFish 1,800,000, Open-Meteo 1,500,000, Keenable 500,000, The Guardian Open Platform 75,000, ScrapingAnt 50,000.

Reported but not re-verified in this snapshot run (excluded from the total above):

- Unpaywall: 3,000,000/month reported — Free API: 100,000 requests/day (~3M/month) with email in request (`unpaywall`, confidence medium)
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
- ScreenshotOne: 100/month reported — Free plan (100 screenshots/month commonly advertised; not captured in snapshot) (`screenshotone`, confidence low)

One-time, first-month totals (not recurring, ×5 accounts where the grant is per account):

- Apify: $500 free usage for 6 months for own Actors/agents program
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

Two separate evidence classes, kept apart:

**Measured (independent):** the treg Web Arena leaderboard records per-provider hit rate, median latency and price on live routed calls over a 30-day window. Snapshot: `data/snapshots/treg/leaderboard.json`, updated 2026-10-19T05:43Z.


**Vendor-claimed (not independently measured here):**


## 3. One-time vs monthly credits

- **Recurring monthly free volume documented:** 46 providers.
- **Recurring + one-time bonus:** 4 providers (Exa, Parallel, Bright Data, Hyperbrowser).
- **One-time only:** 23 providers (Octen, ScrapeGraphAI, Search1API, TikHub, treg, Valyu, You.com, Apify, Crawlbase, DataForSEO, ScrapeOps, ScraperAPI, Scrapfly, ScrapingBee, ScrapingDog, SearchCans, Serply, Web Scraper, Zyte, Notte, Skyvern, Steel.dev, NewsCatcher).
- **Free tier exists but no number in fetched sources, or no free tier:** 123 providers.

Practical reading: a free tier that resets monthly is a permanent budget; a one-time grant is a trial. Providers that document both (Exa, Bright Data, Valyu partly, Zyte + bonus patterns) give the longest runway.

## 4. Maturity, popularity, market awareness

Signals used: first Wayback Machine capture of the primary domain (longevity), GitHub stars where the project is open source (community size), and funding claims made in the providers' own docs (market awareness; vendor-announced, not audited).

| Provider | First web capture | GitHub stars | Funding / company signal |
|----------|-------------------|--------------|--------------------------|
| Octen | 20260214 | — | — |
| Keenable | 20251231 | — | $26M from Accel and Conviction (site) |
| TinyFish | 20240821 | — | — |
| Linkup | 20240501 | — | $10M seed led by Gradient (blog) |
| Firecrawl | 20240413 | — | $75M Series B (announced on site) |
| Search1API | 20240402 | — | — |
| Brand.dev | 20230724 | — | — |
| Olostep | 20230724 | — | — |
| Perplexity | 20211218 | — | — |
| Fiber AI | 20211204 | — | — |
| Context.dev | 20211129 | — | — |
| Valyu | 20200626 | — | — |
| Jina AI | 20200505 | — | — |
| Tavily AI | 20180807 | — | — |
| Parallel | 20170521 | — | — |
| Exa | 20160204 | — | — |
| Nimble | 20130717 | — | $47M Series B (blog) |
| Diffbot | 20070203 | — | — |
| You.com | 20040626 | — | — |
| Brave Search API | 20040102 | — | — |
| Firecrawl self-host (OSS) | — | ★192859 | — |
| MarkItDown (OSS) | — | ★190961 | — |
| Crawl4AI (OSS) | — | ★85801 | — |
| MinerU (OSS) | — | ★82013 | — |
| Docling (OSS) | — | ★69086 | — |
| Khoj (OSS) | — | ★37741 | — |
| Perplexica (OSS) | — | ★37392 | — |
| STORM (OSS) | — | ★31665 | — |
| GPT Researcher (OSS) | — | ★30164 | — |
| Stagehand (OSS) | — | ★25729 | — |
| Maxun (OSS) | — | ★17901 | — |
| Katana (OSS) | — | ★17686 | — |
| Whoogle (OSS) | — | ★11564 | — |
| Morphic (OSS) | — | ★9176 | — |
| 4get (OSS) | — | — | — |
| Agenty | — | — | — |
| Airtop | — | — | — |
| Alibaba Qwen (DashScope) | — | — | — |
| Anchor Browser | — | — | — |
| Anthropic Web Search | — | — | — |
| AnyAPI | — | — | — |
| ApiFlash | — | — | — |
| Apify | — | — | — |
| Arquivo.pt | — | — | — |
| BASE | — | — | — |
| Bing Web Search API | — | — | — |
| Bluesky AT Protocol | — | — | — |
| Bocha AI | — | — | — |
| Bright Data | — | — | — |
| Browse AI | — | — | — |
| Browser Use (OSS) | — | — | — |
| Browserbase | — | — | — |
| Browserless | — | — | — |
| CORE | — | — | — |
| Cloro | — | — | — |
| Cloudflare Browser Rendering | — | — | — |
| Cohere | — | — | — |
| CoinGecko | — | — | — |
| Common Crawl | — | — | — |
| Crawlbase | — | — | — |
| Crawlee (OSS) | — | — | — |
| Crossref REST API | — | — | — |
| Currents API | — | — | — |
| DBpedia | — | — | — |
| DOAJ API | — | — | — |
| DataCite API | — | — | — |
| DataForSEO | — | — | — |
| Decodo | — | — | — |
| DeepSeek | — | — | — |
| DuckDuckGo Instant Answer | — | — | — |
| Europe PMC | — | — | — |
| Event Registry | — | — | — |
| FRED | — | — | — |
| Fetchin | — | — | — |
| Figshare API | — | — | — |
| FiveFilters Full-Text RSS | — | — | — |
| GDELT | — | — | — |
| GNews | — | — | — |
| GitHub Search API | — | — | — |
| Google Books API | — | — | — |
| Google Gemini Grounding | — | — | — |
| Google Programmable Search | — | — | — |
| Groq Compound | — | — | — |
| HAL API | — | — | — |
| Hacker News (Algolia) | — | — | — |
| HasData | — | — | — |
| Hyperbrowser | — | — | — |
| Internet Archive Scholar | — | — | — |
| Just One API | — | — | — |
| Kagi Search API | — | — | — |
| Kakao/Daum Search API | — | — | — |
| Kernel | — | — | — |
| LibreY (OSS) | — | — | — |
| Lightpanda (OSS) | — | — | — |
| Litescrape | — | — | — |
| Marginalia | — | — | — |
| Mastodon API | — | — | — |
| Mediastack | — | — | — |
| Microlink | — | — | — |
| MiniMax | — | — | — |
| Mistral | — | — | — |
| Mojeek Search API | — | — | — |
| Moonshot Kimi | — | — | — |
| Mwmbl | — | — | — |
| Naver Search API | — | — | — |
| NetNut | — | — | — |
| New York Times API | — | — | — |
| NewsAPI | — | — | — |
| NewsCatcher | — | — | — |
| NewsData.io | — | — | — |
| Nodemaven | — | — | — |
| Nominatim (OSM) | — | — | — |
| Notte | — | — | — |
| OSF API | — | — | — |
| Octoparse | — | — | — |
| Open Library | — | — | — |
| Open-Meteo | — | — | — |
| OpenAI Web Search | — | — | — |
| OpenAIRE | — | — | — |
| OpenAlex | — | — | — |
| OpenRouter | — | — | — |
| Openverse API | — | — | — |
| Oxylabs | — | — | — |
| ParseHub | — | — | — |
| Playwright (OSS) | — | — | — |
| Presearch | — | — | — |
| PubMed E-utilities | — | — | — |
| RDAP | — | — | — |
| REST Countries | — | — | — |
| Rainforest API | — | — | — |
| RapidAPI | — | — | — |
| Reddit JSON | — | — | — |
| Right Dao | — | — | — |
| SauceNAO | — | — | — |
| Scite | — | — | — |
| Scrape.do | — | — | — |
| ScrapeCreators | — | — | — |
| ScrapeGraphAI | — | — | — |
| ScrapeHero Cloud | — | — | — |
| ScrapeNinja | — | — | — |
| ScrapeOps | — | — | — |
| ScrapeOps Proxy | — | — | — |
| ScraperAPI | — | — | — |
| ScraperBox | — | — | — |
| Scrapfly | — | — | — |
| ScrapingAnt | — | — | — |
| ScrapingBee | — | — | — |
| ScrapingDog | — | — | — |
| Scrapy (OSS) | — | — | — |
| ScreenshotAPI.net | — | — | — |
| ScreenshotOne | — | — | — |
| SearXNG (OSS) | — | — | — |
| SearchCans | — | — | — |
| Semantic Scholar | — | — | — |
| SerpApi | — | — | — |
| SerpStack | — | — | — |
| SerpWow | — | — | — |
| Serpdog | — | — | — |
| Serper | — | — | — |
| Serply | — | — | — |
| Simplescraper | — | — | — |
| Skyvern | — | — | — |
| Spider | — | — | — |
| StackExchange API | — | — | — |
| Steel.dev | — | — | — |
| Stract | — | — | — |
| Teclis | — | — | — |
| The Guardian Open Platform | — | — | — |
| TheNewsAPI | — | — | — |
| TikHub | — | — | — |
| Trafilatura (OSS) | — | — | — |
| URLtoMarkdown | — | — | — |
| USPTO | — | — | — |
| Unpaywall | — | — | — |
| Urlbox | — | — | — |
| ValueSERP | — | — | — |
| Wayback Machine CDX | — | — | — |
| Web Scraper | — | — | — |
| Webz.io | — | — | — |
| Wiby | — | — | — |
| Wikidata SPARQL | — | — | — |
| Wikimedia REST | — | — | — |
| World Bank | — | — | — |
| Yep | — | — | — |
| Z.ai / Zhipu | — | — | — |
| ZenRows | — | — | — |
| Zenodo API | — | — | — |
| Zenserp | — | — | — |
| Zyte | — | — | — |
| arXiv API | — | — | — |
| bioRxiv API | — | — | — |
| crt.sh | — | — | — |
| iTunes Search API | — | — | — |
| ip-api | — | — | — |
| ipapi.co | — | — | — |
| treg | — | — | — |
| urlscan.io | — | — | — |
| xAI Live Search | — | — | — |

Caveats: a Wayback capture only proves a domain existed, not that the company was operating the same product; stars measure attention, not reliability. Providers launched 2024-2026 (Firecrawl, TinyFish, Keenable, Octen, Linkup) are the youngest.

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
| You.com | free MCP tier with no signup | https://you.com/docs/welcome.md |
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
| Browserbase | runtime included; Stagehand framework open source | https://www.browserbase.com/pricing |
| Cloudflare Browser Rendering | works on Workers Free plan | https://developers.cloudflare.com/browser-rendering/platform/pricing/ |
| Hyperbrowser | all four products included on free tier | https://www.hyperbrowser.ai/pricing |
| Notte | no Notte markup; credits cover sessions, proxies, LLMs, functions | https://www.notte.cc/pricing |
| Skyvern | open-source Skyvern available | https://www.skyvern.com/pricing |
| Steel.dev | open-source browser infra | https://steel.dev/pricing |
| Google Programmable Search | Programmable Search Engine UI free | https://developers.google.com/custom-search/v1/overview |
| Marginalia | no ads, no tracking | https://api.marginalia.nu/ |
| Mwmbl | open source | https://mwmbl.org/ |
| Stract | open source | https://stract.com/ |
| Microlink | every feature unlocked on free plan | https://microlink.io/pricing |
| Common Crawl | petabytes of crawl data free | https://commoncrawl.org/cc-index |
| Wayback Machine CDX | no key required | https://archive.org/help/wayback_api.jsp |
| Currents API | real-time and historical news on free tier | https://currentsapi.services/en/pricing |
| The Guardian Open Platform | free for non-commercial usage | https://open-platform.theguardian.com/access/ |
| CORE | open access full texts | https://core.ac.uk/services/api |
| OpenAlex | free API key issued in one call for agents | https://help.openalex.org/access/pricing/ |
| PubMed E-utilities | higher rate with free NCBI key | https://www.ncbi.nlm.nih.gov/books/NBK25501/ |
| Bluesky AT Protocol | open protocol | https://docs.bsky.app/ |
| CoinGecko | free demo key for all users | https://docs.coingecko.com/ |
| Hacker News (Algolia) | no key | https://hn.algolia.com/api |
| Mastodon API | self-hostable | https://docs.joinmastodon.org/api/ |
| Open Library | free monthly data dumps | https://openlibrary.org/developers/api |
| Open-Meteo | no key, no sign-up | https://open-meteo.com/en/pricing |
| StackExchange API | free app key raises quota | https://api.stackexchange.com/docs |
| Wikimedia REST | free community access on Enterprise | https://api.wikimedia.org/ |
| Cohere | evaluation keys free | https://docs.cohere.com/docs/rate-limits |
| Google Gemini Grounding | Gemini free tier includes grounding quota | https://ai.google.dev/gemini-api/docs/pricing |
| Groq Compound | free tier for developers | https://console.groq.com/docs/compound |
| Mistral | La Plateforme free tier for API experiments | https://mistral.ai/pricing |
| OpenRouter | free model pool; deposit raises daily free-model cap | https://openrouter.ai/docs |

Common patterns: work-email upgrades (Valyu doubles the grant), payment-method bonuses (Bright Data +$5), startup programs (Exa up to $1,000, Linkup $5,000), agent-payment rails (x402 on Tavily/Exa/Keenable, MPP on Exa), and free model/API tiers that require no card at all.
