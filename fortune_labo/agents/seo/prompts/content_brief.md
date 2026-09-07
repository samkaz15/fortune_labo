# Prompt — Content Brief Generation

## Task
Convert an approved SEO opportunity into a brief for Content Agent.

## Path selection — do this first

**Path 1 (Tier A, first-hand):** shrine reports, annual outlooks, forecast reviews.
**A brief on this path may only be issued when a completed visit record exists.**
No `visit_record_id` → no brief. This is a hard rule, not a preference
(`rules.md` §2).

**Path 2 (Tier B/C, standard):** method explainers, situation guides, service pages.

## Section sourcing

Tag every outline section with `source_requirement`:

| Value | Meaning |
| --- | --- |
| `visit_notes` | Must derive from the human visit. AI structures, never originates. |
| `practitioner_judgment` | Must derive from the practitioner's own reading and stated basis. |
| `research` | Verified external facts. |
| `ai_structurable` | AI may draft freely. |

If more than half the outline is `ai_structurable`, the page probably fails the
one-line test. Reconsider it.

## Title — your responsibility

You own titles, so title compliance is on you. A compliant body under a
fear-framed title is still a violation. Forbidden: fear framing
(`行かないと運気が下がる`), guaranteed outcomes (`願いが叶う`), efficacy
rankings (`効く神社ランキング`).

"Visiting is good" is permitted. "Not visiting is bad" is not.

## Mandatory elements
- Outbound internal link to the booking page (all Tier A and B pages)
- Standard disclaimer (all shrine and forecast pages)
- Subjectivity marking requirement
- Divinatory basis requirement (annual outlooks)
- Photo permission status — publication blocked while `pending`

## Output
`schemas/content_brief.schema.json`.
