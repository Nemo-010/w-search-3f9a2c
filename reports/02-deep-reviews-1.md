# Deep reviews 1–3: Tavily, Exa, Firecrawl

Evidence base: snapshots fetched 2026-10-19 under `data/snapshots/<slug>/`, plus the
treg Web Arena leaderboard snapshot (`data/snapshots/treg/leaderboard.json`, 30-day
window, updated 2026-10-19T05:43Z). Success-rate numbers from that leaderboard are
independent of the vendors' own claims; where both exist they are labelled.

---

## 1. Tavily

| | |
|---|---|
| Home | https://tavily.com/ |
| Docs / llms.txt | https://docs.tavily.com/ · https://docs.tavily.com/llms.txt |
| Free tier | **1,000 credits/month**, resets monthly, no card (docs, verbatim below) |
| Keyless | Search + Extract free without an account, rate-limited per IP |
| Paid | credit packs / pay-as-you-go; Advanced Search also payable per request in USDC (x402) |
| Measured (treg) | search 87.2% success on 2,865 runs; fetch 75.1% on 12,763 runs; papers 98% |
| Endpoints | Search, Extract, Map, Crawl, Research |

**Free-tier mechanics.** The docs state: "Get a free API key at https://app.tavily.com
(1,000 credits/month, no credit card required)." Credits are per basic operation
(1 credit ≈ 1 basic search or 1 page extracted); advanced/deep options and research
mode cost more per call, so the *effective* call count for non-basic usage is below
1,000. The keyless path matters for a gateway: Search and Extract work with no key at
all, so the 1,000-credit allowance is only consumed once the keyless per-IP cap is
hit (`docs.tavily.com/documentation/keyless`).

**Integration surface.** Tavily is the most "agent-shaped" of the three: CLI
(`tavily-cli`, `tvly login`), hosted MCP endpoint (`https://docs.tavily.com/mcp` for
documentation; the product API is exposed through `app.tavily.com`), and docs that
ship per-page Markdown (`.md` suffix) plus `llms-full.txt`. Output is JSON with
`answer`, `results[]` and per-result `content` suitable for direct LLM context.

**Fit for a personal fetch/search gateway.** Best first hop for *search-plus-answer*:
one call returns ranked results plus optionally synthesized content, which removes a
second fetch for many queries. Weaknesses to design around: (a) credit costs are not
flat across operations, so a naive "credits = calls" budget overestimates the monthly
volume; (b) it is a reseller-class index — when Tavily misses, the failure mode is a
thin/empty result set rather than a 403, so a gateway should chain to a second
provider; (c) research mode can spend the whole free allowance in a handful of calls.

---

## 2. Exa

| | |
|---|---|
| Home | https://exa.ai/ |
| Docs / llms.txt | https://docs.exa.ai/ · https://exa.ai/docs/llms.txt |
| Free tier | **$10 credits every month + $10 onboarding bonus**, no payment method required |
| Paid | Instant Search $4/1k, Fast/Auto $7/1k, Deep $12/1k, Deep-Reasoning $15/1k; Contents $1/1k pages |
| Measured (treg) | search 98.1% success on 125,076 runs; fetch 89.1% on 116,634 runs; papers 100% on 497 |
| Startup/edu | up to $1,000 credits |
| Endpoints | Search (+deep), Contents, Similar, Answer, Agent, Monitors, Websets |

**Free-tier mechanics.** The pricing page states: "Free $10 credits every month plus a
$10 onboarding bonus. No payment method required." At the cheapest endpoint
(Instant, $4/1k) the recurring grant is worth ~2,500 searches/month, but the free
tier's rate limit is 10 search QPS with 50 agent concurrency — high enough for
interactive use, too low for bulk sweeps. Deep/agent tiers convert the same $10 to
fewer calls (Deep-Reasoning at $15/1k ⇒ ~666 calls).

**Why it matters in this inventory.** Exa is the only major provider whose monthly
grant is denominated in USD rather than credits, which makes the effective volume
transparent and lets a gateway price a mixed workload (search + contents + monitors)
from one balance. Independent measurements put its search success at the top of the
tracked set (98.1% on 125k runs) while its fetch path is also strong (89.1%). The
`extracts` feature returns structured fields (e.g. company/people) from the same call,
which is useful for a personal gateway that wants JSON facts rather than raw pages.

**Caveats.** $10/month is a small absolute budget: a single Deep-Reasoning research
run can cost ~$0.015, and Agent runs are ACU-metered with contact enrichment billed
separately. Contents is billed per page and per content type, so `text + highlights +
summary` on one page can triple the per-page charge. Treat Exa as the quality search
leg, not the crawl leg.

---

## 3. Firecrawl

| | |
|---|---|
| Home | https://www.firecrawl.dev/ |
| Docs / llms.txt | https://docs.firecrawl.dev/ · https://docs.firecrawl.dev/llms.txt |
| Free tier | **1,000 credits/month**, resets monthly, no card, 2 concurrent browsers |
| Keyless | Scrape, Search, Interact work with no API key (per-IP daily cap) |
| Paid | Hobby 5k credits, Standard 100k ($83/mo), Growth 500k, Scale 1M |
| Measured (treg) | search 99.8% success on 9,604 runs; fetch **32.2%** on 148,814 runs; sitemap 100% |
| Extras | self-hostable (AGPL-3.0), MCP server, CLI, Agent endpoint (5 free runs/day) |

**Free-tier mechanics.** `docs.firecrawl.dev/billing.md`: "**1,000 credits per
month.** The allotment resets at the start of each monthly cycle. Unused free credits
do not roll over." Credit costs are per endpoint and option: scrape/crawl 1/page, map
1/call, search 2 per 10 results, JSON extraction +4/page, PDF parsing +1/page, browser
sandbox 2–7 credits/minute. The same page documents the failure semantics that matter
for a gateway: on the free plan there is no pay-as-you-go, so once the monthly
allotment is spent every request returns HTTP 402 ("Running Out of Credits"). That is
a clean signal for a router to switch providers.

**The 32% fetch number.** The leaderboard's fetch column is the one result in this
inventory that contradicts vendor marketing most sharply: Firecrawl scored 99.8% on
search but 32.2% on page fetch over 148,814 routed calls, at a median 1,661 ms. This
is not a claim that Firecrawl cannot scrape — it is a statement that in treg's routed
workload (which includes provider fallback ordering), Firecrawl's fetch was frequently
the *miss* that another vendor covered. A gateway should therefore treat Firecrawl's
scrape path as best-effort and chain it (its `/search` + scrape in one call is the
strong path), rather than as the only fetch leg. The `search` endpoint's combination
of search + optional scraping is where the credit math is best: 2 credits per 10
results plus 1 per scraped page.

**Keyless + self-host.** Firecrawl is the only one of the three with an AGPL
self-hosted option, which is the escape hatch if the cloud allowance is exhausted:
same `/v2` API shape, no per-call cost, at the price of running the crawler (and its
browser dependencies) yourself. The cloud free tier also supports a keyless path with
a per-IP daily cap, so a gateway can keep some functionality at zero marginal cost.

---

## Cross-cutting conclusion for these three

- **Recurring free volume**: Exa $20 first month/$10 after; Tavily 1,000 credits;
  Firecrawl 1,000 credits. All three are enough for interactive personal use, none is
  enough for unattended crawling.
- **Independent reliability**: Exa is the only one of the three measured above 89% on
  *both* search and fetch. Tavily's fetch measured 75.1%; Firecrawl's 32.2%.
- **Failure modes**: Tavily degrades to empty results, Firecrawl returns HTTP 402 at
  the allowance boundary, Exa bills per unit and simply stops when the balance is
  exhausted. A router should treat 402/429 as routing signals and empty results as a
  quality signal.
- **Combination** for a personal gateway with zero marginal spend: Tavily keyless →
  Exa $10/month search → Firecrawl keyless scrape → Bright Data/ZenRows recurring
  credits → ZenRows/Bright Data as paid fallback.
