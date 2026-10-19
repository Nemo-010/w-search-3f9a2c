# Deep reviews 4–8

Same evidence base: `data/snapshots/<slug>/` (fetched 2026-10-19) and the treg Web
Arena leaderboard snapshot. Vendor claims and independent measurements are labelled.

---

## 4. Jina AI (Reader + Search + embeddings)

| | |
|---|---|
| Home / docs | https://jina.ai/ · https://docs.jina.ai/ · `llms.txt` 27 KB, `llms-full.txt` present |
| Products | `r.jina.ai` (URL → Markdown), `s.jina.ai` (web search), embeddings, rerankers |
| Free tier | Free API key; docs publish rate limits rather than a monthly credit number |
| Documented limits | r.jina.ai **500 RPM**, s.jina.ai **100 RPM**, embeddings/reranker **500 RPM / 1M TPM** (premium: 5k RPM / 1k RPM / 2k RPM / 5M TPM) |
| Models | open weights on HuggingFace (CC-BY-NC-4.0 for the newest ones) |
| Status | acquired by Elastic, October 2025 (per jina.ai/models/llms.txt) |

**What it is good for.** The Reader (`r.jina.ai/<url>`) is the lowest-friction
URL→Markdown primitive in this inventory: no key needed for basic use, no SDK, and a
`x-respond-with`/`Accept` switch for text/markdown/JSON. For a personal gateway it is
the natural *fetch leg* behind a search provider: 500 RPM with a key is far more than a
single user needs, and because Jina publishes the limit as a rate rather than a credit
pool, there is no monthly cliff — the budget is throughput, not volume.

**Billing caveat.** The fetched docs do not publish a monthly token grant for the free
key on the Reader/Search endpoints; the documented free surface is the key plus the
RPM/TPM table. Any "Jina gives N free tokens" claim should be treated as unverified
unless re-checked against the dashboard. Embeddings are billed per token and the
newest models carry a non-commercial licence, which matters if the gateway later
indexes content for a product.

**Fit.** Strong: Reader for fetch, `s.jina.ai` for a secondary search, embeddings for
local retrieval. Weak: no crawling/mapping, no browser actions, no structured
extraction; the Reader is a text transform, not a bot-protection layer.

---

## 5. Brave Search API

| | |
|---|---|
| Home / pricing | https://brave.com/search/api/ |
| Free tier | **$5 credits every month**, automatically applied; page also advertises "up to $20 in free calls every month" |
| Price | $5 per 1,000 requests (Search); fast mode lower |
| Index | own index ("long-tail queries … not passed to Google or Bing" — vendor claim) |
| Vendor benchmark | FreshQA 85.3% accuracy at $18/1k questions all-in (vendor-run, methodology published) |
| Independent measurement | not present in the treg leaderboard snapshot (treg routes other search vendors) |

**Free-tier mechanics.** Brave bills in prepaid USD credits; the free plan's $5 is
applied monthly and at $5/1k requests is worth ~1,000 queries/month. The page's "up to
$20 in free calls" line refers to the combined free allowance across Search plus the
answer/grounding products, not to 4,000 extra search calls. There is no published
monthly *request* count, so the budget is best tracked in dollars.

**Why it is in the top set anyway.** It is one of the few providers with its own
independent web index (not a Google/Bing reseller), which makes it the obvious
diversity leg when a gateway's primary search is a SERP reseller that breaks when the
underlying engine changes. The vendor publishes accuracy-vs-cost benchmarks and its
methodology, which is rare. The trade-off is volume: $5/month is small, and the
free tier's value is concentrated in search, not crawling.

**Gateway role.** Use as the *independent second opinion*: query Brave when Tavily/Exa
return thin results, and compare top-N overlap as a quality signal. Do not use it for
bulk crawls.

---

## 6. The SERP-scraper cluster (ZenRows, Bright Data, ScrapingAnt, HasData, Scrape.do, ScrapingBee, ScraperAPI, Scrapfly, Crawlbase, Zyte, DataForSEO, SerpApi, Zenserp, SerpStack, Serply)

This is where most of the recurring free volume in the inventory sits, and where the
"free tier" definitions differ the most. The table below is the documented free
surface only; paid rates are omitted except where needed to convert credits.

| Provider | Free allowance | Recurring? | Unit | Card | Notes |
|---|---|---|---|---|---|
| ScrapingAnt | 10,000 credits | **yes, monthly** | 1 credit/basic request | no | largest recurring no-card credit pool in the cluster |
| ZenRows | 5,000 credits | **yes, monthly** | 1 standard, 5 JS, 10 premium, 25 protected | no | failed requests not charged |
| Bright Data | 5,000 credits (~$7.50) | **yes, monthly** | 1 credit/request across Unlocker, SERP, Scraper API, Scraper Studio | no | proxies + Browser API excluded; separate $2 trial + $5 card bonus |
| Scrape.do | 1,000 calls | **yes, monthly** | successful API calls | no | residential/mobile proxies + captcha + JS on free plan |
| HasData | 1,000 credits | **yes, monthly** | 1 credit/request | no | |
| ScrapingBee | 1,000 credits | one-time | 1 credit/basic request | no | |
| ScraperAPI | 1,000 credits free plan; 5,000-credit 7-day trial | one-time | 1 credit/request | no | |
| Scrapfly | 1,000 credits | one-time, no expiry | credit/request | no | |
| Crawlbase | "up to 5,000 requests" | one-time to start | 1 credit/standard request | no | one rate card for all products |
| Zyte | $5 credit | one-time, 30-day trial | usage | no | |
| DataForSEO | $1 trial credit | one-time | usage | no | |
| SerpApi | free plan listed; volume not in fetched pages | — | per search | — | cached searches free |
| Zenserp | 50 searches | **yes, monthly** | per search | — | |
| SerpStack | 100 searches | **yes, monthly** | per search | — | non-commercial, JSON only |
| Serply | 2,500 credits | one-time, 30-day expiry | per successful request | no | purchased credits never expire |

**Technical differences that decide the pick.**

1. **What a credit buys.** ZenRows publishes a cost ladder per request class (1/5/10/25),
   so 5,000 credits is not 5,000 hard pages. Bright Data's free credits are shared
   across four products (Unlocker/SERP/Scraper API/Studio) and explicitly exclude
   proxies and Browser API. ScrapingAnt and HasData advertise 1 credit = 1 request,
   which makes their 10k/1k allowances the easiest to plan against.
2. **Which anti-bot tier is included.** Scrape.do's free plan explicitly includes
   residential/mobile proxies, geo-targeting, CAPTCHA handling and JS rendering;
   ScrapingBee/ScraperAPI free credits also cover JS rendering but premium-proxy
   escalation consumes more credits. This is the difference between a free tier that
   works on protected sites and one that only works on static pages.
3. **Failure accounting.** ZenRows does not charge failed requests; Scrape.do bills
   successful calls; Bright Data bills per delivered record/request. For a retry-heavy
   personal gateway, "no charge on failure" is worth more than a larger nominal grant.
4. **Independent measurements.** In the treg leaderboard, SerpApi scores 100% on
   maps/news/youtube tasks (small samples, 791–5,350 runs), DataForSEO 100% on maps and
   news (345k and 56k runs), Serper 89.5% search and 70.8% news. Bright Data, ZenRows
   and ScrapingAnt are not routed by treg, so no independent hit rate is available —
   their claims ("99.9% success") are vendor-stated only.

**Selection logic for a personal gateway.** Start with ZenRows (recurring 5k, no-card,
transparent credit ladder) and Bright Data (recurring 5k, four products, strong
unblocking reputation) as the two free recurring fetch legs; add ScrapingAnt as a third
if the workload is static-page heavy; keep ScrapingBee/Scrapfly/ScraperAPI one-time
credits as burst capacity; use DataForSEO or Serper for SERP JSON rather than scraping
Google yourself.

---

## 7. LLM-native web grounding (Gemini, Perplexity, You.com, Cohere, Groq, Mistral, DeepSeek)

| Provider | Free surface | Documented number | Card |
|---|---|---|---|
| Google Gemini grounding | Grounding with Google Search on the free tier | **5,000 requests/month** shared across Gemini 3+ models, then $14/1k search queries | no |
| Cohere | Trial keys | **1,000 API calls/month**, 20 req/min | no |
| Mistral | Free plan (Vibe/Studio) | limited access, includes search; API free tier rate-limited | no |
| Groq | Free developer tier | rate-limited; Compound models include web search | no |
| Perplexity | no free API tier | per-request: Search $5/1k, fast $1/1k | — |
| You.com | free credits at signup; keyless MCP profile | amount not published in fetched docs | no |
| DeepSeek | no free tier | Search API $0.75/1k searches (community skill measurement) | — |
| OpenAI / Anthropic | no free API credits | web search billed ~$10/1k searches + tokens | — |

**How this class differs.** These are not search APIs; they are *answer* APIs that
perform retrieval internally. A gateway gets one synthesized, cited answer instead of
N URLs, at the cost of control over the retrieval (no reranking, no raw page access,
no crawl). They are best used as a final summarization hop, not as a fetch primitive.

**Gemini is the standout on free volume**: 5,000 grounding requests per month is more
than any other answer-class provider in this inventory except the recurring search
credits above. The catch is that "requests" includes the model call, and free-tier
models are the Flash family; grounding on newer/paid models bills per search query.

**Cohere's trial key** is the sleeper: 1,000 calls/month is small, but the same key
covers chat + embeddings + rerank, and the docs state the limit plainly. For a gateway
that needs a reranker more than a crawler, it is a free quality upgrade.

**Perplexity/You/OpenAI/Anthropic** are technically strong (Perplexity's search API is
the cheapest per-request answer path at $1/1k in fast mode; You.com exposes Search,
Contents, Research and Finance under one key) but there is no recurring free volume to
run a zero-cost gateway on. Treat them as paid fallbacks.

---

## 8. Self-hosted stack (Crawl4AI, SearXNG, Playwright, Trafilatura, MarkItDown, Katana, Firecrawl OSS)

| Tool | Role | Licence / cost | Operational cost |
|---|---|---|---|
| Crawl4AI | LLM-oriented crawl + extract, Markdown output | OSS, self-host | browser install, ~hundreds of MB RAM per concurrent crawl |
| SearXNG | metasearch over 70+ engines | OSS (AGPL) | 1 small service; upstream engines rate-limit/block datacenter IPs |
| Playwright / Puppeteer | raw browser automation | OSS | Chromium download, memory, anti-bot fingerprinting is your problem |
| Trafilatura | boilerplate removal / main-text extraction | OSS | CPU only |
| MarkItDown | documents (PDF/DOCX/PPTX) → Markdown | OSS (MIT) | CPU only |
| Katana | crawling + JS parsing | OSS | Go binary, low overhead |
| Firecrawl (self-host) | API-compatible crawl/search | AGPL-3.0 | browser + queue + storage |
| Steel / Browserless / Skyvern / Maxun | hosted-or-self-hosted browser/scrape | OSS + cloud | same browser costs |

**Economics.** The self-hosted path has no marginal per-call cost but is not free: a
headless Chromium crawl costs roughly 200–500 MB RAM and seconds of CPU per page, and
the hard part of web access (IP reputation, CAPTCHA, fingerprinting) does not go away
— it becomes an operational problem. For a single-user gateway the break-even is
roughly: below a few thousand pages/month, hosted free tiers (ZenRows 5k, Bright Data
5k, ScrapingAnt 10k, Firecrawl 1k, TinyFish search 12k/day) are cheaper in real terms;
above that, self-hosting starts to win, mostly because the free tiers are per-account.

**What each piece is actually good at.**

- **Crawl4AI** is the best OSS drop-in for "give me clean Markdown for these URLs" and
  it ships an llms.txt (20 KB) for agent setup. It has no bot-protection layer of its
  own; the 45.2% fetch success measured for Crawl4AI in the treg leaderboard (1.1M
  calls) is a realistic expectation for a self-hosted crawler on the open web.
- **SearXNG** gives a zero-cost metasearch endpoint, but the same leaderboard shows
  free/metasearch-class results are the weakest at *structured* output; it is best for
  human-facing search, not for grounding a pipeline.
- **Playwright** is the right tool when a page needs interaction (login, form, scroll).
  Budget for a proxy if the target has anti-bot protection; headless Chromium from a
  datacenter IP is blocked by most large sites.
- **Trafilatura + MarkItDown** are the cheap 80% solution for HTML/PDF → text and can
  sit behind any fetch layer; they add no network calls.
- **Firecrawl OSS** is the escape hatch when the cloud free tier's 1,000 credits are
  spent: same API shape, AGPL obligations, and you own the browser fleet.

**Recommended hybrid** (zero marginal spend): SearXNG or Tavily keyless for search →
Jina Reader / Crawl4AI for fetch → Trafilatura/MarkItDown for cleanup → hosted free
credits (ZenRows/Bright Data/ScrapingAnt) only for pages that fail the self-hosted
fetch. The 45%/32% fetch success rates measured for self-hosted-style providers are the
reason the hosted fallback leg is not optional.
