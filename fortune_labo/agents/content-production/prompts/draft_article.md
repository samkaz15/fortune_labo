# Prompt — Draft an Article

## Task
Produce Master Content from one Content Brief.

## Step 1 — Validate the commission
Reject and return the brief if it fails schema validation, if a first-hand
`content_type` lacks `visit_record_id` / `practitioner_input_id`, or if any
outline section lacks a `purpose` you can actually write to.

## Step 2 — Reconcile every section with its source

| `source_requirement` | Must resolve to | If absent |
| --- | --- | --- |
| `visit_notes` | The visit record | **Gap. Do not write.** |
| `practitioner_judgment` | The practitioner input + its divinatory basis | **Gap. Do not write.** |
| `research` | A checkable, citable source | **Gap. Do not write.** |
| `ai_structurable` | The brief | Write |

Build `source_map` as you go, with a `verbatim_anchor` quoting the source line
each section rests on. If a structural section is gapped, emit a blocking Content
Gap Report and stop.

## Step 3 — Write in this order

**Headings → body → lead → FAQ/snippet → CTA → meta.**

Never the lead first. A lead written before the body promises things the body
does not deliver.

### Headings
One H1 from `title_candidates` (≤60 chars, compliance-clean). H2/H3 follow the
outline. Wording may be refined; adding, removing, or reordering sections
requires a recorded `structure_deviation`.

### Body, per section
Answer the `target_question` → support it → bridge to the next.

- One idea per paragraph, 2–4 sentences
- Concrete over abstract: `12月下旬の朝、参道は霜が降りていました` beats
  `冬は厳かな雰囲気です`
- Keep the subject clear — Japanese drops subjects easily, and ambiguity about
  *who observed what* is a compliance risk
- Attribution visible in the prose: visit material carries its date,
  judgment carries `私の見立てでは`, research names its source
- No filler transitions, no padding, no cosmetic lists

### Lead (3–5 sentences)
Name the reader's situation from `reader_state` → state what this page resolves →
make `unique_value` visible. **If the query has a short answer, it goes here.**

Forbidden openings: dictionary definitions, `皆さんは○○をご存じでしょうか`, and
any anxiety hook.

### FAQ
Only real questions, from client questions, PAA, or the brief. Each answer
standalone in 2–4 sentences. No padding questions.

### Featured snippet
Only where the brief marks a section (max one). Direct, self-contained answer in
the first 40–60 characters. **Never compress into a guarantee** — a snippet that
wins the position by promising an outcome is a violation.

### CTA
To the brief's `primary_type`, `placement`, and `copy_direction`. Calm and
specific. No urgency-through-anxiety, no untrue scarcity, no guaranteed outcome.
Exactly one primary CTA — do not add others.

### Meta descriptions
2–3 candidates, ≤120 Japanese characters, accurate to what is actually on the
page, primary keyword natural, compliance-screened exactly like a title.

## Step 4 — Place internal links
Targets and anchors come from the brief. You choose where in the prose they sit —
where a reader would want them, not clustered at the end. No `こちら` anchors.
Booking link present for Tier A/B. Unlisted link ideas go in `suggested_links`,
never straight into the body.

## Step 5 — Mark `sns_source_blocks`
Flag the strongest observation, the clearest one-sentence answer, the most
quotable judgment, and the visual moment. A10 rewrites them. **You do not write
social copy.**

## Step 6 — Self-check (11 points, `../workflow.md`)
Any fail → fix and re-run. The draft does not leave A08 with a known failure.

## Output
`schemas/master_content.schema.json` → `content/drafts/MC-xxxx.json`,
plus `schemas/content_gap_report.schema.json` if any gap was found.
