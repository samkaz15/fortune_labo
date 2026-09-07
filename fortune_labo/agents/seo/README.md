# SEO Agent

SEO strategy, analysis, and prioritisation for fortune_labo.

> **Start with [`positioning.md`](./positioning.md).** It constrains everything
> else in this directory and overrides standard SEO practice where they conflict.

## What this agent is

**SEO Manager / Strategist.** Decides what should change and why.
Does not write content, does not write code, does not collect raw data.

```
              Strategy Agent          business priority
                    │
              Research Agent          market / competitor / demand
                    │
              ┌─────▼─────┐
              │ SEO AGENT │           analysis · judgment · prioritisation
              └─────┬─────┘
       ┌────────────┼────────────┬──────────────┐
       ▼            ▼            ▼              ▼
  Visit Plan   A07 Content    Codex        CRO Agent
   (human)      Strategy         │              │
       │            │            │              │
       │      A08 Production     │              │
       │            │            │              │
       │      A10 SNS Content    │              │
       │            │            │              │
       └────────────┴─────┬──────┴──────────────┘
                          ▼
                    A28 QA Agent  ◄── A30 Compliance/Risk
              (compliance → factual → first-hand
               → editorial → SEO → technical)
                          ▼
                   HUMAN APPROVAL
                          ▼
                      WordPress
                          ▼
                    User Traffic
                          ▼
                  Analytics Agent
                          ▼
                     SEO Agent  ──► PDCA
```

## Files

| File | Purpose |
| --- | --- |
| [`positioning.md`](./positioning.md) | **Read first.** Why SEO here is demand capture, not traffic. Keyword tiers. Anti-goals. |
| [`mission.md`](./mission.md) | Mission, scope, non-goals |
| [`responsibilities.md`](./responsibilities.md) | Keyword strategy, SERP, competitor, content, internal links, technical, visit planning |
| [`kpi.md`](./kpi.md) | Three-tier KPI structure. Bookings at the top, traffic at the bottom |
| [`inputs.md`](./inputs.md) | Data sources and phase availability |
| [`outputs.md`](./outputs.md) | Artifacts, handoff contracts, report format |
| [`workflow.md`](./workflow.md) | PDCA loop, daily/weekly/monthly/quarterly/annual cadence, seasonal backward planning |
| [`rules.md`](./rules.md) | Hard rules: positioning, first-hand, subjectivity, compliance, operating |
| [`integrations.md`](./integrations.md) | GSC, GA4, WordPress, Codex — read-only by design |
| `prompts/` | `_system.md` plus one prompt per task |
| `schemas/` | Six JSON Schemas defining all agent-to-agent handoffs |

## Design decisions worth knowing

**1. Traffic is a Tier 3 diagnostic, not a goal.**
Yano Research (2023 FY) found five of six fortune-telling segments growing; the
only flat one was "Web fortune-telling (apps/SNS)" — the segment with no human
involved. Generative AI has commoditised exactly the content a traffic-optimising
SEO agent gravitates toward. Traffic and business value are decoupled here.

**2. `moat_alignment` is a required field on every output.**
An agent cannot emit a recommendation that trades the moat for traffic without it
being machine-visible. `conflicting` forces escalation to Strategy Agent.

**3. Visit plans, not content briefs, are the primary content artifact.**
Tier A supply is bounded by human physical visits, not AI capacity. SEO Agent
schedules the human, then briefs the writer — never the reverse.

**4. `firsthand_content_ratio` is a P0 alert metric.**
If it falls while traffic rises, the site is drifting to commodity content and
the business is being hollowed out. This is treated as a failure, not a tradeoff.

**5. `branded_search_volume` is the primary authority metric.**
When people search the practitioner's name instead of the topic, the standing
strategy is working. It is the best available proxy for the stated business goal.

**6. Compliance ranks above SEO in the QA gate order.**
Japan tightened spiritual-claim solicitation rules in 2022–2023, with rescission
windows extended to 3 years from realisation / 10 years from the act, exercisable
by family members through subrogation. SEO Agent owns titles and meta
descriptions, so title compliance is SEO Agent's responsibility.

## Implementation phasing

### Now (Phase 1) — no external API required

- [x] Specification (this directory)
- [ ] Keyword register seeded from client questions + shrine calendars
- [ ] Tier classification of all existing pages
- [ ] Baseline `firsthand_content_ratio`
- [ ] Manual SERP analysis on top 20 Tier A/B keywords
- [ ] First 90-day visit plan
- [ ] Technical audit → Codex specs (`Person` / `LocalBusiness` schema first)
- [ ] Internal link graph map + booking-page inbound audit
- [ ] Seasonal calendar for the next 12 months

**Phase 1 is fully operational.** SEO Agent is not blocked on API access.

### Phase 2 — read APIs

- [ ] GSC Search Analytics (Analytics Agent fetches, caches to `data/`)
- [ ] GA4 Data API
- [ ] WordPress REST read access
- [ ] Daily alerting, weekly analysis loop automated

### Phase 3 — attribution and write path

- [ ] Booking events (`booking_complete`) instrumented
- [ ] Organic first-touch attribution
- [ ] Tier 1 KPIs measurable — **prioritisation is proxy-based until this lands,
      and every report must say so**
- [ ] Codex write path with dry-run

### Always requires human approval

- Any production publish
- Any WordPress write
- Visit plans
- Bulk operations (20+ URLs)
- Anything with a non-empty `compliance_flags`
- Any `moat_alignment: conflicting` escalation

## Consistency with `/AGENTS.md`

| Repository rule | How this directory enforces it |
| --- | --- |
| No autonomous publishing | `workflow.md`; SEO Agent holds no write credentials by design |
| Do not invent business facts | `rules.md` §2 extends this to first-hand experience |
| Use evidence for decisions | `evidence` + `evidence_confidence` required on every output |
| Update hypotheses, not evidence | `outcome.hypothesis_update`; mandatory hypothesis ledger in reports |
| Small reviewable changes | Every artifact is a discrete schema-conforming unit |
| Secrets out of Git | `integrations.md` |
| WordPress writes authenticated and scoped | `integrations.md`; Codex only |
| Dry-run where practical | Enforced in schema for 20+ URL operations |
