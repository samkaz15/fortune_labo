# Prompt — Batch Composition

## Task
Assemble finished posts into a batch, set the posting order, and write the
markdown batch file.

X Content Agent ships **batches, not individual posts**, so that variety is
designed rather than hoped for.

## Balance checks — all blocking

| Check | Limit | Why |
| --- | --- | --- |
| Category share | No category above ~40% | `categories.md` |
| Category C share | Kept lowest of the four | The drift category |
| Tier mix | X-C never the majority | `positioning.md` §5 |
| Angle repetition | No angle more than twice | `rules.md` §4.3 |
| Hook pattern repetition | No pattern more than twice | Same |
| CTA type repetition | No type more than twice | `writing.md` §8 |
| `booking` CTA | At most once per batch | Authority channel, not a sales channel |
| No CTA at all | Roughly half the batch | A CTA every time reads as marketing |
| Same-theme posts | Never consecutive | `responsibilities.md` §B |

A batch that fails a check is rebalanced, not shipped with a note.

## Posting order

1. **Seasonal posts against their windows first.** Everything else fills around
   them. A 節句 post one day late is worth nothing
2. Spread same-theme angles as far apart as possible
3. Alternate categories — two Category C posts in a row makes the account look
   like every other 開運 account
4. Put the strongest X-A post where cadence is most established, not first —
   a new week's first post gets the least reach

## Status handling

| Status | Goes in the batch? |
| --- | --- |
| `draft` | Yes — into QA |
| `fact_check_pending` | Listed, but cannot be scheduled until resolved |
| `blocked` | Listed in the blocked section with what is missing and who supplies it |
| `rejected` | Not listed. Recorded in the plan's `dropped_reason` |

**A blocked post does not block the batch.** It moves to the next one. Never
ship around a gap by softening the post until the gap stops mattering.

## Markdown batch file

Write to `content/sns/drafts/<YYYY-MM>/x.md`, extending the format that
directory already uses:

```
# X 投稿ドラフト — <YYYY-MM> バッチ

status: draft / QA未通過 / 人間承認前
文字数の注意（プレースホルダ置換後に再カウント）
ハッシュタグ方針

## <ID> ｜ <theme> ｜ Category <A-D> / <X-tier>
- 狙い:
- 切り口 (angle):
- 基盤 (basis):
- 依存: {{placeholders}}
- 事実確認: 要 / 不要 — 対象クレーム
- 主観明示: あり / なし
- 概算: 約NN字
- status:

（本文をコードブロックで）

## 投稿順の提案
## 発行できなかった枠
```

The JSON is the machine-readable form; the markdown is the human review surface.
**The markdown is generated from the JSON, never edited independently.**

## Before handing over

- [ ] Every post has ≥1 basis
- [ ] No unresolved `needs_verification` claim in any schedulable post
- [ ] Every `{{placeholder}}` listed in the batch file's dependency section
- [ ] Compliance self-check filled on every post, hooks included
- [ ] Seasonal posts have dates that are still achievable
- [ ] `grep -rn '{{' content/sns/drafts/<YYYY-MM>/x.md` output matches the
      declared placeholder list
- [ ] Any post whose first person makes a claim about the practitioner's actual
      practice is flagged for their confirmation (`rules.md` §4.4)

## Output
The batch markdown file, plus the `x_post` JSON set, handed to A28 QA.
