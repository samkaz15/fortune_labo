# Content Pipeline — Agent Data Flow

> The end-to-end artifact chain from search demand to measured outcome, and the
> schema contract at every handoff.

## The loop

```text
                    ┌──────────────────────────────────────────┐
                    │                                          │
                    ▼                                          │
        ┌───────────────────────┐                              │
        │ A02 Research Agent    │  market · competitors · demand│
        └───────────┬───────────┘                              │
                    ▼                                          │
        ┌───────────────────────┐                              │
        │ A06 SEO Agent         │                              │
        └───────────┬───────────┘                              │
                    │  seo_opportunity.json                    │
                    │  visit_plan.json ──► HUMAN VISIT ──┐     │
                    ▼                                    │     │
        ┌───────────────────────┐                        │     │
        │ A07 Content Strategy  │ ◄──── visit notes ─────┘     │
        └───────────┬───────────┘        + photos              │
                    │  content_brief.json  (CB-xxxx)           │
                    ▼                                          │
        ┌───────────────────────┐                              │
        │ A08 Content Production│                              │
        └───────────┬───────────┘                              │
                    │  master_content.json  (MC-xxxx)          │
          ┌─────────┴─────────┐                                │
          ▼                   ▼                                │
┌───────────────────┐   ┌─────────────────────┐                │
│ A10 SNS Content   │   │                     │                │
└─────────┬─────────┘   │                     │                │
          │ channel_content.json (CC-xxxx)    │                │
          └─────────┬───────────────────────  ┘                │
                    ▼                                          │
        ┌───────────────────────┐   layer 1   ┌──────────────┐ │
        │ A28 QA Agent          │ ◄─────────► │ A30          │ │
        │                       │  delegated  │ Compliance   │ │
        └───────────┬───────────┘             │ /Risk        │ │
                    │  qa_report.json         └──────────────┘ │
                    │  (QA-xxxx)               risk_assessment │
                    ▼                                          │
        ┌───────────────────────┐                              │
        │ ★ HUMAN APPROVAL ★    │  mandatory — /AGENTS.md      │
        └───────────┬───────────┘                              │
                    ▼                                          │
        ┌───────────────────────┐                              │
        │ Codex / human posts   │  WordPress · SNS             │
        └───────────┬───────────┘                              │
                    ▼                                          │
        ┌───────────────────────┐                              │
        │ A18 Analytics Agent   │  GSC · GA4 · bookings        │
        └───────────┬───────────┘                              │
                    │                                          │
                    └──────────────────────────────────────────┘
                              back to A06 SEO Agent
```

**Two hard invariants hold at every step:**

1. **No path bypasses human approval.** Nothing customer-facing is published,
   posted, or sent without an explicit human decision (`/AGENTS.md`).
2. **No path lets AI originate first-hand experience.** The human-visit branch is
   a hard dependency for Tier A content, enforced structurally by
   `visit_record_id` and `source_map`.

---

## Artifact chain

| # | Producer | Artifact | Id | Schema | Consumer |
|---|---|---|---|---|---|
| 1 | A06 | SEO Opportunity | `SEO-xxxx` | [`seo/schemas/seo_opportunity.schema.json`](../../fortune_labo/agents/seo/schemas/seo_opportunity.schema.json) | A07 |
| 1b | A06 | SEO requirement set | `BRIEF-xxxx` | [`seo/schemas/content_brief.schema.json`](../../fortune_labo/agents/seo/schemas/content_brief.schema.json) | A07 |
| 1c | A06 | Visit Plan | — | [`seo/schemas/visit_plan.schema.json`](../../fortune_labo/agents/seo/schemas/visit_plan.schema.json) | **Human** |
| 2 | A07 | **Content Brief** | `CB-xxxx` | [`content-strategy/schemas/content_brief.schema.json`](../../fortune_labo/agents/content-strategy/schemas/content_brief.schema.json) | A08, A10, A28, A30 |
| 2b | A07 | Decline Record | `DEC-xxxx` | [`content-strategy/schemas/decline_record.schema.json`](../../fortune_labo/agents/content-strategy/schemas/decline_record.schema.json) | A01, A06 |
| 2c | A07 | Editorial Calendar | `CAL-yyyy-mm` | [`content-strategy/schemas/editorial_calendar.schema.json`](../../fortune_labo/agents/content-strategy/schemas/editorial_calendar.schema.json) | A01, human |
| 3 | A08 | **Master Content** | `MC-xxxx` | [`content-production/schemas/master_content.schema.json`](../../fortune_labo/agents/content-production/schemas/master_content.schema.json) | A10, A28, A30, Codex |
| 3b | A08 | Content Gap Report | `GAP-xxxx` | [`content-production/schemas/content_gap_report.schema.json`](../../fortune_labo/agents/content-production/schemas/content_gap_report.schema.json) | A07, human |
| 4 | A10 | **Channel Content** | `CC-xxxx` | [`sns-content/schemas/channel_content.schema.json`](../../fortune_labo/agents/sns-content/schemas/channel_content.schema.json) | A28, A30, human |
| 4b | A10 | Repurpose Plan | `RP-xxxx` | [`sns-content/schemas/repurpose_plan.schema.json`](../../fortune_labo/agents/sns-content/schemas/repurpose_plan.schema.json) | human, A09 |
| 5 | A30 | **Risk Assessment** | `RISK-xxxx` | [`compliance-risk/schemas/risk_assessment.schema.json`](../../fortune_labo/agents/compliance-risk/schemas/risk_assessment.schema.json) | A28 |
| 5b | A30 | Risk Register Entry | `REG-xxxx` | [`compliance-risk/schemas/risk_register_entry.schema.json`](../../fortune_labo/agents/compliance-risk/schemas/risk_register_entry.schema.json) | human, A01 |
| 6 | A28 | **QA Report** | `QA-xxxx` | [`qa/schemas/qa_report.schema.json`](../../fortune_labo/agents/qa/schemas/qa_report.schema.json) | human, all producers |
| 6b | A28 | QA Finding | `F-xxx` | [`qa/schemas/qa_finding.schema.json`](../../fortune_labo/agents/qa/schemas/qa_finding.schema.json) | routed per owner |
| 6c | A28/A06 | Technical Issue | — | [`seo/schemas/technical_issue.schema.json`](../../fortune_labo/agents/seo/schemas/technical_issue.schema.json) | **Codex** |

---

## Handoff contracts

### A06 → A07 · demand becomes an editorial question

**Sends:** `seo_opportunity` (+ the SEO requirement set and keyword register entry).

A07 **rejects at intake**:

| Condition | Route |
| --- | --- |
| `moat_alignment: conflicting` | A01 Strategy — accepting it would launder an escalation into a brief |
| `compliance_flags` non-empty | A30 first |
| Tier missing, or Tier D | Rejected outright |
| Empty `evidence` or missing `evidence_confidence` | Returned to A06 |

**Returns:** decline records, capacity escalations, cannibalisation findings.

### A07 → A08 · editorial commitment becomes prose

**Sends:** one complete `content_brief`. Never a bare keyword, never a partial
outline.

Structurally guaranteed by the schema before A08 ever sees it:

- First-hand content types require a resolvable `visit_record_id` or
  `practitioner_input_id`
- ≥1 planned inbound internal link (no orphans)
- Booking-page link for Tier A/B
- `rewrite` requires `existing_url` + `rewrite_reason`
- `annual_outlook` requires `divinatory_basis_required: true`
- `case_reflection` requires `client_consent_recorded: true`

**Returns:** `content_gap_report`, `structure_deviations`, `seo_conflicts`,
`suggested_links`.

### A08 → A10 · prose becomes channel material

**Sends:** `master_content` + `sns_source_blocks` (the strongest observation, the
clearest answer, the most quotable judgment, the visual moment).

A10 rewrites per channel. A08 never writes social copy; A10 never writes articles.

### A07 → A10 · the repurposing decision

**Sends:** the brief's `sns_repurpose` block — per channel `viability`, `angle`,
`objective`, `rationale`.

A10 may **downgrade** a channel to `skip`. A10 may never **upgrade** an A07 `skip`.

### A08 / A10 → A30 → A28 · the compliance gate

```
artifact ──► A28 (orchestrates) ──delegates layer 1──► A30 (adjudicates)
                    ▲                                       │
                    └────────── risk_assessment ────────────┘
                              enforced verbatim
```

A28 **cannot** overrule an A30 `block`, downgrade its severity, or issue `pass`
while one is open. Only a **human** may accept a flagged risk, on the record.

### A28 → Human · the gate

`pass` clears an artifact **for** human approval. It is not approval.
See [`HUMAN-APPROVAL.md`](./HUMAN-APPROVAL.md).

### A28 / A06 → Codex · what to implement

Technical findings from either agent use **the same** `technical_issue` schema, so
Codex receives one format regardless of origin. Each carries acceptance criteria
and a verification method, or it is not emitted.
See [`CODEX-INTERFACE.md`](./CODEX-INTERFACE.md).

### Publishing → A18 → A06 · the loop closes

Measured outcome returns to A06 as evidence, and A06 updates its hypothesis
ledger rather than reinterpreting the evidence (`/AGENTS.md` decision hierarchy).

---

## The two files named `content_brief.schema.json`

Both are valid. They are different layers of the same handoff.

| | `agents/seo/` | `agents/content-strategy/` |
| --- | --- | --- |
| Author | A06 SEO Agent | A07 Content Strategy Agent |
| Id prefix | `BRIEF-` | `CB-` |
| Answers | "What must be true for this page to rank and stay compliant?" | "What are we publishing, for whom, and why us?" |
| Consumer | A07 | A08 |
| Carries | keyword, intent, SERP gap, structured data, SEO constraints | persona, reader state, angle, unique value, outline, CTA, distribution, priority |

A07's brief references A06's by `seo_brief_id` and **re-carries every constraint
A06 set**, so A08 reads exactly one file.

This layering is why A06's own documentation refers to its downstream consumer as
"Content Agent": before A07 existed, A06's brief went straight to production.
With A07 in place, A06's brief is the SEO requirement set that A07 builds on.

---

## Id conventions

| Prefix | Artifact | Owner |
| --- | --- | --- |
| `SEO-` | SEO Opportunity | A06 |
| `BRIEF-` | SEO requirement set | A06 |
| `CB-` | Content Brief | A07 |
| `DEC-` | Decline Record | A07 |
| `CAL-` | Editorial Calendar | A07 |
| `MC-` | Master Content | A08 |
| `GAP-` | Content Gap Report | A08 |
| `CC-` | Channel Content | A10 |
| `RP-` | Repurpose Plan | A10 |
| `QA-` | QA Report | A28 |
| `F-` | QA Finding | A28 |
| `RISK-` | Risk Assessment | A30 |
| `R-` | Risk Finding | A30 |
| `REG-` | Risk Register Entry | A30 |

---

## Where artifacts live

```
content/
├── briefs/       CB-xxxx.json          A07
├── declines/     DEC-xxxx.json         A07
├── calendar/     CAL-yyyy-mm.json      A07
├── drafts/       MC-xxxx.json          A08
├── gaps/         GAP-xxxx.json         A08
├── sns/          CC-xxxx.json          A10
│   └── plans/    RP-xxxx.json          A10
├── qa/           QA-xxxx.json          A28
│   └── technical/                      A28 → Codex
└── compliance/   RISK-xxxx.json        A30
    └── register/ REG-xxxx.json         A30
```

See [`content/README.md`](../../content/README.md) for what may and may not be
stored there.

---

## Failure paths

Every stage can refuse, and refusing is a designed outcome rather than an error.

| Stage | Refusal | Meaning |
| --- | --- | --- |
| A07 | `decline_record` | This should not be built. Healthy rate: 30–60%. |
| A07 | deferral | Source material does not exist yet |
| A08 | `content_gap_report` | Cannot be written honestly. **Normal and expected.** |
| A10 | `skip` | This channel is not right for this piece |
| A30 | `block` | Legal or regulatory risk. Binding. |
| A30 | `escalate_to_professional` | Genuine legal interpretation needed |
| A28 | `fail` | Returns to the owning agent |
| Human | rejection | Final word, always |

**A pipeline that never refuses is not working.** A07 approving everything, A08
never reporting a gap, A10 adapting all nine channels, A28 finding nothing, and
A30 blocking nothing are each investigated as failure signals, not celebrated.

## Revision ceilings

A08 and A28 both stop at three failed revisions and return the piece to A07.
Three failures means the commission was defective, and continuing to rework prose
against a broken brief consumes the scarcest resource in the system —
practitioner review time.
