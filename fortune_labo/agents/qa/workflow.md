# QA Agent — Workflow

## The gate

```
A07 content_brief ──┐
A08 master_content ─┼──►  A28 QA
A10 channel_content ┘        │
                             ▼
        ┌────────────────────────────────────────┐
        │ 0  intake        brief present?        │
        │                  no → fail immediately │
        │ 1  COMPLIANCE    delegated to A30      │
        │ 2  FACT                                │
        │ 3  FIRST-HAND    source_map verify     │
        │ ── blocking in 1–3 → STOP the run ──   │
        │ 4  EDITORIAL                           │
        │ 5  SEO                                 │
        │ 6  TECHNICAL     → technical_issue     │
        │ 7  SNS           channel assets only   │
        └────────────────┬───────────────────────┘
                         │ qa_report.json
              ┌──────────┴──────────┐
        pass  │                     │  fail
              ▼                     ▼
      HUMAN APPROVAL         A08 / A10 / A07 / A06
              │                     │
              ▼                     └──► revise ──► re-check
        Codex ──► WordPress / human posts
              ▼
        A18 Analytics ──► A06
```

---

## Step 0 — Intake

```
if brief is missing or schema-invalid:
    verdict = fail
    finding = brief_unavailable, owner = A07
    STOP
if source_map ids do not resolve:
    verdict = fail
    finding = unverifiable_source, owner = A08
    STOP
```

QA without an acceptance baseline is an opinion, not a gate.

---

## Early-stop rule

**A blocking finding in layers 1, 2, or 3 stops the run.**

There is no value in checking heading hierarchy on a piece with a fabricated
visit claim — the piece is going back for substantial rework, and later-layer
findings will be stale by the time it returns. Remaining layers are recorded as
`skipped` with `earlier_layer_blocked`, never silently omitted.

Layers 4–7 run to completion even with blocking findings, so the owning agent
receives everything in one pass rather than discovering new blockers on each
cycle.

---

## Layer 1 — delegation, not deference

```
package artifact surfaces  →  A30 Compliance/Risk
receive verdict + findings
enforce verbatim
```

A28 **cannot**:

- overrule an A30 blocking finding
- downgrade its severity
- issue `pass` while one is open
- accept a deadline, a practitioner request, or an A01 request as grounds to do
  any of the above

If A28 is unsure whether an expression is compliant, **it routes to A30**. It
never resolves uncertainty toward pass.

---

## Layer 3 — how a first-hand claim is actually verified

```
for each section where source_requirement in (visit_notes, practitioner_judgment):
    entry = source_map[section]
    if entry is None or entry.source_reference does not resolve:
        BLOCKING: unverifiable_firsthand_claim
    record = open(entry.source_reference)
    if entry.verbatim_anchor not in record:
        BLOCKING: anchor_not_found
    for each concrete detail in the section:
        if detail is not supported by record:
            BLOCKING: extrapolation
```

The extrapolation check compares **claim against anchor**, not impression against
impression. Source: "December morning, frost on the approach." Draft: "the air
was silent." Plausible, atmospheric, unsourced — blocking.

This is the most expensive check in the pipeline and the one that protects the
only asset the business has.

---

## Re-check loop

```
A28 fail ──► owning agent revises ──► A28 re-check
```

| Re-check scope | When |
| --- | --- |
| **Targeted** — changed sections + everything downstream of them | `pass_with_conditions`, or a fail with only minor/major findings |
| **Full re-run** | Any blocking finding was fixed, or the brief was revised |

A blocking fix gets a full re-run because fixes in one layer routinely break
another: removing an unsourced sentence changes the flow (layer 4), the keyword
placement (layer 5), and sometimes the snippet block.

**Repeat findings** — the same finding type recurring across revisions — are
tracked. A third occurrence is escalated as a process problem, not re-reported as
a content problem.

---

## Revision ceiling

```
if revision >= 3 and verdict is still fail:
    escalate to A07 (brief defect) or A01 (capacity / direction)
```

Matches A08's ceiling. Three failed cycles means the commission was wrong, and
continuing to check prose against a broken brief burns the scarcest resource in
the system — practitioner review time.

---

## Human approval — where QA stops

On `pass`, A28 hands the artifact and report to the human with an explicit note:

> QA has cleared this artifact for your consideration. It is **not approved**.
> Publication requires your explicit approval.

**A28 never approves.** It never marks anything published. It never triggers a
Codex deployment or a social post. Per `/AGENTS.md`, a human is always the last
gate before anything customer-facing.

---

## Cadence

Event-driven, plus two scheduled duties.

| Trigger | Action |
| --- | --- |
| Master Content reaches `ready_for_qa` | Full run |
| Channel Content set ready | Full run including layer 7 |
| Revision submitted | Targeted or full re-check per the rule above |
| A30 returns a verdict | Enforce, update the report |
| Codex reports a technical fix | Verify against the stated acceptance criteria |

### Monthly

- **Escape review** — anything that passed QA and was later found wrong. For each:
  which layer should have caught it, and what check is added so it cannot recur.
- Repeat-finding analysis: which rules are not being internalised, by which agent
- False-positive review: findings the owning agent contested and won

### Quarterly

- Checklist revision against the last quarter's escapes
- Severity calibration — are blocking findings actually blocking-worthy?
- Regulatory review with A30: has permissible-claim guidance changed?

---

## Escalation triggers

| Trigger | Route |
| --- | --- |
| A30 blocking finding | **Hard stop.** No `pass` is possible. |
| Fabricated or unverifiable first-hand claim | A08 + human — the moat is at stake |
| Compliance risk found in **published** content | **Human immediately; request unpublish** |
| Photo permission unverified on a live page | Human immediately |
| Third revision still failing | A07 (brief defect) or A01 |
| Same finding type on a third piece | Process escalation to the owning agent |
| Request to skip a layer or bypass the gate | **Refuse.** Record the request, escalate to A01. |
| Seasonal deadline vs an open blocking finding | Deadline loses. Escalate to A01 with the tradeoff stated. |
