# Prompt — Theme Selection

## Task
Choose the themes for the next X batch and emit one `x_content_plan` per theme.

## Order of operations

**1. Seasonal windows first.**
What opens in the next 6 weeks? Work backward including fact-check turnaround
(`workflow.md` §Seasonal backward planning). Anything already past its post-by
date is lost — do not draft it, note it as a miss.

**2. Basis inventory second.**
What `firsthand` and `practitioner_view` material exists **today**? Not what
could be obtained in principle. An empty inventory caps the whole batch at
Tier X-B and below, and that is a fact to report, not to work around.

**3. Then draw themes**, weighted:

```
seasonal urgency  >  real client questions  >  SEO Agent Tier A/B gaps
                  >  approved content clusters  >  existing articles
```

Client questions outrank keyword sources. They are the literal language of
people who already paid (`agents/seo/inputs.md`).

## The schedulability test

For each candidate theme, ask in this order:

1. **Which bases are available today?** None → not schedulable. Emit it as a
   request to the practitioner or Research Agent, not as a draft.
2. **How many real angles does it support?** One → weak theme, deprioritise.
3. **What is the verification load?** Heavy load against a near seasonal
   deadline → move it to the next batch or start the fact-check now.
4. **Which category?** Check it against the batch mix before committing.

## Category mix

No category above ~40% of a batch. Target steady state (`categories.md`):

| A 歴史・日本文化 | B 開運アクション | C 占い・開運 | D 食・生活 |
| --- | --- | --- | --- |
| ~35% | ~30% | ~20% | ~15% |

**C is deliberately lowest.** It is the category this account will drift toward
if unchecked, and the one that most resembles what every other 開運 account
already posts.

## Do not select

- A theme whose only available basis is `mechanism` and whose subject is 運気
- A theme requiring shrine experience when no visit record exists
- A theme you cannot name a source candidate for, when it is Category A or D
- A theme already covered in the last two batches from the same angle

## Output
`schemas/x_content_plan.schema.json`, one per theme.
Themes that failed the schedulability test are still emitted — with
`status: parked` and `missing_basis` filled in, so the gap is visible rather
than silently dropped.
