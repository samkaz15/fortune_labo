# Prompt — Keyword Evaluation

## Task
Classify and score candidate keywords for fortune_labo.

## Input
A list of candidate keywords with any available context (source, volume estimate,
observed SERP).

## Procedure

**Step 1 — Tier assignment (before any scoring).**

| Tier | Definition |
| --- | --- |
| A | Shrine names, shrine + 御朱印/祭事/参拝, region + shrine + purpose, annual outlook, practitioner name |
| B | Situational intent with booking potential: 対面鑑定 + 地域, 事業承継 時期, 悩み + 相談 |
| C | Divination-method explainers tied to the practitioner's own system |
| D | Generic horoscope/free-fortune/generic tarot meanings, efficacy rankings |

**Tier D is excluded here and is never scored.** Record it once as
`excluded_tier_d` so it is not rediscovered, then move on.

**Step 2 — Score the rest.**

```
priority_score = (booking_potential * 3)
               + (moat_fit * 3)
               + (volume_normalised * 1)
               - (difficulty_normalised * 2)
               + (seasonal_urgency * 2)
```

`booking_potential` (0–5): how close is this searcher to booking a paid reading?
`moat_fit` (0–5): does winning this require a physical visit or a named
professional judgment?

Volume is deliberately the weakest positive term. Do not override this.

**Step 3 — Winnability.**
If the SERP is dominated by shrine official sites, national media, or a map pack
and fortune_labo would be indistinguishable, mark `not_winnable` and drop it.
Declining to compete is a valid and expected output.

**Step 4 — Cannibalisation.**
Map each keyword cluster to exactly one canonical URL. Flag conflicts.

## Output
Array conforming to `schemas/keyword_register.schema.json`.
State volume source and confidence for every estimate.
