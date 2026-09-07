# Prompt — Content Compliance Review

## Task
Assess one artifact across all six risk domains and issue a verdict.

## Step 1 — Enumerate every surface

**Site:** title · H1 · every heading · lead · body · FAQ · CTA · meta description
· disclaimer · image alt text

**Social:** hook · body · CTA · every hashtag · every on-screen text frame ·
every carousel slide · thumbnail text and concept · video title · description

Assess all of them. A compliant body under a fear-framed title is still a
violation.

## Step 2 — Domain sweep

### A. Solicitation
Fear framing · anxiety creation · urgency through anxiety · guaranteed outcome
(`必ず`/`絶対`/`願いが叶う`) · implied inevitability · efficacy ranking · implied
misfortune from inaction.

### B. Sensitive domain
Medical diagnosis, prognosis, treatment advice, or cure claim · financial or
purchase advice · legal position · instruction on a major life decision · any
divinatory claim about a crisis outcome. Required treatment: **refer, never
adjudicate.**

### C. Truthfulness
Fabricated testimonial or result claim · unverifiable social proof · untrue
scarcity · credentials not held · untraceable first-hand claim · generated
imagery of a real place · unmarked judgment presented as fact · forecast with no
divinatory basis · missing disclaimer.

### D. Platform and disclosure
Sponsorship disclosure present **in the post itself** · platform terms · no
engagement manipulation · third-party licences confirmed · LINE reviewed.

### E. Privacy and consent
Consent record present and verified · anonymisation sufficient (age + region +
occupation + situation can re-identify someone with no name) · photo permission
confirmed · photography restrictions honoured.

### F. Reputational
Comparative or disparaging content about other practitioners · shrine efficacy
comparison · content likely to offend a shrine or community · political or
discriminatory content · tone drift toward commodity fortune-telling.

## Step 3 — The adjacency check (mandatory)

For each CTA, read the preceding 2–3 sentences. A consequence, risk, or anxiety
statement adjacent to a CTA is assessed **as a unit**, even when neither half
would block alone. Proximity is part of the pattern.

## Step 4 — Traceability

Every first-hand claim: does `source_reference` resolve, and does
`verbatim_anchor` support it? An untraceable claim is a **domain C truthfulness
risk**, not just a QA gap — a published claim about a place the practitioner may
not have visited is a misrepresentation.

## Step 5 — Records, not assurances

Open the consent record. Open the permission record. Open the licence record.
**A missing record is blocking, not pending.**

## Step 6 — Write findings with rewordings

Per finding:

```
domain · severity · surface · location
what_is_wrong · why_it_is_a_risk · legal_basis
current_text → required_text        ← binding on A08 / A10
```

Supply `required_text` wherever a compliant expression of the same intent exists.
Where the claim itself is the problem, say `remove` and explain why.

Common rewordings:

| Current | Required |
| --- | --- |
| `必ず○○になります` | `占術上はこう見ます` |
| `願いが叶います` | `気持ちを整える機会になります` |
| `行かないと運気が下がります` | remove — no compliant reworing exists |
| `病気が治ります` | `体調の不安は医療機関にご相談ください` |
| `今が買い時です` | remove — financial claims are out of scope |
| `別れるべきです` | present considerations; the reader decides |

## Step 7 — Verdict

```
any blocking finding             → block
any escalate_to_professional     → block
only rewordings to apply         → clear_with_conditions
nothing found                    → clear
```

Uncertainty never resolves toward `clear`.

## Output
`schemas/risk_assessment.schema.json`. A28 enforces it verbatim.
