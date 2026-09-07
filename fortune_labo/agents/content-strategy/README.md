# A07 — Content Strategy Agent

Decides **what content fortune_labo should produce, for whom, and why.**

> **Read [`agents/seo/positioning.md`](../seo/positioning.md) first.**
> Content Strategy Agent inherits every constraint in that file. Where standard
> content-marketing practice conflicts with it, positioning wins.

## What this agent is

**Editor-in-Chief / Content Planner.** It converts *search demand* into an
*editorial decision*. It does not write body copy and it does not implement.

```
              A06 SEO Agent
                    │  seo_opportunity.json  (+ SEO requirement set)
                    ▼
        ┌───────────────────────┐
        │ A07 CONTENT STRATEGY  │  theme · persona · angle · outline · CTA
        └───────────┬───────────┘
                    │  content_brief.json   (CB-xxxx)
                    ▼
          A08 Content Production
                    │  master_content.json
                    ▼
             A10 SNS Content
                    │
                    ▼
        A28 QA  ◄── A30 Compliance/Risk
                    ▼
             HUMAN APPROVAL
                    ▼
              WordPress / SNS
                    ▼
               Analytics ──► A06
```

## The decision this agent owns

SEO Agent says *"there is demand here and we could win it."*
Content Strategy Agent answers three questions SEO Agent is not allowed to
answer alone:

1. **Should we build this at all?** (`build` / `rewrite` / `consolidate` / `decline`)
2. **Who is it for, and what state are they in when they search?**
3. **What is the one thing this page gives them that nothing else on the SERP does?**

A brief that cannot answer (3) is not issued. Declining is a valid output and is
recorded, not silently dropped.

## New vs rewrite

Every opportunity is triaged against the existing site before a new URL is
proposed. The default is **rewrite an existing page**, not publish a new one.
Page-count growth is explicitly not progress (`agents/seo/kpi.md`).

## Files

| File | Purpose |
| --- | --- |
| [`mission.md`](./mission.md) | Mission, scope, non-goals |
| [`responsibilities.md`](./responsibilities.md) | Theme, persona, intent, angle, outline, CTA, internal links, priority, rewrite triage |
| [`inputs.md`](./inputs.md) | What A06 and others must supply |
| [`outputs.md`](./outputs.md) | Content Brief, Editorial Calendar, Decline Record |
| [`workflow.md`](./workflow.md) | The 9-step decision loop and cadence |
| [`rules.md`](./rules.md) | Binding rules. Violations are blocking at QA |
| [`kpi.md`](./kpi.md) | Brief-level and portfolio-level KPIs |
| [`prompts/`](./prompts/) | System prompt + task prompts |
| [`schemas/`](./schemas/) | `content_brief`, `editorial_calendar`, `decline_record` |

## Handoff contract

| Direction | Artifact | Schema |
| --- | --- | --- |
| A06 → A07 | SEO Opportunity | [`../seo/schemas/seo_opportunity.schema.json`](../seo/schemas/seo_opportunity.schema.json) |
| A06 → A07 | SEO requirement set | [`../seo/schemas/content_brief.schema.json`](../seo/schemas/content_brief.schema.json) |
| A07 → A08 | **Content Brief** | [`schemas/content_brief.schema.json`](./schemas/content_brief.schema.json) |
| A07 → A10 | `sns_repurpose` block inside the Content Brief | same file |
| A07 → Strategy (A01) | Decline Record / capacity escalation | [`schemas/decline_record.schema.json`](./schemas/decline_record.schema.json) |

See [`../../../docs/agents/CONTENT-PIPELINE.md`](../../../docs/agents/CONTENT-PIPELINE.md)
for the full end-to-end artifact chain and for the relationship between the two
files both named `content_brief.schema.json`.
