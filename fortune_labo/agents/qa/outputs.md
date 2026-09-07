# QA Agent — Outputs

## Artifact catalogue

| Artifact | Schema | Consumer | Stored at |
| --- | --- | --- | --- |
| **QA Report** | `qa_report.schema.json` | Human approver, A08, A10, A07, A06 | `content/qa/QA-xxxx.json` |
| QA Finding | `qa_finding.schema.json` | Embedded in the report; routed per owner | — |
| Technical Issue | [`../seo/schemas/technical_issue.schema.json`](../seo/schemas/technical_issue.schema.json) | **Codex** | `content/qa/technical/` |

Technical findings deliberately reuse A06's schema so Codex receives one format
regardless of which agent found the problem.

---

## QA Report

`QA-xxxx`. One report per artifact per revision.

```
identity   id, target_type, target_id, brief_id, revision, checked_at
verdict    verdict, blocking_count, major_count, minor_count
layers     layer_results[]  — one per layer, with status and skip reason
findings   findings[]       — every finding, with severity, owner, evidence
routing    routed_to[], technical_issue_ids[]
approval   human_approval_required, approval_note
history    previous_report_id, repeat_findings[]
```

### The verdict

| Verdict | Condition | Next step |
| --- | --- | --- |
| `pass` | Zero blocking findings, zero unresolved A30 blocking findings | **Human approval** |
| `pass_with_conditions` | Zero blocking, ≥1 major that must be fixed and re-verified | Fix → targeted re-check → human approval |
| `fail` | ≥1 blocking finding, or the brief was unavailable | Return to the owning agent |

**There is no fourth value and no partial pass.** A verdict of `pass` means
*cleared for a human to approve*, never *approved*.

### Every finding is actionable

```
finding_id · layer · severity · surface · location
what_is_wrong · evidence · why_it_matters · required_fix · owner_agent
```

- **`evidence`** — the actual text, the source line, the measured value. Not
  "reads awkwardly".
- **`required_fix`** — what specifically must change. A finding that only
  identifies a problem forces the receiving agent to guess, and guessing produces
  a second QA cycle.
- **`owner_agent`** — a finding routed to nobody is incomplete.

### Layer results record skips honestly

Each layer reports `passed` / `failed` / `skipped` / `not_applicable`, with a
reason for any skip. A layer skipped because an earlier layer blocked is recorded
as `skipped` with `earlier_layer_blocked` — **never silently omitted**, so nobody
reads a short report as a clean one.

---

## Handoff contracts

**→ Human approver (on `pass`)**
Sends: the report, the artifact, and the approval note. The note states plainly
that QA has cleared the artifact for consideration and that **publication
requires the human's explicit approval** (`/AGENTS.md`).

**→ A08 Content Production**
Sends: findings owned by A08, by severity. A08 fixes or contests with reasoning;
A08 may never ignore one and may never mark its own draft passed.

**→ A10 SNS Content**
Sends: channel-asset findings, per channel.

**→ A07 Content Strategy**
Sends: findings whose root cause is the brief — ambiguity, wrong angle,
unachievable outline, a commissioned SNS adaptation the material cannot support.
Also every `brief_unavailable` failure.

**→ A06 SEO Agent**
Sends: cannibalisation findings, internal-link architecture problems, keyword
conflicts, and structured-data priority mismatches.

**→ A30 Compliance/Risk**
Sends: the artifact for layer 1, and any expression A28 is unsure about.
**Uncertainty routes to A30 rather than resolving toward pass.**

**→ Codex**
Sends: `technical_issue` artifacts, each with acceptance criteria and a
verification method. A technical issue without one is incomplete and is not
emitted (`../seo/integrations.md`).

---

## Escape record

When something that passed QA is found wrong after publication, A28 records an
escape: what was missed, which layer should have caught it, and what check is
added so it cannot recur.

Escapes are the **primary input to QA's own improvement**, and the escape rate is
this agent's top KPI. A QA agent that never records an escape is either perfect
or not looking, and only one of those is likely.
