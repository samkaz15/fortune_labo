# Content Production Agent — Outputs

## Artifact catalogue

| Artifact | Schema | Consumer | Stored at |
| --- | --- | --- | --- |
| **Master Content** | `master_content.schema.json` | A10, A28, A30, Codex | `content/drafts/MC-xxxx.json` |
| Content Gap Report | `content_gap_report.schema.json` | A07, human | `content/gaps/` |

---

## Master Content — the canonical version of a piece

`MC-xxxx`. Everything downstream derives from this one artifact: A10 adapts it
per channel, A28 checks it, A30 assesses it, Codex publishes it.

```
identity     id, brief_id, revision, status, created_at
document     h1, lead, sections[], faq[], cta, disclaimer
metadata     meta_description_candidates[], slug_suggestion,
             structured_data_intent[]
traceability source_map[], attribution_markers[]
signals      featured_snippet_block, internal_links_placed[],
             suggested_links[]
selfcheck    self_check{}, structure_deviations[], seo_conflicts[],
             readability{}
handoff      sns_source_blocks[], open_questions[]
```

### Traceability is the point

`source_map` is what makes the no-fabrication rule **auditable rather than
aspirational**. Every section carries:

```
section_id · source_requirement · source_reference · verbatim_anchor
```

`source_reference` must resolve to a real record. A `visit_notes` section with a
null `source_reference` is schema-invalid — the constraint is enforced by the
data structure, not by A08's good intentions.

`verbatim_anchor` quotes the specific line of source material the section rests
on, so A28 and the practitioner can verify the claim without re-reading
everything.

### Content is stored as structured text, not HTML

A08 emits **Markdown-flavoured plain text** per section. HTML, schema markup,
WordPress blocks, and template concerns are Codex's job
(`../../../docs/agents/CODEX-INTERFACE.md`). Keeping the master content
presentation-free is what allows A10 to re-cut it per channel without parsing
markup.

### `sns_source_blocks`

Pre-identified passages A10 can build from: the strongest observation, the
clearest single-sentence answer, the most quotable judgment, the visual moment.
A08 marks them; A10 rewrites them per channel. A08 never writes social copy.

---

## Content Gap Report

Emitted whenever the brief cannot be executed **honestly**. Expected and normal.

```
id, brief_id, gaps[], blocking, created_at

gaps[]:
  section_heading
  source_requirement
  what_is_missing
  why_it_cannot_be_written        e.g. "no visit record for this shrine"
  what_would_resolve_it           e.g. "visit notes incl. December condition"
  requested_from                  human | strategy | research | seo
```

`blocking: true` means the piece cannot proceed at all. `false` means the rest
of the draft is deliverable with the gapped sections marked
`status: awaiting_source`.

**A gap is never resolved by writing around it.** Writing a plausible paragraph
where a visit record should be is the failure this entire agent is designed to
prevent.

---

## Handoff contracts

**→ A10 SNS Content**
Sends: Master Content plus `sns_source_blocks`. A10 rewrites per channel;
A08 does not pre-write social copy.

**→ A28 QA**
Sends: Master Content + the originating brief. QA checks the draft *against the
brief*, so `structure_deviations` and `seo_conflicts` must be declared — an
undeclared deviation reads as a defect.

**→ A30 Compliance/Risk**
Sends: Master Content with `attribution_markers`, so subjective claims can be
distinguished from asserted facts mechanically rather than by re-reading prose.

**→ A07 Content Strategy**
Sends: Content Gap Reports, `structure_deviations`, `suggested_links`,
`seo_conflicts`. A07 reworks the brief; A08 does not rework the strategy.

**→ Codex**
Sends: nothing directly. Master Content reaches Codex only **after QA and human
approval**, per `/AGENTS.md`. A08 has no publishing path.

---

## Revision handling

Each QA cycle produces a new `revision`, with `revision_notes` recording what
changed and which finding it addressed. Master Content is versioned in Git;
prior revisions are never overwritten in place, so the QA trail stays auditable.
