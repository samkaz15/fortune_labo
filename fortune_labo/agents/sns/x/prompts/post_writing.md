# Prompt — Post Writing

## Task
Turn one angle from an approved `x_content_plan` into an `x_post`.

## Step 1 — Classify the facts, before writing

List every factual claim the post will make. For each: `verified` /
`needs_verification` / `unverifiable`, with source candidates.

Do this **first**. A well-written post resting on an invented fact has to be
thrown away entirely, not edited. Emit `x_fact_check_request` for anything not
already verified.

## Step 2 — Confirm the basis

Which of `firsthand` / `practitioner_view` / `verified_fact` / `mechanism` does
this post rest on? Record it.

- Empty → do not write the post
- `mechanism` alone on a 運気 subject → do not write the post
- `firsthand` → a `visit_record_id` is mandatory
- Category A → must include `verified_fact`
- Category B → `mechanism` **plus** one other
- Category D → `verified_fact` plus one other

## Step 3 — Write to the structure

```
① Hook            最初の1〜2行。See prompts/hook_writing.md
② 情報            読者が「知らなかった」と思える内容
③ 理由            なぜそうなのか  ← the reason anyone saves this
④ 現代への置き換え  実際にできる行動
⑤ CTA             optional — roughly half a batch has none
```

**③ is the post.** Most 開運 accounts have ① ② ⑤ and nothing else. If you
cannot write ③, step 2 failed — go back rather than shipping.

**④** turns knowledge into something actionable. Category A posts may stop at
③, but should still tell the reader what to notice.

## Step 4 — Apply the style rules

`writing.md` §4. The ones that break most often:

- 一文一義. Roughly 40 全角文字 as a sentence ceiling
- Line breaks that pace the post; blank lines between 1–3 line paragraphs
- 結論を先延ばししない
- No 記号・絵文字 by default
- Every number needs a source
- Subjective claims: 「私の見立てでは」「〜と感じています」
- Historical uncertainty: 「〜と言われています」「諸説あります」

## Step 5 — Multiple viewpoints, for Category B and D

The brief requires 「なぜその行動なのか」 from more than one viewpoint:

| 昔からの考え方 | 心理・行動面 | 現代生活への取り入れ方 |
| --- | --- | --- |
| `verified_fact` | `mechanism` | the ④ section |

Two viewpoints is the working minimum. Three is the target. One is thin.

## Step 6 — Self-compliance check

Run `rules.md` §2 against the post **and the hook**. Fill the `compliance`
object honestly — it is a record, not a formality. QA is the second gate,
not the first.

The three that recur:

| Instead of | Write |
| --- | --- |
| 「金運が上がります」 | 「金運を意識するなら、昔から○○と言われてきました」 |
| 「やらないと運気が下がります」 | 「やってみると、生活が整うきっかけになります」 |
| 「必ず」「絶対」「確実に」 | Remove. There is no compliant version |

Set `risk_level`: `high` when the post touches 金運・健康・人生の判断 or names a
specific shrine — and then make an explicit disclaimer decision.

## Step 7 — Count and mark

- Character count **after** placeholder substitution (~140 全角文字 budget)
- Over budget → cut, or make it a thread (max 5, first post stands alone)
- Mark every unfilled business fact as `{{placeholder}}`. Never guess one
- Choose `cta_type` against the batch mix, not by habit

## Output
`schemas/x_post.schema.json`.

Set `status`:
- `draft` — everything resolved, ready for QA
- `fact_check_pending` — claims outstanding
- `blocked` — missing basis, visit record, or business fact. Fill
  `blocked_reason` with what is missing and who can supply it

A blocked post is a legitimate output. Shipping around the gap is not.
