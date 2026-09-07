# Prompt — Content QA (layers 2, 3, 4)

Run only after layer 1 (compliance, A30) has returned. A blocking finding in
layers 1–3 stops the run.

---

## Layer 2 — Fact

| Check | Blocking? |
| --- | --- |
| Every factual statement is marked as fact, judgment, or general tendency | Blocking if a judgment reads as fact |
| Every `research` section cites a source | Blocking |
| The cited source actually says this | Blocking |
| Numbers match the source exactly | Blocking |
| Dates real, consistent internally and with the visit record | Blocking |
| Proper nouns correct — shrine, deity, place, person names | Major |
| Access details, hours, fees traceable | Major |
| Time-bound facts still true today | Major |
| No self-contradiction, and no contradiction with a published page | Major |

**A number with no source is invented.** "Approximately" does not convert an
unsourced figure into a sourced one. Check the source; do not accept an assurance
that it is right.

---

## Layer 3 — First-hand verification (the moat check)

For every section where `source_requirement` is `visit_notes` or
`practitioner_judgment`:

```
1. Does source_map contain this section?            no → BLOCKING
2. Does source_reference resolve to a real record?  no → BLOCKING
3. Does verbatim_anchor appear in that record?      no → BLOCKING
4. For each concrete detail in the section:
     is it supported by the record?                 no → BLOCKING (extrapolation)
```

### Detecting extrapolation

Compare **claim against anchor**, not impression against impression.

| Source says | Draft says | Verdict |
| --- | --- | --- |
| `12月の朝、参道に霜` | `12月の朝、参道に霜が降りていました` | Pass |
| `12月の朝、参道に霜` | `空気は澄み、物音ひとつしませんでした` | **Blocking — extrapolation** |
| `拝殿は改修中` | `拝殿は改修中でした（2025年12月時点）` | Pass |
| `拝殿は改修中` | `改修は春には終わる見込みです` | **Blocking — invented** |

Atmospheric, plausible, and unsourced is still fabricated.

### Also blocking in this layer

- Visit date absent or not matching the visit record
- Photo permission not `confirmed` for any image in use
- Imagery generated to depict a real place
- A judgment with no attribution marker
- A forecast with no stated divinatory basis
- `case_reflection` content with no recorded consent
- A first-hand claim in a channel asset that does not trace to the same source map

---

## Layer 4 — Editorial

| Check | Severity |
| --- | --- |
| **Does the piece answer its own `target_question`s?** | **Blocking** |
| Padding — sections that exist to add length | Major |
| Japanese naturalness; no translationese | Major |
| Logical flow; sections build rather than sit side by side | Major |
| Lead delivers the answer where a short answer exists | Major |
| FAQ answers standalone | Major |
| Brand voice consistent with the practitioner | Major |
| Typos, okurigana, punctuation | Minor |
| 敬体/常体 consistency | Minor |
| Redundancy | Minor |
| Sentence and paragraph length | Minor |
| Terminology consistency | Minor |
| Heading informativeness | Minor |

Information sufficiency is blocking: a page that ranks and does not answer the
question is exactly the failure this pipeline exists to prevent.

---

## Output
Findings appended to `schemas/qa_report.schema.json`, each with evidence, a
required fix, an owner, and a location.
