# Prompt — FAQ and Featured Snippet

## FAQ

### Only real questions
Sources, in priority order: the practitioner's real client questions, the brief's
`target_question` fields, SERP "People also ask", and search-console query data.

**Inventing questions to pad a page is a defect.** Three real questions beat ten
manufactured ones, and a manufactured FAQ block is visible to readers.

### Per question
- Phrased the way the reader would phrase it, not the way a marketer would
- Answered completely in 2–4 sentences, standalone (an FAQ answer may be shown
  out of context)
- No answer that is "it depends" with nothing following
- Same compliance rules as body copy — no guarantee, no fear frame, no medical /
  financial / legal adjudication
- A judgment inside an FAQ answer still needs its attribution marker

### Structured data
If the brief lists `FAQPage`, the FAQ must contain genuine Q&A the page actually
answers. Marking up manufactured questions to win rich results is exactly the
kind of thing that costs a site its rich results.

## Featured snippet

Only where the brief marks a section `featured_snippet_target: true`. **At most
one per piece.**

### Shape follows the query

| Query shape | Snippet shape |
| --- | --- |
| `○○とは` | Definition, 1–2 sentences, first line of the section |
| `○○ 方法` / `やり方` | Ordered steps, each step self-contained |
| `○○ いつ` | Direct temporal answer, then the reason |
| `○○ 違い` | Comparison in a small table or parallel sentences |
| `○○ 持ち物` / list queries | Short unordered list |

### Rules
- The answer opens the section — no preamble before it
- 40–60 Japanese characters for the core answer
- True and complete standing alone, with no surrounding context
- **Never compressed into a guarantee.** `参拝すると運気が上がります` is not an
  acceptable snippet even if it would win the position. Compression pressure is
  precisely where guarantees sneak in — this is the highest-risk sentence in the
  whole draft.
- If the honest answer cannot be stated in snippet form without becoming a
  claim you may not make, **do not target the snippet.** Record why, and let A07
  know the brief's snippet target was not achievable.

## Output
FAQ block and `featured_snippet_block` fields of Master Content.
