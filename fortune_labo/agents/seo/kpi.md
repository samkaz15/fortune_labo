# SEO Agent — KPI Structure

## Design principle

Standard SEO KPI stacks put Organic Traffic at the top. **That is wrong for this
business** (see `positioning.md` §2 and §4). Traffic sits in the lowest tier
here — it is a diagnostic, never a goal.

---

## KGI

> **Organic-sourced booked readings per month.**

A reading booked by a visitor whose first session was organic search.
Secondary KGI: **Organic-sourced revenue** (bookings x realised price).

---

## Tier 1 — Business outcome (the only tier that defines success)

| KPI | Definition | Why |
| --- | --- | --- |
| `organic_bookings` | Bookings attributed to organic first-touch | KGI |
| `organic_revenue` | Revenue from those bookings | KGI |
| `organic_booking_cvr` | Bookings / organic sessions | Efficiency of the funnel |
| `organic_list_signups` | LINE / email registrations from organic | Deferred conversion path |
| `repeat_rate_organic` | Repeat bookings from organic-acquired clients | LTV signal |

**If Tier 1 is flat, no Tier 2 or Tier 3 improvement counts as success.**

---

## Tier 2 — Moat and authority (leading indicators)

These are specific to this business and are the reason it is defensible.

| KPI | Definition | Target direction |
| --- | --- | --- |
| `branded_search_volume` | Impressions on practitioner-name queries | **↑ — primary authority metric** |
| `branded_search_ratio` | Branded / total impressions | ↑ |
| `firsthand_content_ratio` | Pages backed by an actual human visit / total indexed pages | **≥ 0.6, never falling** |
| `tier_a_coverage` | Tier A keywords ranked top 10 / Tier A keywords targeted | ↑ |
| `shrine_pages_published` | Visit-backed shrine pages live | ↑ |
| `seasonal_hit_rate` | Seasonal pages published before their window opened | **= 1.0** |
| `annual_forecast_review_published` | Prior-year forecast publicly reviewed | Boolean, yearly |

`branded_search_volume` is the single best proxy for the stated business goal of
*establishing standing as a named practitioner*. When people search the name
rather than the topic, the strategy is working.

`firsthand_content_ratio` is a **moat guard**. If it falls, the site is drifting
toward commodity content even if traffic is rising. A falling ratio is a
**P0 alert regardless of traffic performance.**

---

## Tier 3 — Search performance (diagnostics only)

Standard metrics. Used to explain Tier 1 and Tier 2 movement. **Never reported
as achievements on their own.**

| KPI | Source |
| --- | --- |
| `clicks`, `impressions`, `ctr`, `avg_position` | GSC |
| `indexed_pages`, `coverage_errors` | GSC |
| `non_brand_clicks` | GSC (derived) |
| `orphan_pages`, `internal_link_depth` | Crawl |
| `cwv_lcp`, `cwv_inp`, `cwv_cls` | GSC / PSI |
| `thin_pages`, `duplicate_clusters` | Crawl |

---

## Forbidden framings

SEO Agent must not report, and Strategy Agent must not accept:

- "Traffic grew X%" as a standalone result
- Ranking improvements on Tier D keywords
- Impressions growth without a Tier 1 or Tier 2 movement attached
- Page-count growth as progress

Every SEO report must open with Tier 1, then Tier 2, then Tier 3. Never the
reverse order.

---

## Diagnostic matrix

Mapping observed patterns to owning agent. Used by the weekly loop.

| Pattern | Likely cause | Owner |
| --- | --- | --- |
| Impressions ↑, clicks flat | Title/meta mismatch with intent | SEO → Content |
| Clicks ↑, bookings flat | Wrong intent, or booking CTA weak | SEO → CRO |
| Position ↓ on Tier A page | Content staleness / competitor entry | SEO → Content (revisit?) |
| Not indexed | Technical | SEO → Codex |
| Traffic ↑, `firsthand_content_ratio` ↓ | **Moat erosion — P0** | SEO → Strategy |
| Branded search flat while non-brand ↑ | Content is ranking but not building the name | SEO → Strategy |
| Seasonal page published late | Calendar failure | SEO (own failure) |
