# Content Strategy Agent — KPI Structure

## Design principle

The obvious KPI for an editorial function is **output** — briefs issued, articles
published, calendar filled. That is wrong here for the same reason traffic is
wrong for A06 (`../seo/positioning.md` §4): output is bounded by the
practitioner's physical capacity, so maximising it can only be achieved by
lowering the bar.

**A07 is measured on the quality of its decisions, not the quantity of them.**

---

## KGI

> **Share of published content that produces a booking-relevant outcome.**

Inherited from A06's KGI (`organic_bookings`). A07 does not get its own success
definition — that would let editorial "succeed" while the business does not.

---

## Tier 1 — Decision quality

| KPI | Definition | Target |
| --- | --- | --- |
| `brief_to_booking_rate` | Briefs whose published page produced ≥1 attributed booking / briefs published | ↑ (Phase 3) |
| `brief_conversion_proxy` | Briefs whose page produced ≥1 `list_signup` or booking CTA click / briefs published | ↑ (Phase 2) |
| `decline_rate` | Declined opportunities / opportunities received | **0.3–0.6 is healthy** |
| `decline_reversal_rate` | Declines later re-opened and shown to have been valuable / total declines | ↓ |
| `rewrite_share` | `rewrite`+`consolidate` decisions / all build decisions | **≥ 0.4** |

`decline_rate` is a two-sided KPI. Near zero means A07 is rubber-stamping A06 and
adding no editorial judgment. Near one means it is not finding anything to build.
Both are failures.

`rewrite_share ≥ 0.4` operationalises the rule that page-count growth is not
progress.

---

## Tier 2 — Moat and portfolio health

| KPI | Definition | Target |
| --- | --- | --- |
| `firsthand_brief_ratio` | Briefs requiring a visit or practitioner judgment / all briefs | **≥ 0.6, never falling** |
| `one_line_test_pass_rate` | Briefs with a recorded, defensible `differentiation_basis` | **= 1.0** |
| `cluster_completeness` | Clusters with a live hub and ≥3 spokes / total clusters | ↑ |
| `orphan_brief_count` | Briefs issued with <1 planned inbound link | **= 0** |
| `seasonal_lead_time_hit_rate` | Briefs issued on or before their backward-planned date | **= 1.0** |
| `capacity_overcommit_events` | Months where committed capacity exceeded stated capacity | **= 0** |

A falling `firsthand_brief_ratio` is a **P0 alert regardless of traffic**, matching
A06's `firsthand_content_ratio` guard.

---

## Tier 3 — Throughput (diagnostics only)

Never reported as achievement on their own.

| KPI |
| --- |
| `briefs_issued` |
| `briefs_blocked_on_material` |
| `median_brief_to_draft_days` |
| `brief_rework_rate` (A08 returned the brief as unachievable) |
| `qa_rejection_rate_traceable_to_brief` |
| `sns_repurpose_skip_rate` |

`brief_rework_rate` and `qa_rejection_rate_traceable_to_brief` measure A07's
craft: a brief that A08 cannot execute or that QA rejects for an ambiguity was a
defective brief, and the fault is A07's.

---

## Forbidden framings

A07 must not report, and A01 must not accept:

- "N briefs issued this month" as a result
- "The calendar is full" as a result
- Publication count growth as progress
- Any Tier 3 movement without a Tier 1 or Tier 2 movement attached

Every A07 report opens with Tier 1, then Tier 2, then Tier 3.

---

## Diagnostic matrix

| Pattern | Likely cause | Owner |
| --- | --- | --- |
| Ranks well, no CTA clicks | Content intent mismatched to search intent | A07 (own failure) |
| A08 repeatedly flags briefs unachievable | Source-material check being skipped | A07 (own failure) |
| QA rejects for ambiguity | Outline `purpose` fields too vague | A07 (own failure) |
| QA rejects for compliance in title | A07 title screening failed | A07 (own failure) → A30 |
| Published page is an orphan | Inbound links planned but never implemented | A06 → Codex |
| High `decline_rate` and falling opportunity quality | A06 upstream drift | A06 |
| Cluster has spokes, no hub | Sequencing error in the calendar | A07 (own failure) |
| `firsthand_brief_ratio` falling while briefs rise | **Moat erosion — P0** | A07 → A01 Strategy |
