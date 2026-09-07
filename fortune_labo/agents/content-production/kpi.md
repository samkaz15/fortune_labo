# Content Production Agent — KPI Structure

## Design principle

The obvious KPI for a writing agent is **throughput** — drafts produced, words
written, turnaround time. Optimising throughput on a pipeline whose supply is
bounded by human shrine visits produces exactly one behaviour: writing sections
whose source material does not exist.

**A08 is measured on trustworthiness first, reader outcome second, and speed
last.**

---

## KGI

> Inherited: **organic-sourced booked readings** (`../seo/kpi.md`).

A08 does not get an independent success definition. A draft that reads beautifully
and produces no booking has not succeeded.

---

## Tier 1 — Trustworthiness (gating; no other tier counts if this fails)

| KPI | Definition | Target |
| --- | --- | --- |
| `fabrication_incidents` | Claims published without a resolvable source | **= 0. Non-negotiable.** |
| `source_traceability_rate` | First-hand sections with a valid `source_map` entry / all first-hand sections | **= 1.0** |
| `attribution_marking_rate` | Judgments carrying an attribution marker / all judgments | **= 1.0** |
| `compliance_blocking_findings` | Blocking findings from A30 per draft | **= 0** |
| `gap_reported_rate` | Missing-source sections reported as gaps / all missing-source sections | **= 1.0** |

`gap_reported_rate` is the inverse of the failure mode. A month with zero gap
reports across many first-hand pieces is **suspicious, not excellent** — it
suggests gaps are being written around rather than reported.

A single `fabrication_incident` outranks every other metric in this document.

---

## Tier 2 — Reader outcome

| KPI | Definition | Direction | Phase |
| --- | --- | --- | --- |
| `cta_click_rate` | Primary CTA clicks / page sessions | ↑ | 2 |
| `booking_attributed_drafts` | Published drafts producing ≥1 attributed booking | ↑ | 3 |
| `scroll_completion` | Sessions reaching the CTA region | ↑ | 2 |
| `engaged_session_rate` | GA4 engaged sessions / sessions | ↑ | 2 |
| `snippet_capture_rate` | Snippet-targeted sections that won the position | ↑ | 2 |
| `answer_in_lead_rate` | Drafts where the query's answer appears in the lead | **= 1.0 where a short answer exists** | 1 |

---

## Tier 3 — Craft and throughput (diagnostics only)

Never reported as achievement on their own.

| KPI | What it actually measures |
| --- | --- |
| `qa_findings_per_draft` | Self-check effectiveness |
| `blocking_findings_per_draft` | Rule internalisation — should trend to zero |
| `revision_count_per_draft` | Target ≤ 2; a 3rd revision means the brief was defective |
| `structure_deviation_rate` | Brief–reality mismatch (may indicate an A07 problem) |
| `seo_conflict_rate` | How often SEO requirements fight the reader |
| `brief_returned_rate` | Briefs A08 sent back as unexecutable |
| `median_draft_turnaround_days` | Speed. **Last, deliberately.** |
| `word_count` | **Not a KPI.** Listed only to state it is not one. |

---

## Forbidden framings

A08 must not report, and A07 / A01 must not accept:

- Word count or article count as achievement
- Turnaround speed as a headline result
- "Comprehensive coverage" without a reader-outcome metric
- Keyword density or keyword count of any kind
- Any Tier 2 or Tier 3 movement while a Tier 1 metric is failing

---

## Diagnostic matrix

| Pattern | Likely cause | Owner |
| --- | --- | --- |
| Ranks well, no CTA clicks | Body never answers the actual question | **A08** |
| High bounce from the lead | Lead defers the answer | **A08** |
| Repeated compliance findings on the same expression | Rule not internalised | **A08** → A30 |
| QA finds an unsourced claim | Self-check step 2 skipped | **A08** — most serious |
| Zero gap reports on first-hand-heavy months | Gaps being written around | **A08** — investigate immediately |
| Repeated `structure_deviation` on similar briefs | Briefs systematically unexecutable | A07 |
| Repeated `seo_conflict` on similar requirements | SEO requirement is wrong | A06 |
| 3rd revision reached | Defective brief | A07 |
| Draft blocked on material for weeks | Visit or judgment not happening | Human → A01 |
