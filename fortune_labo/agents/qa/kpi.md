# QA Agent — KPI Structure

## Design principle

The obvious KPIs for a QA function are **throughput and pass rate** — checks per
week, percentage passed, turnaround time. Both are actively dangerous here:
optimising either is achieved most easily by checking less carefully.

**A28 is measured on what it lets through, not on how fast it lets things
through.**

---

## KGI

> **Zero compliance or fabrication incidents in published content.**

This is the one KGI in the system that is not a growth metric, because the
failure it prevents is not a missed opportunity — it is legal exposure and the
destruction of the practice's credibility.

---

## Tier 1 — Escape prevention (the only tier that defines success)

| KPI | Definition | Target |
| --- | --- | --- |
| `compliance_escapes` | Compliance violations found in published content | **= 0. Non-negotiable.** |
| `fabrication_escapes` | Unsourced or fabricated claims found in published content | **= 0. Non-negotiable.** |
| `factual_escapes` | Factual errors requiring post-publication correction | **= 0** |
| `total_escape_rate` | Escapes / artifacts passed | **= 0** |
| `unpublish_events` | Content requiring emergency removal | **= 0** |

**One escape outranks every other metric in this document.** An escape triggers a
mandatory root-cause review: which layer should have caught it, why it did not,
and what check is added so it cannot recur.

`total_escape_rate` cannot be gamed by failing everything, because Tier 3 tracks
false positives and the owning agents contest findings on the record.

---

## Tier 2 — Gate integrity

| KPI | Definition | Target |
| --- | --- | --- |
| `gate_bypass_events` | Artifacts published without a QA verdict | **= 0** |
| `severity_downgrade_events` | Blocking findings downgraded under pressure | **= 0** |
| `unverifiable_pass_events` | `pass` issued on an artifact QA could not fully check | **= 0** |
| `a30_enforcement_rate` | A30 blocking findings enforced / A30 blocking findings issued | **= 1.0** |
| `layer_completion_rate` | Layers run to completion or honestly recorded as skipped | **= 1.0** |
| `finding_actionability` | Findings with evidence, a required fix, and an owner | **= 1.0** |

`severity_downgrade_events` and `gate_bypass_events` are the metrics that
detect **schedule pressure winning**. They are the earliest visible symptom of a
QA function being eroded, and they appear long before the first escape.

---

## Tier 3 — Process health (diagnostics only)

Never reported as achievement on their own.

| KPI | What it actually tells you |
| --- | --- |
| `findings_per_artifact` | Rigour. A sudden drop is investigated, not celebrated. |
| `blocking_findings_per_artifact` | Whether upstream agents have internalised the rules |
| `first_pass_rate` | Upstream quality. **Not a QA target** — raising it by checking less is the failure mode. |
| `repeat_finding_rate` | Which rules are not sticking, and for which agent |
| `false_positive_rate` | Findings contested and won by the owning agent |
| `revision_cycles_per_artifact` | Target ≤ 2 |
| `median_qa_turnaround_hours` | Speed. **Last, deliberately.** |
| `contested_finding_rate` | Whether QA and the writing agents disagree systematically |

**A zero-finding month is a warning sign, not an achievement.** It is
investigated as a possible rigour failure before it is celebrated as upstream
excellence.

---

## Forbidden framings

A28 must not report, and A01 must not accept:

- Pass rate as a quality result
- Turnaround speed as a headline result
- "No findings this month" as an achievement without an investigation
- Any throughput metric while a Tier 1 metric is non-zero
- A deadline as a reason a blocking finding was downgraded

---

## Escape review (mandatory on every escape)

```
1. What was published that should not have been?
2. Which layer should have caught it?
3. Why did that layer not catch it?
     - check absent          → add the check
     - check present, missed → why? tighten the procedure
     - layer skipped         → why? was the skip honest?
     - severity downgraded   → by whom, under what pressure?
4. What check is added so this cannot recur?
5. Are other published pages affected? Sweep them.
```

Recorded in the escape register and reviewed monthly. **Suppressing an escape is
worse than causing one** — an escape that is recorded improves the gate, and an
escape that is hidden guarantees a repeat.

---

## Diagnostic matrix

| Pattern | Likely cause | Owner |
| --- | --- | --- |
| Compliance escape | Layer 1 not run, or A30 verdict not enforced | **A28** — most serious |
| Fabrication escape | Layer 3 anchor check skipped | **A28** |
| Findings per artifact dropping | Rigour eroding under schedule pressure | **A28** |
| Same finding on many pieces from one agent | Rule not internalised upstream | A08 / A10 |
| High false-positive rate | Checklist miscalibrated | **A28** |
| Blocking findings rising on one content type | Brief pattern is defective | A07 |
| Third revision still failing | Defective commission | A07 / A01 |
| Bypass requested near a seasonal deadline | Capacity planning failed upstream | A07 → A01 |
