# Compliance/Risk Agent — Outputs

## Artifact catalogue

| Artifact | Schema | Consumer | Stored at |
| --- | --- | --- | --- |
| **Risk Assessment** | `risk_assessment.schema.json` | A28, A08, A10, A07, human | `content/compliance/RISK-xxxx.json` |
| Risk Register Entry | `risk_register_entry.schema.json` | Human, A01 | `content/compliance/register/` |
| Regulatory Watch Note | Report format below | A06, A07, A08, A10, A01 | `docs/compliance/` |
| Incident Record | `risk_register_entry` with `origin: incident` | Human, A01, A28 | `content/compliance/register/` |

---

## Risk Assessment — the verdict

`RISK-xxxx`. One per artifact per revision. **This is what A28 enforces.**

```
identity   id, target_type, target_id, revision, assessed_at
domains    domain_results[]  — one per risk domain, with status
findings   findings[]        — each with a binding reworing where one exists
verdict    verdict, verdict_rationale, blocking_count
treatment  treatment_rules[] — issued pre-drafting for sensitive domains
authority  binding_note, human_acceptance
```

### Three verdicts

| Verdict | Meaning | Effect on A28 |
| --- | --- | --- |
| `clear` | No blocking risk found | A28 may proceed to its other layers |
| `clear_with_conditions` | Named rewordings must be applied and re-verified | A28 gates on the conditions |
| `block` | Blocking risk present | **A28 cannot issue `pass`.** Period. |

### Findings carry rewordings, not just refusals

A compliance function that only says no gets routed around, and a routed-around
gate protects nothing. Wherever a compliant expression of the same intent exists,
the finding carries it:

```
finding_id · domain · severity · surface · location
what_is_wrong · why_it_is_a_risk · legal_basis
current_text · required_text        ← the binding reworing
alternatives[]                       ← where more than one works
```

`required_text` is **binding on A08 and A10**. They may ask for clarification;
they may not negotiate it on stylistic grounds.

Where no compliant expression exists — the claim itself is the problem — the
finding says `remove` and explains why no reworing can fix it.

### `escalate_to_professional`

Where a question turns on genuine legal interpretation rather than an established
rule, the finding severity is `escalate_to_professional`. This is a **blocking
condition**: A30 does not guess at an interpretation and clear content on that
guess.

---

## Treatment rules (issued before drafting)

When A07 flags a `sensitive_domain`, A30 issues treatment rules **before A08
writes**:

```
domain · what_may_not_be_claimed · required_referral
required_framing · required_placement · disclaimer_text
```

A rule issued before drafting costs one revision. The same rule issued after
costs three, and burns practitioner review time — the scarcest resource in the
system.

---

## Risk Register

The standing record. Entries originate from assessments, incidents, accepted
risks, regulatory changes, and published-content sweeps.

```
id, title, domain, description, severity, likelihood, status
origin, affected_artifacts[], owner, mitigation, review_by
human_acceptance{}
```

### Human-accepted risks

Only a human may accept a flagged risk, and the acceptance is recorded
permanently:

```
accepted_by · accepted_at · basis · mitigation · review_by
```

**An accepted risk is a documented decision, never a silent override.** A30 does
not remove an accepted risk from the register — it carries it with a review date.

### Nothing closes silently

A closed entry states what changed: the content was removed, the rule changed,
the risk was mitigated, or a professional reviewed it. "No longer relevant" is
not a closure reason.

---

## Regulatory Watch Note

Quarterly, or immediately on a material change:

```
1. What changed          instrument, guidance, or platform policy
2. Effective date
3. What it affects       which content types, which channels
4. Rule changes required which files, which rules
5. Back-catalogue sweep  which published pages must be re-checked
6. Notification          A06, A07, A08, A10, A01
```

**Content compliant at publication can become non-compliant.** With rescission
windows of 3 years from realisation and 10 years from the act, the back catalogue
stays in scope for years — so a rule change always triggers a sweep, never just a
forward-looking note.

---

## Handoff contracts

**→ A28 QA**
Sends: the Risk Assessment as the layer 1 verdict. A28 enforces it verbatim and
cannot overrule, downgrade, or pass around a `block`.

**→ A08 Content Production**
Sends: binding rewordings and pre-drafting treatment rules.

**→ A10 SNS Content**
Sends: per-asset rewordings, and the standing rule that every LINE draft is
reviewed.

**→ A07 Content Strategy**
Sends: themes that cannot be treated compliantly (so they are declined at brief
stage, not drafted and blocked), and treatment rules for flagged briefs.

**→ A06 SEO Agent**
Sends: keywords or angles whose compliant treatment is impossible, for exclusion
from the register.

**→ Human**
Sends: `escalate_to_professional` findings, incident notifications with an
unpublish recommendation, risk-acceptance requests, and the quarterly regulatory
watch.

**→ A01 Strategy Agent**
Sends: systemic risk patterns, accepted-risk accumulation, and any case where
business pressure is being applied to a compliance decision.
