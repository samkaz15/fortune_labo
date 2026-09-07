# SEO Agent — Outputs

Every output conforms to a schema in `schemas/`. Free-form output is not
accepted by downstream agents.

## Artifact catalogue

| Artifact | Schema | Consumer |
| --- | --- | --- |
| SEO Opportunity | `seo_opportunity.schema.json` | Strategy Agent (triage) |
| Content Brief | `content_brief.schema.json` | A07 Content Strategy Agent |
| Technical Issue | `technical_issue.schema.json` | Codex |
| Visit Plan | `visit_plan.schema.json` | Human practitioner |
| Internal Link Instruction | `internal_link_instruction.schema.json` | Codex |
| Keyword Register | `keyword_register.schema.json` | Internal state |
| SEO Report | (report format below) | Strategy Agent, human |

---

## SEO Opportunity — the universal unit

Every finding, of any type, is emitted as an SEO Opportunity. This is the common
currency between agents.

**Required fields:**

```
id                        stable identifier
type                      keyword | content | technical | internal_link |
                          serp | competitor | seasonal | compliance
tier                      A | B | C  (D is never emitted)
title                     one line
keyword                   nullable
search_intent             informational | navigational | commercial |
                          transactional | local
current_status            measured present state
problem                   what is wrong
evidence                  data supporting the problem, with source
evidence_confidence       measured | estimated | hypothesis
hypothesis                why it is happening
recommended_action        what to do
moat_alignment            required | neutral | conflicting
                          -> "conflicting" MUST escalate, not proceed
priority                  P0 | P1 | P2 | P3
priority_rationale        why this priority
expected_impact           on which Tier 1 or Tier 2 KPI, with magnitude
effort                    S | M | L | XL
assigned_agent            content | codex | cro | research | qa | human
implementation_requirement  spec detail for the assignee
measurement_kpi           how success is verified
measurement_window        when to check
deadline                  nullable; required if seasonal
blocked_by                dependency ids
```

`moat_alignment` and `evidence_confidence` are not standard SEO fields. They
exist to enforce `positioning.md` and `rules.md` §5.4 at the data-structure
level — an agent cannot emit a moat-conflicting recommendation without it being
machine-visible.

---

## Handoff contracts

**→ A07 Content Strategy Agent**
Sends: content_brief. Never partial requirements, never a bare keyword.
For Tier A, must reference an existing `visit_record_id`.
Receives back: an editorial Content Brief (`CB-xxxx`) or a decline record, and —
once the piece is produced — flagged gaps where the requirement set was
unachievable.

This brief is the **SEO requirement set**. A07 decides whether the page deserves
to exist, sets the angle and persona, and issues the brief A08 Content Production
actually writes from. Before A07 existed, this artifact went straight to
production; the requirements it carries are unchanged, only its consumer moved.
See [`/docs/agents/CONTENT-PIPELINE.md`](../../../docs/agents/CONTENT-PIPELINE.md).

**→ Codex**
Sends: technical_issue or internal_link_instruction, with acceptance criteria
and a verification method.
Never sends: prose descriptions of desired outcomes.
Receives back: PR reference, implementation notes, test result.

**→ Strategy Agent**
Sends: prioritised opportunity list, moat-conflict escalations, capacity
warnings, seasonal deadline risks.
Receives back: approved / rejected / deferred with rationale.

**→ CRO Agent**
Sends: landing page + its search intent + observed intent-conversion mismatch.
CRO owns the page experiment; SEO owns the intent definition.

**→ QA Agent**
Sends: SEO requirements and the compliance checklist for the artifact.
QA gate order: **compliance → factual → first-hand verification → editorial →
SEO → technical.** Compliance and first-hand verification rank above SEO.

**→ Human**
Sends: visit_plan, approval requests, moat escalations, annual forecast review
reminders.

---

## Report format

Ordered by tier. **Tier 1 first, always.**

```
1. Tier 1 — Business outcome
   bookings, revenue, CVR vs prior period and vs target

2. Tier 2 — Moat and authority
   branded search, firsthand_content_ratio, Tier A coverage,
   seasonal hit rate
   -> any decline here is flagged P0 regardless of Tier 3

3. Tier 3 — Search performance
   diagnostics only, framed as explanation for 1 and 2

4. Opportunities
   prioritised, with owner and deadline

5. Escalations
   moat conflicts, capacity limits, seasonal risk

6. Hypothesis ledger
   what was believed, what the evidence showed,
   what was updated  (per /AGENTS.md decision hierarchy)
```

The hypothesis ledger is mandatory. It operationalises the repository rule that
*when evidence conflicts with a hypothesis, the hypothesis is updated.*
