# Compliance/Risk Agent — KPI Structure

## Design principle

A compliance function has two failure modes, and optimising against one produces
the other:

```
too permissive → violations reach the public → legal exposure, lost credibility
too restrictive → the gate gets routed around → protects nothing at all
```

**A30 is measured on incidents prevented first, and on calibration second.**
Neither alone is sufficient.

---

## KGI

> **Zero compliance incidents in published content, with a gate that is still
> being used.**

The second clause is not decoration. A30 blocking everything and being bypassed
scores zero incidents on paper and provides no protection.

---

## Tier 1 — Incident prevention

| KPI | Definition | Target |
| --- | --- | --- |
| `published_violations` | Compliance violations found in live content | **= 0. Non-negotiable.** |
| `unpublish_events` | Content requiring emergency removal | **= 0** |
| `regulatory_actions` | Complaints, warnings, or actions from any authority | **= 0** |
| `platform_takedowns` | Posts removed or accounts actioned by a platform | **= 0** |
| `consent_violations` | Client or personal content published without a recorded consent | **= 0** |
| `permission_violations` | Images published without confirmed permission | **= 0** |

One incident outranks every other metric here. Every incident triggers a root
cause, a pattern sweep, and a new or tightened check.

---

## Tier 2 — Gate integrity

| KPI | Definition | Target |
| --- | --- | --- |
| `blocking_override_events` | Blocking findings overruled or downgraded by another agent | **= 0** |
| `bypass_events` | Content published without an A30 assessment where one was required | **= 0** |
| `line_review_coverage` | LINE assets reviewed / LINE assets published | **= 1.0** |
| `sensitive_domain_pre_review_rate` | Flagged briefs reviewed before drafting / flagged briefs | **= 1.0** |
| `escalation_completion_rate` | `escalate_to_professional` findings actually reviewed by a professional | **= 1.0** |
| `accepted_risk_review_rate` | Human-accepted risks reviewed by their review date | **= 1.0** |

`blocking_override_events` and `bypass_events` detect **the gate eroding under
business pressure**. They appear long before the first incident does, which is
what makes them worth watching.

`accepted_risk_review_rate` prevents accepted risks from quietly becoming
permanent exemptions.

---

## Tier 3 — Calibration and process (diagnostics only)

| KPI | What it tells you |
| --- | --- |
| `false_positive_rate` | Findings contested and won by the owning agent. **Rising = A30 is miscalibrated and will be routed around.** |
| `reworing_acceptance_rate` | Binding rewordings applied without dispute. Low = rewordings are impractical |
| `findings_per_artifact` | Rigour. A sudden drop is investigated. |
| `repeat_finding_rate` | Which rules upstream agents have not internalised |
| `pre_review_vs_post_review_ratio` | Higher pre-review = cheaper corrections |
| `median_assessment_turnaround_hours` | Speed. **Last, deliberately.** |
| `register_entries_open` | Accumulated unresolved risk |
| `accepted_risks_open` | Accumulated deliberate exposure — a rising count is escalated to A01 |

**`false_positive_rate` is the metric that keeps A30 honest in the other
direction.** A compliance agent that is wrong about what is risky trains everyone
around it to stop listening, and that is how the gate stops working.

---

## Forbidden framings

A30 must not report, and A01 must not accept:

- Block rate as a result ("we blocked 30 items" measures nothing)
- Turnaround speed as a headline
- "No findings this month" without investigating whether the sweep ran
- Any Tier 3 movement while a Tier 1 metric is non-zero
- A deadline, a campaign, or a performance target as context for a risk decision

---

## Incident review (mandatory, every incident)

```
1. What was published that should not have been?
2. Which domain check should have caught it?
3. Why did it not?
     - rule absent          → write the rule
     - rule present, missed → tighten the procedure
     - assessment skipped   → why? was it bypassed?
     - finding downgraded   → by whom, under what pressure?
4. What check is added so it cannot recur?
5. PATTERN SWEEP — every other artifact with the same pattern,
   including the back catalogue. The exposure window is 3 years
   from realisation / 10 years from the act.
6. Register the incident with its full history.
```

**Suppressing or minimising an incident is the most serious failure available to
this agent.** A recorded incident improves the gate; a hidden one guarantees a
repeat and extends the exposure window.

---

## Diagnostic matrix

| Pattern | Likely cause | Owner |
| --- | --- | --- |
| Violation found in published content | Domain check absent or skipped | **A30** — most serious |
| Blocking finding was overruled | Gate authority eroding | **A01 + human** |
| Rising `false_positive_rate` | Miscalibration; A30 heading toward being ignored | **A30** |
| Same finding pattern across three artifacts | Rule not internalised upstream | A08 / A10 |
| Rising LINE block rate | Anxiety framing or over-messaging | A10 → **A30** |
| Accepted risks accumulating in one domain | Systemic exposure being normalised | **A01** |
| Findings concentrated at post-draft review | Pre-drafting review being skipped | A07 → A30 |
| Content compliant at publication now non-compliant | Regulatory change | **A30** — back-catalogue sweep |
