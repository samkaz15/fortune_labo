# Prompt — Visit Planning

## Task
Convert search demand into a physical shrine visit schedule.

This is your highest-leverage artifact. Tier A content cannot be scaled by adding
AI capacity — it is bounded by how many shrines a human can actually visit.

## Inputs
Seasonal calendar, Tier A keyword gaps, competitor coverage, travel feasibility,
**practitioner's stated available visit days**.

## Constraints

1. **Never plan beyond stated capacity.** If demand exceeds it, set
   `capacity_warning` and escalate to the human. Do not silently drop targets —
   record them in `deferred` with a reason.
2. **Plan backward from the seasonal window**, not forward from today.

```
Demand opens        →  publish 4 weeks earlier
Publish             →  QA + approval 2 weeks earlier
Approval            →  draft 2 weeks earlier
Draft               →  brief 1 week earlier
Brief               →  VISIT 2–4 weeks earlier
```

A visit plan issued in November for 初詣 has already failed.

3. **Cluster geographically.** Group nearby shrines into one trip to raise output
   per visit day.

## Seasonal windows

| Window | Publish by |
| --- | --- |
| 初詣 / 年始 | early November |
| 節分・立春 | early January |
| 七五三 | early September |
| 大祓 (6月/12月) | ~6 weeks prior |
| Annual outlook (翌年) | late October |

## Capture requirements
For each visit, specify what the practitioner must record: atmosphere notes,
specific photographs needed, and **practitioner judgment prompts** — questions
only they can answer, e.g. "how does this shrine read for 2027 under your system,
and on what basis". Always include the photo permission check.

## Output
`schemas/visit_plan.schema.json`.
