# Raw Performance Schema

Version: raw-metrics-1.0.0. No performance provider is connected by this change. [performance_observation.schema.json](schemas/performance_observation.schema.json) and `fortune_labo/editorial/performance.py` define observations ready for later ingestion. Missing metrics are null; an observed zero remains zero. No total score, weighting, benchmark, or automatic success label is calculated.

Each observation is keyed by content ID, source, period, timezone, dimensions, filters and definition version. Sources are `Search Console`, `GA4`, `WordPress`, and `SNS`. Retain the source reference, collection time, sampling/thresholding notes and per-metric source key, definition, aggregation, unit, numerator and denominator. Store providers separately; rows with differing filters, periods or definitions must not be merged as interchangeable evidence. Private property/account IDs, URLs and raw exports stay in private storage.

| Group | Raw metric | Unit / meaning to confirm at connection |
| --- | --- | --- |
| SEO | impressions, clicks | Nonnegative integer counts in the source report. |
| SEO | ctr | Source-reported ratio 0–1; retain click/impression denominators where available. |
| SEO | average_position | Nonnegative source-reported position; retain scope and aggregation. |
| Engagement | users, sessions, engaged_sessions | Nonnegative integer counts; the exact user definition must be recorded. |
| Engagement | engagement_rate | Ratio 0–1 with the source's numerator/denominator definition. |
| Engagement | average_engagement_time | Seconds; specify whether per user/session and the exact source metric. |
| Engagement | scroll_depth | Percent 0–100; specify threshold, maximum or average and collection method. A scroll event count is not automatically scroll depth. |
| Conversion | fortune_cta_clicks, fortune_start, fortune_complete, member_registration, premium_conversion | Raw event/conversion counts with exact event names, deduplication and attribution definitions. |
| Retention | returning_users, repeat_article_views | Counts with repeat/user/content/window definitions; do not substitute page views. |

`empty_observation(...)` initializes all 17 metrics to null. `validate_observation` rejects reversed periods, negative/nonfinite values, boolean counts, invalid ratios, extra score fields, and observed metrics missing collection/provenance/definition data. The JSON schema requires all metric keys and rejects additional top-level and metric properties. Period ends are inclusive; compare like periods and document reporting timezone.

No automatic adapter guesses the meaning of provider fields. At connection time, approve event contracts, access, consent, attribution windows and dimensional filters, then preserve source values. Aggregated ratios must be recomputed from compatible denominators or retained as source report observations; do not average daily CTR/engagement rates. A07 may read separate raw observations as evidence but must not invent an overall 100-point score or weights.

## A07 feedback adapter

`performance_context(observations, content_id=..., period_start=..., period_end=..., timezone=..., filters={}, dimensions={})` validates flat source observations and projects them into A07's `seo`, `engagement`, `conversion`, and `retention` groups. Supply `build_brief(..., performance={"observations": [...], "selection": {"period_start": "2026-01-01", "period_end": "2026-01-31", "timezone": "UTC", "filters": {}, "dimensions": {}}})`. The example period is illustrative; no real data has been collected.

The adapter requires the same content ID, exact selected period, timezone, filters, dimensions and definition version. It rejects mixed periods or scopes and rejects two providers reporting the same metric even when their values match. Select the provider/scope explicitly upstream instead of combining ambiguous counts. Data from providers with incompatible reporting timezones or filters must be inspected as separate contexts; this adapter does not silently normalize them.

Every grouped value retains the full source record under `raw_observations`, including metric definition, unit, source reference, collection time, filters and quality notes. Source references become A07 evidence references. Observed zero remains observed; absent values remain null. `scroll_depth: 75` remains 75 percent. No computation, averaging, numerical prioritization or performance score is introduced. A07's legacy grouped input is reserved for empty/unmeasured placeholders; measured feedback must use the raw observation contract.
