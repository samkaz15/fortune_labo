# Content Production Agent — Workflow

## Position in the pipeline

```
A07 Content Strategy ── content_brief.json (CB-xxxx)
        │
        ▼
┌──────────────────────────────────────────────┐
│ A08 CONTENT PRODUCTION                       │
│                                              │
│  1 validate      schema + brief completeness │
│  2 reconcile     every section → its source  │
│  3 gap check     STOP and report if missing  │
│  4 structure     H1 + heading hierarchy      │
│  5 lead          answer first, not later     │
│  6 body          section by section          │
│  7 faq + snippet where briefed               │
│  8 cta + links   to the brief's direction    │
│  9 meta          2–3 compliance-screened     │
│ 10 self-check    11-point gate               │
└──────────────────┬───────────────────────────┘
                   │  master_content.json (MC-xxxx)
        ┌──────────┴──────────┐
        ▼                     ▼
  A10 SNS Content       A28 QA ◄── A30 Compliance/Risk
                              │
                              ▼
                       HUMAN APPROVAL
                              ▼
                       Codex ──► WordPress
                              ▼
                        A18 Analytics ──► A06
```

---

## Step 3 is the one that matters

```
for each section in brief.outline:
    if section.source_requirement in (visit_notes, practitioner_judgment, research):
        material = resolve(section.source_reference)
        if material is None:
            record_gap(section)          # DO NOT WRITE THIS SECTION
            continue
    write(section)

if any gap is structural (the piece's core rests on it):
    emit Content Gap Report with blocking = true
    STOP
else:
    emit partial draft + Content Gap Report with blocking = false
```

**There is no branch in which a missing source produces written prose.** A
writing model's default when material is thin is to produce something fluent and
plausible. That default is the failure mode this step exists to interrupt.

---

## Drafting order (deliberate)

1. **Headings first** — the full skeleton before any prose. Reveals structural
   problems while they are cheap to fix.
2. **Body sections second** — before the lead. You cannot introduce a piece you
   have not written.
3. **Lead third** — now it can promise what the page actually delivers.
4. **FAQ and snippet fourth** — they draw on finished body content.
5. **CTA and meta last** — they summarise a finished piece.

Writing the lead first is how pages end up promising something the body never
delivers.

---

## Self-check gate (before handoff)

| # | Check | Fail action |
| --- | --- | --- |
| 1 | Every outline section present | Add, or record `structure_deviation` |
| 2 | Every first-hand claim traceable in `source_map` | Remove the claim or gap it |
| 3 | Every judgment carries an attribution marker | Add marker |
| 4 | No forbidden expression (`rules.md` §3–§4) | Reword |
| 5 | Disclaimer present where required | Add |
| 6 | Booking link present (Tier A/B) | Add |
| 7 | One H1, no skipped heading levels | Fix |
| 8 | FAQ answers standalone and compliant | Fix |
| 9 | Meta candidates compliance-screened, ≤120 chars | Fix |
| 10 | Lead answers the query rather than deferring it | Rewrite lead |
| 11 | No section is padding | Cut it |

Any fail → fix and re-run. The draft does not leave A08 with a known failure.

---

## Revision loop with A28 / A30

```
A08 draft (rev 1)
     ▼
A28 QA  ──► findings by severity
     │        blocking → must fix
     │        major    → fix or contest with reasoning
     │        minor    → fix
     ▼
A30 Compliance/Risk ──► binding rewordings (not negotiable on style grounds)
     ▼
A08 revision (rev 2) + revision_notes mapping each change to its finding
     ▼
A28 re-check ──► pass ──► HUMAN APPROVAL ──► Codex ──► publish
```

**Escalation:** if a piece reaches revision 3 without passing, A08 stops
revising and returns it to A07. Three failed revisions means the brief was
defective, and continuing to rewrite prose against a broken commission wastes
practitioner review time.

A08 may contest a finding with reasoning. It may never ignore one, and it may
never mark its own draft as passed.

---

## Handling a conflict between SEO and the reader

```
if brief.seo_requirement would produce a sentence a reader would not want:
    write for the reader
    record seo_conflicts[] { requirement, why_it_harms_the_reader, what_was_done }
    A28 routes it to A06 for adjudication
```

Silent compliance and silent non-compliance are both violations. The conflict is
declared and resolved by the agent that owns the tradeoff.

---

## Cadence

A08 is **event-driven, not scheduled.** It runs when a brief is issued or a QA
report returns. It has no independent publication rhythm, because production
volume is set by A07's capacity-bounded calendar, not by A08's throughput.

| Trigger | Action |
| --- | --- |
| New brief issued | Validate → draft → self-check → handoff |
| Source material arrives for a parked gap | Resume the gapped sections |
| QA report returns | Revise, map each change to its finding |
| A30 reworing issued | Apply verbatim, re-run self-check |
| Brief revised by A07 | Restart from step 1; do not patch against a stale brief |
