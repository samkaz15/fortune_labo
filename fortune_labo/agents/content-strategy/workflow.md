# Content Strategy Agent — Workflow

## Position in the pipeline

```
A06 SEO Agent
     │  seo_opportunity.json  ·  seo content_brief.json  ·  visit_plan.json
     ▼
┌──────────────────────────────────────────────┐
│ A07 CONTENT STRATEGY AGENT                   │
│                                              │
│  1 intake        accept / reject the input   │
│  2 triage        build / rewrite / decline   │
│  3 source check  does the material exist?    │
│  4 audience      persona + reader state      │
│  5 purpose       content intent + value      │
│  6 angle         unique value + one-line test│
│  7 structure     titles + H2/H3 outline      │
│  8 distribution  CTA + links + SNS decision  │
│  9 commit        capacity check + calendar   │
└──────────────────┬───────────────────────────┘
                   │  content_brief.json (CB-xxxx)
                   ▼
        A08 Content Production ──► master_content.json
                   ▼
            A10 SNS Content   ──► channel_content.json
                   ▼
                A28 QA  ◄──── A30 Compliance/Risk
                   ▼
             HUMAN APPROVAL     (mandatory, /AGENTS.md)
                   ▼
             WordPress / SNS
                   ▼
              A18 Analytics
                   ▼
              A06 SEO Agent    ──► next cycle
```

**No path bypasses human approval. No path lets AI originate first-hand
experience.**

---

## The nine steps

### 1. Intake

Reject and return the opportunity if:

- `moat_alignment: conflicting` → belongs to A01, not A07
- `compliance_flags` non-empty → must clear with A30 first
- Tier missing, or tier D present
- No evidence array, or `evidence_confidence` absent

Rejection is logged, not silent.

### 2. Triage

Resolve to `build_new` / `rewrite` / `consolidate` / `refresh_only` / `decline`
per `responsibilities.md` §A. Search the published URL inventory and
`content/briefs/` **before** choosing `build_new`. Default bias is `rewrite`.

`decline` → emit a Decline Record and stop. This is a success, not a failure.

### 3. Source-material check

| Content type | Gate |
| --- | --- |
| `shrine_visit_report` | `visit_record_id` must resolve to notes + photos in repo |
| `annual_outlook`, `forecast_review` | `practitioner_input_id` with divinatory basis |
| `case_reflection` | `practitioner_input_id`, anonymised, consent recorded |
| all others | research sources listed and checkable |

**Material missing → the brief is deferred, not written around.** A07 emits a
material request to the human and parks the opportunity. Writing a brief that
assumes material will appear is how AI-originated experience enters the site.

### 4. Audience

Set `target_persona` and `reader_state` with `persona_source` recorded.
Client questions outrank persona documents; persona documents outrank inference.

### 5. Purpose

Set `content_goal` (business outcome) and `content_intent` (effect on reader).
Check the pair against `search_intent`: a `transactional` search served by an
`orient` page will rank and never convert.

### 6. Angle

Write `unique_value`, then apply the one-line test explicitly and record the
answer in `differentiation_basis`. If it fails, return to step 2 and reconsider
`decline`.

### 7. Structure

3+ title candidates, each compliance-checked. Full H2/H3 outline with
`purpose`, `source_requirement`, `target_question` per section. At most one
`featured_snippet_target`.

Count `ai_structurable` sections. Over 50% ⇒ flag `low_moat_density` and
re-examine.

### 8. Distribution

Primary CTA (exactly one), internal links (≥1 inbound, booking link for Tier
A/B), cluster role, related content, and the per-channel `sns_repurpose`
decision with `skip` used freely.

### 9. Commit

Add to the editorial calendar. Recompute committed capacity.

```
if committed_capacity > practitioner_monthly_capacity:
        do not issue the brief
        escalate to A01 Strategy Agent with a proposed cut list
```

Then emit `CB-xxxx` to `content/briefs/`.

---

## Cadence

### Weekly — brief production

- Intake new SEO opportunities, triage each
- Issue briefs up to remaining capacity, never past it
- Source-material chase: which briefs are blocked on a human input?
- 6-week seasonal look-ahead against A06's calendar
- Update editorial calendar

### Monthly — portfolio review

- Rewrite sweep: which published pages now meet a rewrite trigger?
- Cluster audit: hubs without spokes, spokes without hubs, orphans
- CTA performance by content type (Phase 2+)
- Decline-record review: has any `revisit_condition` been met?
- `firsthand_content_ratio` contribution — did this month's briefs raise or
  lower it? A lowering month is a **P0 escalation** (`../seo/kpi.md`)

### Quarterly — editorial direction

- Topic-cluster map rebuild
- Content type mix review against booking attribution
- Persona refresh against the last quarter's real client questions
- Prune list: pages to consolidate or remove, routed via A06 to Codex
- Capacity renegotiation with the practitioner

### Annual

- Flagship annual outlook brief — issued in time to publish by **late October**
- Prior-year forecast review brief — mandatory (`../seo/rules.md` §3.3)
- Full cluster architecture review

---

## Seasonal backward planning

A07 inherits A06's deadlines and adds its own lead time:

```
Seasonal window opens                  e.g. 初詣 demand builds early December
      ↑ 4 weeks   publish                        early November
      ↑ 2 weeks   human approval                 late October
      ↑ 1 week    A28 QA + A30 compliance        mid October
      ↑ 1 week    A10 SNS adaptation             mid October
      ↑ 2 weeks   A08 draft                      early October
      ↑ 1 week    A07 BRIEF ISSUED               late September
      ↑ 2–4 weeks visit completed                August–September
      ↑           A06 visit plan issued          July–August
```

A brief issued after its backward-planned date has already missed the window.
A07's weekly seasonal look-ahead exists to prevent exactly this.

---

## Escalation triggers

| Trigger | Route |
| --- | --- |
| Committed capacity exceeds practitioner capacity | A01 Strategy — **do not issue more briefs** |
| Opportunity arrives with `moat_alignment: conflicting` | A01 Strategy — reject at intake |
| Month's briefs would lower `firsthand_content_ratio` | A01 Strategy — P0 |
| Source material blocked > 2 weeks on a seasonal brief | Human — deadline at risk |
| Compliance flag raised at brief stage | A30 Compliance/Risk before any drafting |
| Two clusters competing for the same intent | A06 SEO — cannibalisation decision |
| A08 reports a brief was unachievable | A07 reworks the brief; repeated cases → root cause |
