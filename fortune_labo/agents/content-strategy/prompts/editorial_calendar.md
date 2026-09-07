# Prompt — Editorial Calendar Planning

## Task
Maintain a rolling 90-day editorial calendar that never exceeds the
practitioner's stated capacity.

## Step 1 — Establish capacity (not optional)

From the practitioner's stated monthly availability:

```
visits_per_month            physical shrine visits possible
judgment_sessions           divinatory work for outlooks / reflections
review_hours                approval and correction time
```

Capacity cost per brief:

| Content type | Visit | Judgment | Review |
| --- | --- | --- | --- |
| `shrine_visit_report` | 1 | 0 | high |
| `annual_outlook` | 0 | high | high |
| `forecast_review` | 0 | medium | high |
| `case_reflection` | 0 | medium | high |
| `method_explainer` | 0 | low | medium |
| `situation_guide` | 0 | low | medium |
| `service_page`, `hub_page`, `faq_page` | 0 | 0 | medium |

## Step 2 — Place seasonal work first

Seasonal windows are immovable. Work backward (`../workflow.md`):

```
window opens → publish (−4w) → approval (−2w) → QA + compliance (−1w)
  → SNS adaptation (−1w) → draft (−2w) → BRIEF (−1w) → visit (−2..4w)
```

Known windows: 初詣 (publish early Nov), 節分・立春 (early Jan), 七五三
(early Sep), 大祓 6月/12月 (~6 weeks prior), annual outlook (late Oct).

**A seasonal slot that cannot be met is escalated now, not discovered later.**
A missed window costs a full year.

## Step 3 — Fill remaining capacity by priority

Order by A06 priority, adjusted by editorial readiness (source material present,
cluster hub live). Never fill a slot whose source material is blocked — park it
and record the blocker.

## Step 4 — Check the portfolio, not just the slots

- Would this month's mix lower `firsthand_brief_ratio`? → **P0 escalation to A01**
- Are there spokes scheduled whose hub is not live? → resequence
- Is `rewrite_share` below 0.4? → replace a `build_new` with a rewrite
- Is any cluster receiving nothing for a full quarter? → deliberate or drift?

## Step 5 — Publish the calendar

If committed capacity exceeds stated capacity, **do not publish the calendar as
a plan.** Publish it as an escalation to A01 Strategy Agent with a proposed cut
list, ordered by lowest expected booking impact.

## Output
`schemas/editorial_calendar.schema.json`.
