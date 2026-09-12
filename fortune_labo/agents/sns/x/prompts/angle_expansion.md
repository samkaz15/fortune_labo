# Prompt — Angle Expansion

## Task
Take one approved theme and expand it into the distinct posts it genuinely
supports. **One theme yields several posts, not one.**

This is the production mechanic that makes sustained cadence possible without
new research every day (`positioning.md` §6).

## The angle set

`writing.md` §3: 教養型 / 誤解型 / 実践型 / 開運型 / 歴史型 / 問題提起型 /
比較型 / 季節型 / 失敗型 / 質問回答型.

Each angle is **a different entry point for a different reader**, not a rewrite.

## Method

For each angle, before writing anything, answer:

1. **Who arrives through this door?** A reader who already meditates is not the
   reader who thinks meditation is emptying your mind.
2. **What does this angle need that the others do not?** A different fact, a
   different basis, a different action at the end.
3. **What is the 理由 section here?** If it is the same 理由 as another angle,
   this is not a separate post.

## The duplication test

Draft the 情報 and 理由 of two angles side by side. If they say the same thing
in different words, **one of them was not a real angle.** Drop it. Shipping both
is template farming (`rules.md` §4.3).

## Tier can differ across angles of one theme

The same theme yields posts at different tiers, and that is expected:

| Theme: 瞑想 | Angle | Basis | Tier |
| --- | --- | --- | --- |
| 瞑想とは何をするものなのか | 教養型 | `verified_fact` | X-B |
| 瞑想＝無になることではない | 誤解型 | `verified_fact` + `mechanism` | X-B |
| 朝5分のやり方 | 実践型 | `mechanism` + `practitioner_view` | X-C |
| 運気を整えたい人にすすめる理由 | 開運型 | `practitioner_view` | **X-A** |
| 日本人が心を整えてきた時間 | 歴史型 | `verified_fact` | X-B |
| 「毎日やらないと意味がないですか」 | 質問回答型 | `practitioner_view` | **X-A** |

Note where X-A appears: wherever the practitioner's own judgment carries the
post. That is the cheapest route to Tier X-A when no visit record exists — and
the reason 質問回答型 and 開運型 are worth the practitioner's time to answer.

## Scheduling constraint

- Angles from one theme are **spread across the calendar**, never consecutive
- No angle used more than twice per batch
- Each post stands alone. No 「前回の続き」. Reposts strip context

## Output
Fill the `angles` array of the theme's `x_content_plan`.
Angles considered and dropped are recorded with `dropped_reason` — so the same
dead angle is not re-proposed next month.
