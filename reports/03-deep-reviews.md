# Deep reviews

Generated 2026-10-19 from `data/facts.json` and the treg leaderboard snapshot. Every allowance below is a quote from a captured page in `data/snapshots/`; every hit rate is from treg's 30-day routed-call window and is labelled measured. Where a provider publishes no number, the review says so instead of inferring one. `make test` fails if a quote stops matching its snapshot.

## 1. Tavily

| | |
|---|---|
| Home | https://tavily.com/ |
| Pricing | https://www.tavily.com/#pricing |
| Docs | https://docs.tavily.com/ |
| llms.txt | https://docs.tavily.com/llms.txt |
| Recurring free volume | **1,000 calls/month** |
| Evidence confidence | **high** |
| Facts row | `data/facts.json` → `tavily` |
| Endpoints | Search, Extract, Map, Crawl, Research |

Documented allowance, verbatim from the captured page:

> Get a free API key at https://app.tavily.com (1,000 credits/month, no credit card required).
>
> — https://docs.tavily.com/llms.txt (`data/snapshots/tavily/llms.txt`)

**What the credit buys.** Tavily bills one credit for a basic search or a basic page extract, and more for advanced/deep search and research mode. The allowance is therefore an upper bound on calls, not a flat count: a gateway that mixes basic search with advanced extract spends the 1,000 faster than a naive `credits = calls` budget predicts. Plan the monthly budget in credits per operation, not in calls.

**Why it suits an agent gateway.** One call returns ranked results plus optional synthesized content, so many queries need no second fetch. Output is JSON with an `answer` field and per-result `content`, which is directly usable as LLM context. There is also a keyless path for Search and Extract, so a gateway can keep working after the monthly credits are spent, at a lower per-IP rate.

**Failure mode.** Tavily's miss is a thin or empty result set, not a 403. That is a quality signal rather than a routing signal, so the gateway has to judge result count itself. The measured fetch rate is well below the measured search rate, so do not use it as the only fetch leg.

Measured on treg's routed workload, 30-day window (`data/snapshots/treg/leaderboard.txt`):

| Task | Success | ok calls | Rate samples | Median ms |
|------|---:|---:|---:|---:|
| search | 87.2% | 2,333 | 2,676 | 2300 |
| fetch | 75.1% | 8,899 | 11,850 | 1204 |
| news | —% | — | 193 | 1419 |
| sitemap | 78.1% | 25 | 32 | 2554 |

The search/fetch gap is the number that matters: a good search rate does not carry over to page retrieval.

## 2. Exa

| | |
|---|---|
| Home | https://exa.ai/ |
| Pricing | https://exa.ai/pricing |
| Docs | https://docs.exa.ai/ |
| llms.txt | https://exa.ai/docs/llms.txt |
| Recurring free volume | **2,500 calls/month** |
| One-time grant | $10 onboarding bonus credits |
| Card for free tier | no |
| Evidence confidence | **high** |
| Facts row | `data/facts.json` → `exa` |
| Endpoints | Search, Deep Search, Contents, Similar, Answer, Agent, Monitors, Websets |

Documented allowance, verbatim from the captured page:

> Free $10 credits every month plus a $10 onboarding bonus. No payment method required
>
> — https://exa.ai/pricing (`data/snapshots/exa/pricing.txt`)

**Denominated in dollars, not credits.** Exa's free tier is a monthly USD balance, so the effective call count depends entirely on the endpoint chosen. From the captured rate card (per 1,000 requests, up to 10 results): Instant Search $4, Fast/Auto $7, Deep $12, Deep-Reasoning $15, Contents $1 per 1,000 pages per content type. A $10 monthly balance is therefore about 2,500 Instant searches, about 1,400 Fast searches, or about 660 Deep-Reasoning calls. A gateway can price a mixed workload from one balance, but it has to read the rate card to know what is left; the same balance is worth a factor of four depending on the endpoint.

**Contents is billed per page per content type.** The rate card says `$1 /1k pages per content type`, so requesting text, highlights and summary for the same page is three charges rather than one. This is the most common way to spend the monthly balance faster than expected, and it is invisible unless the request is priced before it is sent.

**Measured strength.** Exa has the largest independent sample in the inventory and is strong on both search and fetch, which is unusual: most providers are good at one. Its median fetch latency is also far below the field. That combination makes it the natural quality leg, with the caveat that the absolute budget is small.

Measured on treg's routed workload, 30-day window (`data/snapshots/treg/leaderboard.txt`):

| Task | Success | ok calls | Rate samples | Median ms |
|------|---:|---:|---:|---:|
| search | 98.1% | 102,669 | 104,657 | 1634 |
| fetch | 89.0% | 103,084 | 115,825 | 87 |
| news | 99.4% | 9,943 | 10,003 | 507 |
| papers | 100.0% | 488 | 488 | 567 |

The largest measured sample in the inventory. A high rate on 100k+ samples is a materially stronger claim than the same rate on 200.

## 3. Firecrawl

| | |
|---|---|
| Home | https://www.firecrawl.dev/ |
| Pricing | https://www.firecrawl.dev/pricing |
| Docs | https://docs.firecrawl.dev/ |
| llms.txt | https://docs.firecrawl.dev/llms.txt |
| Recurring free volume | **1,000 calls/month** |
| Evidence confidence | **high** |
| Facts row | `data/facts.json` → `firecrawl` |
| Endpoints | Scrape, Crawl, Map, Search, Extract, Interact, Agent |
| Self-host | AGPL-3.0, same API shape |

Documented allowance, verbatim from the captured page:

> **1,000 credits per month.** The allotment resets at the start of each monthly cycle. Unused free credits do not roll over.
>
> — https://docs.firecrawl.dev/billing.md (`data/snapshots/firecrawl/billing-md.txt`)

**The credit ladder.** Costs are per endpoint and per option: scrape and crawl one credit per page, map one per call, search two per ten results, JSON extraction four per page, PDF parsing one per page, browser sandbox two to seven per minute. The 1,000-credit allowance is therefore between about 1,000 simple scrapes and a few hundred extraction-heavy ones.

**Clean failure semantics.** On the free plan there is no pay-as-you-go: when the monthly allotment is gone, requests return HTTP 402. That is the cleanest routing signal in the inventory — the gateway can treat 402 as "switch provider" without guessing.

**The search/fetch split is the finding.** Firecrawl measures near the top of the field on search and near the bottom on fetch, on a large sample. This is not a claim that it cannot scrape; it means that on treg's routed workload another provider was usually the one that returned the page. Design accordingly: use its search-plus-scrape path, and keep a second fetch leg.

**Escape hatch.** It is the only one of these three with a self-hosted build under the same API shape, so the cloud allowance can be supplemented by running the crawler yourself. That trades a per-call cost for browser memory and your own IP reputation.

Measured on treg's routed workload, 30-day window (`data/snapshots/treg/leaderboard.txt`):

| Task | Success | ok calls | Rate samples | Median ms |
|------|---:|---:|---:|---:|
| search | 99.8% | 9,487 | 9,506 | 687 |
| fetch | 32.2% | 44,493 | 138,177 | 2086 |
| sitemap | 100.0% | 155 | 155 | 7859 |

The 32% fetch figure is the sharpest contradiction of vendor marketing in this inventory, and it comes with a 138k sample.

### What these three add up to

| | Tavily | Exa | Firecrawl |
|---|---|---|---|
| Recurring free volume | 1,000 | 2,500 | 1,000 |
| One-time grant | — | $10 onboarding bonus credits | — |
| Card required | no | no | no |
| Measured search | 87.2% | 98.1% | 99.8% |
| Measured fetch | 75.1% | 89.0% | 32.2% |

All three are enough for interactive personal use and none is enough for unattended crawling. Only Exa is measured above 85% on both search and fetch. Their failure modes differ and each is usable as a routing signal: Tavily degrades to thin results, Firecrawl returns 402 at the boundary, Exa stops when the balance is empty. A zero-marginal-cost chain is Tavily keyless search, then Exa's monthly balance for the queries that need quality, then Firecrawl's keyless scrape, then a recurring-credit scraper for pages that still fail.

## 4. Jina AI (Reader, Search, embeddings)

| | |
|---|---|
| Home | https://jina.ai/ |
| Pricing | https://jina.ai/pricing |
| Docs | https://docs.jina.ai/ |
| llms.txt | https://docs.jina.ai/llms.txt |
| Recurring free volume | not quantified in the fetched docs |
| Evidence confidence | **medium** |
| Facts row | `data/facts.json` → `jina` |

Documented allowance, verbatim from the captured page:

> Rate limits: - Embedding & Reranker APIs: 500 RPM & 1M TPM (2k RPM & 5M TPM premium) - r.jina.ai: 500 RPM (5k RPM premium) - s.jina.ai: 100 RPM (1000 RPM premium)
>
> — https://jina.ai/ (`data/snapshots/jina/llms-full.txt`)

**Why the free tier has no number.** Jina publishes rate limits for a free key rather than a monthly credit pool, so the budget is throughput, not volume. That is a different shape from every other provider here: there is no monthly cliff, and the only ceiling is requests per minute. For a single user that is usually better than a credit pool.

**The Reader is the cheapest fetch primitive in the inventory.** `r.jina.ai/<url>` needs no SDK and no key for basic use, and switches output between text, markdown and JSON. It is a text transform, not a bot-protection layer: it does not solve an interstitial for you, so pair it with a provider that does when the target is defended.

**What is not known.** The fetched docs do not state a monthly token or call grant for the free key, so no monthly volume is claimed in this inventory. Any figure circulating elsewhere should be re-checked against a dashboard before it is planned against.

No independent measurement: this provider is not routed by the treg Web Arena leaderboard snapshot, so there is no hit rate to cite and none is claimed here.

## 5. Brave Search API

| | |
|---|---|
| Home | https://brave.com/search/api/ |
| Pricing | https://brave.com/search/api/#pricing |
| Docs | https://api.search.brave.com/app/documentation |
| llms.txt | none usable — no response (connection failed or refused) |
| Recurring free volume | **1,000 calls/month** |
| Evidence confidence | **high** |
| Facts row | `data/facts.json` → `brave` |

Documented allowance, verbatim from the captured page:

> #### Includes _$5 in free_ credits _every month_  Credits are automatically applied to your account
>
> — https://brave.com/search/api/ (`data/snapshots/brave/api-page.txt`)

**Budget in dollars.** Brave bills prepaid USD credits and applies $5 per month automatically. At the search rate card that is roughly a thousand queries; the page's larger "free calls" figure spans several products, so it is not extra search volume. Track the balance in dollars rather than calls.

**Why it earns a slot despite the small allowance.** It runs its own index rather than reselling another engine, which makes it the diversity leg when the primary search is a reseller that breaks when the upstream engine changes. It is not routed by treg, so there is no independent hit rate for it in this inventory and none is claimed.

**Gateway role.** Query it as a second opinion and compare top-N overlap with the primary. Do not use it for bulk crawling; the value is concentrated in search.

No independent measurement: this provider is not routed by the treg Web Arena leaderboard snapshot, so there is no hit rate to cite and none is claimed here.

## 6. ZenRows

| | |
|---|---|
| Home | https://www.zenrows.com/ |
| Pricing | https://www.zenrows.com/pricing |
| Docs | https://docs.zenrows.com/ |
| llms.txt | https://docs.zenrows.com/llms.txt |
| Recurring free volume | **5,000 calls/month** |
| Evidence confidence | **high** |
| Facts row | `data/facts.json` → `zenrows` |

Documented allowance, verbatim from the captured page:

> It's recurring, not a time-limited trial: 5,000 credits every month, no credit card required.
>
> — https://www.zenrows.com/ (`data/snapshots/zenrows/home.txt`)

**Credit ladder, not a flat pool.** A standard request costs one credit, JS rendering five, premium proxies ten, protected pages twenty-five. The nominal monthly allowance is therefore the best case, and a workload aimed at defended pages divides it by up to twenty-five. This is the single most important number to model before relying on it.

**Failure accounting is favourable.** Failed requests are not charged, which matters far more than a larger nominal grant for a retry-heavy gateway: a page that fails costs time, not budget.

No independent measurement: this provider is not routed by the treg Web Arena leaderboard snapshot, so there is no hit rate to cite and none is claimed here.

## 7. Bright Data

| | |
|---|---|
| Home | https://brightdata.com/ |
| Pricing | https://brightdata.com/pricing |
| Docs | https://docs.brightdata.com/ |
| llms.txt | https://docs.brightdata.com/llms.txt |
| Recurring free volume | **5,000 calls/month** |
| One-time grant | $2 trial credit (7 days) + $5 bonus when payment method added |
| Card for free tier | no |
| Evidence confidence | **high** |
| Facts row | `data/facts.json` → `brightdata` |

Documented allowance, verbatim from the captured page:

> Every new Bright Data account gets **5,000 free credits per month** (~$7.50 value), applied automatically at signup. No credit card, no promo code, no commitment.
>
> — https://docs.brightdata.com/general/account/billing-and-pricing/free-tier.md (`data/snapshots/brightdata/llms-full.txt`)

**Shared across products.** The monthly credits are one pool across the unlocker, SERP API, scraper API and scraper studio, and explicitly exclude the proxy and browser products. Spending them on SERP calls is usually the best value per credit; spending them on the heaviest unlocker tier burns the pool quickly.

**The card bonus is a trap for this use case.** There is a separate small trial credit and a bonus for adding a payment method. The bonus is larger than the trial but converts a no-card free tier into a card-on-file account, which is the thing this inventory is trying to avoid.

No independent measurement: this provider is not routed by the treg Web Arena leaderboard snapshot, so there is no hit rate to cite and none is claimed here.

## 8. ScrapingAnt

| | |
|---|---|
| Home | https://scrapingant.com/ |
| Pricing | https://scrapingant.com/pricing |
| Docs | https://docs.scrapingant.com/ |
| llms.txt | none usable — HTTP 404 |
| Recurring free volume | **10,000 calls/month** |
| Evidence confidence | **high** |
| Facts row | `data/facts.json` → `scrapingant` |

Documented allowance, verbatim from the captured page:

> 10,000 free credits every month · no credit card required
>
> — https://scrapingant.com/ (`data/snapshots/scrapingant/home.txt`)

**The largest no-card recurring allowance in the scraper cluster.** The captured pages state the monthly credit figure but do not publish a per-request credit ladder, so the number of *pages* the allowance buys is not documented here and is not inferred. Plan in credits and read the dashboard's consumption per call before committing a workload to it.

**What it is for.** Headless Chrome behind rotating proxies in one API call, which makes it the natural high-volume fetch leg. Because the per-request credit cost of JS rendering and premium proxies is not stated in the captured pages, whether a defended target consumes one credit or several is unknown from this evidence.

No independent measurement: this provider is not routed by the treg Web Arena leaderboard snapshot, so there is no hit rate to cite and none is claimed here.

