# Human Approval

> The one gate no agent may pass, and how it is enforced structurally.

## The rule

From [`/AGENTS.md`](../../AGENTS.md):

> No agent may autonomously publish customer-facing content or make irreversible
> production changes without explicit human approval.

```
Draft  →  QA  →  ★ HUMAN APPROVAL ★  →  Publish  →  Measure  →  Record
```

## What requires approval

| Action | Approval | Notes |
| --- | --- | --- |
| Publishing a page or article | **Required** | Per artifact |
| Posting to any social channel | **Required** | **Per post** — approving a plan approves nothing |
| Sending a LINE message | **Required** | Plus mandatory A30 review first |
| Any customer message | **Required** | No agent messages a customer, ever |
| Production deployment | **Required** | Plus a second approval at merge |
| Bulk metadata / redirect / link operations | **Required** | Plus reviewed dry-run output |
| Accepting a compliance risk | **Required** | **Only a human may accept one**, recorded permanently |
| Unpublishing on a compliance incident | **Required** | A30 recommends; the human decides |
| Changing a ranking URL | **Required** | With a redirect instruction |

## What does not require approval

Internal artifacts that reach no customer: SEO opportunities, briefs, drafts,
channel content held for approval, QA reports, risk assessments, register
entries, and calendars. These are proposals, and Git is their audit trail.

---

## How it is enforced structurally

The gate is not only prose. It is encoded in the schemas, so a violation is
malformed data rather than a judgment call.

These constraints are exercised by the assertion set described at the end of this
document, so "enforced structurally" is a verified claim rather than a stated
intention.

| Mechanism | Where |
| --- | --- |
| `human_approval_required` is `const: true` | `channel_content.schema.json`, `qa_report.schema.json` |
| `approval_note` is fixed text | `qa_report.schema.json`, `repurpose_plan.schema.json` — the boundary cannot be lost when read out of context |
| A08 cannot set `qa_passed` without a `qa_report_id` from A28, nor `approved`/`published` without a recorded human approver | `master_content.schema.json` conditionals |
| A10 `status` enum permits `ready_for_qa` but not `approved` or `posted` | `channel_content.schema.json` |
| `approved` / `posted` require `approved_by` + `approved_at` | `channel_content.schema.json` conditional |
| Human risk acceptance requires `accepted_by`, `basis`, `review_by`, register id | `risk_assessment.schema.json` |
| No agent holds production write credentials | `seo/integrations.md`, `CODEX-INTERFACE.md` |

---

## What "QA passed" means

**It means cleared *for* your consideration. It does not mean approved.**

Every QA Report carries this fixed text:

> QA has cleared this artifact for your consideration. It is NOT approved.
> Publication requires your explicit approval.

A28 is a gate, not an approver. A30 is an authority on risk, not on publication.
The human is the only agent in this system with publication authority.

---

## What the approver is being asked

A `pass` verdict means the pipeline found nothing blocking. It does not mean the
piece is right for the business. Worth checking:

1. **Does this sound like you?** A08 and A10 write in a modelled voice. Only the
   practitioner knows whether it is theirs.
2. **Is the first-hand material accurate?** A28 verified that claims trace to
   records. Only the person who was there knows whether the record is right.
3. **Is the judgment one you actually hold?** A forecast presented as the
   practitioner's view must be the practitioner's view.
4. **Is the CTA the right ask?** For this reader, at this moment.
5. **Would you be comfortable if this were quoted back to you in a year?** The
   rescission window on spiritual-claim solicitation runs 3 years from realisation
   and 10 years from the act.

Question 5 is the one worth slowing down for.

---

## Rejecting

Rejection routes back with a reason, and the reason is recorded:

| Reason | Routes to |
| --- | --- |
| Voice is wrong | A08 (or A05 Brand, when implemented) |
| First-hand material is inaccurate | A08 — and the visit record is corrected |
| Judgment is not mine | A08, blocking — this is a truthfulness issue |
| Wrong topic entirely | A07 — the brief was wrong |
| Wrong ask / wrong CTA | A07 |
| Uncomfortable, cannot articulate why | A30 — a reputational-risk assessment |

**The last row matters.** Discomfort a practitioner cannot articulate is often a
real risk signal, and it is routed for assessment rather than overridden.

---

## Accepting a risk

Only a human may accept a risk A30 has flagged. The acceptance is recorded
permanently in the risk register:

```
accepted_by · accepted_at · basis · mitigation · review_by
```

An accepted risk is **a documented decision, never a silent override**. A30 does
not remove it from the register; it carries it with a review date and reports when
the date passes.

Accepted risks accumulating in one domain is escalated to A01 Strategy as a
systemic pattern — that is what exposure being normalised one reasonable decision
at a time looks like from the outside.

---

## Deadline pressure

Seasonal windows are real and unforgiving: a shrine visit that misses its window
loses a full year (`seo/positioning.md` §7).

**None of that changes the gate.**

| Pressure | Response |
| --- | --- |
| "Publish without QA, the window closes tomorrow" | Refused. Recorded. Escalated to A01. |
| "Downgrade this blocking finding" | Refused by A28 and A30 alike. Recorded. |
| "Approve the whole social plan at once" | The plan is not the posts. Each post is approved individually. |
| "It performed well last time" | Performance is not a compliance argument. |

If a deadline and a blocking finding conflict, **the deadline loses**, and the
tradeoff is escalated to A01 Strategy with the cost stated. A missed window costs
a year. A solicitation violation carries a ten-year exposure window and the
credibility of a named practitioner.

---

## Verifying the gate

The approval constraints above are JSON Schema conditionals, so they can be
tested. A minimal check that the gate holds:

```python
# requires: pip install jsonschema
import json
from jsonschema import Draft202012Validator as V

mc = json.load(open("fortune_labo/agents/content-production/schemas/master_content.schema.json"))
draft = {...}                      # a valid master_content with status "ready_for_qa"

assert     V(mc).is_valid(draft)
assert not V(mc).is_valid({**draft, "status": "approved"})          # no approver
assert not V(mc).is_valid({**draft, "status": "qa_passed"})         # no QA report
assert     V(mc).is_valid({**draft, "status": "approved",
                           "qa_report_id": "QA-0001",
                           "approval": {"approved_by": "practitioner",
                                        "approved_at": "2026-09-08"}})
```

The equivalent holds for `channel_content` (`approved`/`posted` require
`approved_by` and `approved_at`; LINE requires `requires_compliance_review: true`),
`qa_report` (`pass` is invalid while `a30_verdict.blocking_open` is true), and
`risk_assessment` (any blocking finding forces `verdict: block`).

Wiring this into CI is item 2 on the Codex backlog
([`CODEX-INTERFACE.md`](./CODEX-INTERFACE.md)) — it turns these rules from
documentation into a build failure.
