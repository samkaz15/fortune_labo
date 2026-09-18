# X Content Agent — Outputs

Every output conforms to a schema in `schemas/`. Free-form output is not
accepted by downstream agents.

## Artifact catalogue

| Artifact | Schema | Consumer |
| --- | --- | --- |
| **X Post** | `x_post.schema.json` | A28 QA → Human → X |
| **X Content Plan** | `x_content_plan.schema.json` | Internal state; A07 for review |
| **X Fact-Check Request** | `x_fact_check_request.schema.json` | A29 Fact-Check via A28 QA |
| **X Performance Record** | `x_performance_record.schema.json` | A18 Analytics → A01/A06 |
| Batch draft file | Markdown, `content/sns/drafts/<YYYY-MM>/x.md` | Human reviewer |

---

## X Post — the primary unit

The format requested in the implementation brief, extended with the fields this
repository requires to enforce its own rules.

```json
{
  "category": "",
  "theme": "",
  "target": "",
  "angle": "",
  "hook": "",
  "body": "",
  "cta": "",
  "hashtags": [],
  "source_required": true,
  "fact_check_required": true,
  "risk_level": "low",
  "repurpose_candidates": []
}
```

Those twelve fields are present and required, unchanged. Added on top:

| Added field | Why it exists |
| --- | --- |
| `id` | Stable reference across QA, approval and analytics |
| `status` | `draft` / `fact_check_pending` / `qa_pending` / `approved` / `published` / `blocked` / `rejected` |
| `x_tier` | `positioning.md` §5. Makes the moat position machine-visible |
| `basis` | **The central constraint.** `rules.md` §1.1 — an empty array cannot be emitted |
| `hook_candidates` | `writing.md` §7 requires ≥3 and a recorded reason |
| `factual_claims` | Per-claim verification state and source candidates (`rules.md` §3.5) |
| `compliance` | Explicit self-check against `rules.md` §2 before QA sees it |
| `placeholders` | Unfilled business facts. Publication is gated on this being empty |
| `thread` | Thread structure where a single post is insufficient |
| `char_count` | Post-substitution weighted count (`writing.md` §4) |
| `seasonal_window` | Post-by date where the theme is time-bound |
| `blocked_reason` | Required when `status` is `blocked` |

`basis`, `factual_claims` and `compliance` are not standard content fields. They
exist so that a rule violation is visible in the data structure rather than only
in prose — the same design choice `agents/seo/outputs.md` makes with
`moat_alignment` and `evidence_confidence`.

---

## Handoff contracts

**→ A28 QA Agent**

Sends: the `x_post`, plus any `x_fact_check_request` it generated.
QA gate order, inherited from `agents/seo/outputs.md`:

```
compliance → factual → first-hand verification → editorial → SEO → technical
```

On this channel, `compliance` and `factual` do the most work.
Receives back: `approved`, or `rejected` with the failing gate named.
A rejection on `factual` returns to the claim, not to the wording.

**→ A29 Fact-Check Agent** (via QA)

Sends: `x_fact_check_request` — one per post that has any claim not already
`verified`, listing each claim, its category, and its `source_candidates`.
Receives back: per-claim `verified` / `refuted` / `unverifiable` with sources.

A `refuted` claim removes the post, not just the sentence — usually the claim
was the reason the post existed.

**→ Human**

Sends: the batch draft file, with every post's status, basis, unresolved
placeholders, and unresolved claims visible.
Human approval is mandatory and cannot be delegated (`/AGENTS.md`).
Also sends: first-person practice claims requiring the practitioner's
confirmation (`rules.md` §4.4).

**→ A18 Analytics Agent**

Sends: the published post's `id`, `category`, `x_tier`, `angle`, `hook_pattern`,
`cta` type and publication timestamp, so performance can be segmented by
production decision rather than only by post.
Receives back: `x_performance_record`.

**→ A08 Content Production Agent**

Sends: `repurpose_candidates` — posts whose measured bookmark rate or reply
volume indicates the explanation was wanted at greater length.

**→ A06 SEO Agent / A01 Strategy Agent**

Sends: which themes produced bookmarks and profile clicks, as demand evidence;
reach-vs-basis escalations; verification-capacity warnings.

---

## Batch draft file format

Batches are written to `content/sns/drafts/<YYYY-MM>/x.md`, extending the
format already established in that directory:

```
# X 投稿ドラフト — <YYYY-MM> バッチ

status / 文字数注意 / ハッシュタグ方針

## <ID> ｜ <theme> ｜ <category> / <x_tier>
- 狙い:
- 切り口:
- 基盤 (basis):
- 依存: プレースホルダ
- 事実確認: 要 / 不要 — 対象クレーム
- 主観明示: あり / なし
- 概算: 約NN字
- status:

（本文をコードブロックで）
```

The JSON in `schemas/x_post.schema.json` is the machine-readable form; the
markdown batch file is the human review surface. **They must not diverge** —
the markdown is generated from the JSON, never edited independently.

---

## Report format

Ordered by tier. **Tier 1 first, always** (`kpi.md`).

```
1. Tier 1 — Business outcome
   X-attributed bookings and site sessions vs prior period

2. Tier 2 — Authority and saveability
   bookmark rate, profile click rate, follows, link CTR,
   basis coverage, verification hit rate, cadence adherence
   -> any decline here is flagged P0 regardless of Tier 3

3. Tier 3 — Reach and engagement
   impressions, likes, reposts, replies — diagnostics only,
   framed as explanation for 1 and 2

4. What produced the result
   by category / angle / hook pattern / CTA type

5. Escalations
   reach-vs-basis conflicts, verification backlog, seasonal risk

6. Hypothesis ledger
   what was believed, what the data showed, what was updated
```

The hypothesis ledger is mandatory. It operationalises the `/AGENTS.md` rule
that when evidence conflicts with a hypothesis, the hypothesis is updated.
