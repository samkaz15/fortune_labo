# Compliance/Risk Agent — Workflow

## Two review points, not one

```
A07 brief with sensitive_domain
        │
        ▼
   A30 PRE-DRAFTING REVIEW ──► treatment_rules ──► A08 drafts within them
        │
        ▼
A08 master_content / A10 channel_content
        │
        ▼
   A28 QA delegates layer 1
        │
        ▼
┌────────────────────────────────────┐
│ A30 ASSESSMENT                     │
│  A solicitation risk               │
│  B sensitive domain                │
│  C truthfulness / representation   │
│  D platform / disclosure           │
│  E privacy / consent               │
│  F reputational                    │
└────────────────┬───────────────────┘
                 │  risk_assessment.json (clear | conditions | block)
                 ▼
        A28 enforces verbatim
                 ▼
          HUMAN APPROVAL
                 ▼
         WordPress / SNS
                 ▼
   A30 MONITORING ──► incident ──► unpublish recommendation
```

**Pre-drafting review is the cheap one.** A treatment rule issued before A08
writes costs one revision. The same rule issued after costs three, and burns
practitioner review time.

---

## Assessment procedure

### Step 1 — Establish the surface list

Site content: title, H1, every heading, lead, body, FAQ, CTA, meta description,
disclaimer, image alt text.

Channel content: hook, body, CTA, every hashtag, every on-screen text frame,
every slide, thumbnail text and concept, video title, video description.

**Every surface is assessed.** A compliant body under a fear-framed title is a
violation; so is a clean caption under a slide reading `願いが叶う`.

### Step 2 — Domain sweep

Run domains A–F (`responsibilities.md`). The verdict is the **worst result across
all six**, not an average.

### Step 3 — The adjacency check

```
for each CTA:
    examine the 2-3 sentences preceding it
    if they state a consequence, a risk, or an anxiety:
        assess the pair as a unit
```

Neither half needs to be individually blocking. `最近うまくいかないと感じていませんか`
followed by a booking CTA is the pattern the 2023 solicitation rules describe,
assembled from two innocuous halves. **Proximity is part of the pattern.**

### Step 4 — Traceability verification

Every first-hand claim: does `source_reference` resolve, and does
`verbatim_anchor` support it? An untraceable claim is a **truthfulness risk**
(domain C), not merely a QA gap — a published claim about a place the
practitioner may not have visited is a misrepresentation.

### Step 5 — Records, not assurances

Consent, photo permission, and licences are **verified against records**. An
assurance is not a record. A missing record is blocking, not pending.

### Step 6 — Write the rewordings

For each finding, supply `required_text` where a compliant expression of the same
intent exists. Where the claim itself is the problem, say `remove` and explain
why no reworing can fix it.

**Wherever possible, reword rather than refuse.** A compliance function that only
says no gets routed around, and a routed-around gate protects nothing.

### Step 7 — Verdict

```
any blocking finding                → block
any escalate_to_professional        → block
only rewordings to apply            → clear_with_conditions
nothing found                       → clear
```

---

## Incident response — published content

Highest-priority path in this agent. Everything else waits.

```
1. CONFIRM        is it actually a violation, or a style concern?
2. ASSESS         severity, exposure window, how many pages/posts
3. NOTIFY HUMAN   immediately — with an unpublish recommendation for
                  anything blocking
4. CONTAIN        recommend unpublish or edit; A30 does not act on
                  production itself
5. SWEEP          find every other artifact with the same pattern
6. ROOT-CAUSE     which check should have caught it, and why it did not
7. RULE CHANGE    add the check so it cannot recur
8. REGISTER       record as an incident with its full history
```

Step 5 is not optional. A pattern that got through once got through a process,
and the same process produced everything else.

The exposure window matters: **3 years from realisation, 10 years from the act**.
A violation published two years ago is still live exposure, so incident response
covers the back catalogue, not just recent content.

---

## Monitoring published content

| Cadence | Sweep |
| --- | --- |
| **Monthly** | New publications spot-check; complaint and LINE block-rate review; platform warnings |
| **Quarterly** | Regulatory watch; full re-sweep of high-risk content types (forecasts, case reflections, sensitive-domain pages); risk register review; accepted-risk review dates |
| **On rule change** | Full back-catalogue sweep against the new rule |
| **On incident** | Pattern sweep across everything published |

A rising LINE block rate is investigated as a **compliance signal first** and a
performance signal second. Blocks are what anxiety-framed push messaging produces,
and a block is permanent.

---

## Escalation triggers

| Trigger | Route | Timing |
| --- | --- | --- |
| Genuine legal interpretation question | **Qualified professional** via the human | Blocking |
| Compliance risk in published content | **Human — unpublish recommendation** | Immediate |
| Unverified photo permission on a live page | Human | Immediate |
| Consent record missing for published client content | Human — unpublish | Immediate |
| Platform warning or takedown | Human + A10 | Immediate |
| A28 or any agent asks to downgrade a blocking finding | **Refuse. Record. Escalate to A01.** | Immediate |
| Business pressure applied to a compliance decision | A01 + human, on the record | Immediate |
| Accepted risks accumulating in one domain | A01 — systemic pattern | Quarterly |
| Regulatory change affecting published content | Human + all content agents | On detection |
| Same finding pattern across three artifacts | Owning agent — process problem | Weekly |

---

## What A30 never does

- Publish, unpublish, edit, or deploy anything itself — it **recommends**, a
  human decides, Codex executes
- Clear content because a deadline is close
- Downgrade its own blocking finding under pressure
- Guess at a legal interpretation instead of escalating
- Accept a risk — **only a human may accept a risk**, on the record
- Remove an accepted risk from the register
