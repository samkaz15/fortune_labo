# Prompt — Risk Register Maintenance

## Task
Maintain the standing record of known risks, their status, and their owners.

## What goes in

| Origin | Example |
| --- | --- |
| `assessment` | A blocking finding whose underlying risk persists beyond one artifact |
| `incident` | Something published that should not have been |
| `accepted` | A risk a human explicitly accepted |
| `regulatory_change` | A rule change creating new exposure |
| `sweep` | A pattern found while monitoring published content |
| `external` | A platform policy change, an enforcement action against a comparable business |

## Per entry

```
id · title · domain · description · severity · likelihood · status
origin · affected_artifacts[] · owner · mitigation · review_by
```

`severity` reflects **actual exposure**, not discomfort. `likelihood` reflects
observed frequency, not worst case.

## Human-accepted risks

Only a human may accept a risk. Record permanently:

```
accepted_by · accepted_at · basis · mitigation · review_by
```

**A30 never removes an accepted risk from the register.** It carries it with a
review date, and reports when a review date passes.

Accepted risks accumulating in one domain is a **systemic pattern**, escalated to
A01 — it means exposure is being normalised one reasonable decision at a time.

## Nothing closes silently

A closed entry states what changed:

| Valid closure | Invalid |
| --- | --- |
| Content removed | "No longer relevant" |
| Rule changed and back catalogue swept | "Seems fine now" |
| Mitigation implemented and verified | "Nobody complained" |
| Professional reviewed and cleared | "It's been a while" |

## Review cadence

| Cadence | Action |
| --- | --- |
| Monthly | Open entries; overdue review dates; new incidents |
| Quarterly | Full register review; accepted-risk review; systemic pattern check |
| On rule change | Re-severity every affected entry; **sweep the back catalogue** |
| On incident | Add the incident; **pattern-sweep for the same shape everywhere** |

## The back-catalogue rule

Rescission windows run **3 years from realisation and 10 years from the act**.
Content compliant when published can become non-compliant when guidance changes,
and it stays exposed for years.

So a rule change always triggers a sweep of what is already live — never just a
forward-looking note to the content agents.

## Output
`schemas/risk_register_entry.schema.json` per entry, plus a monthly summary for
the human and A01: open by severity, overdue reviews, accepted-risk count by
domain, and any systemic pattern.
