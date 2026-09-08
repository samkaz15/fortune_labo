# Prompt — Fact-Check Handoff

## Task
Emit an `x_fact_check_request` for every post carrying a claim that is not
already verified.

**You never verify your own history claims** (`rules.md` §3.6). You classify
them, name where they could be checked, and hand them over. Self-certification
is not permitted.

## What counts as a factual claim

More than it looks like:

| Claim | Type |
| --- | --- |
| 「重陽の節句は五節句のひとつです」 | `cultural` |
| 「旧暦9月9日は新暦では10月頃にあたります」 | `calendrical` |
| 「寒川神社は○○の神を祀っています」 | `shrine_origin` |
| 「1200年の歴史があります」 | `numeric` — **an unsourced number is a fabricated fact** |
| 「菊酒を飲む習慣がありました」 | `food_tradition` |
| 「昔の日本人は朝に○○していました」 | `historical` + **over-generalisation risk** |
| 「○○という言葉は△△に由来します」 | `attribution` |

Statements about the practitioner's own view are not factual claims — they are
`practitioner_view`, and they need marking, not verification.

## Criticality — set this carefully

| Value | Meaning | If refuted |
| --- | --- | --- |
| `load_bearing` | The post exists because of this claim | **Drop the post.** Do not edit around it |
| `supporting` | Strengthens the post but is not its reason | Remove the sentence |
| `incidental` | Colour | Remove or hedge |

Most Category A posts have exactly one `load_bearing` claim. Name it correctly —
this field decides what happens when verification comes back bad.

## Source candidates

Name where the claim could actually be checked, ranked:

| Type | Examples |
| --- | --- |
| `shrine_official` | The shrine's own 由緒 page or printed 由緒書 |
| `government_or_municipal` | 自治体史, 市町村の文化財説明 |
| `academic` | 学術論文, 大学紀要 |
| `reference_work` | 国史大辞典, 年中行事辞典 |
| `museum_or_archive` | 国立国会図書館デジタルコレクション, 博物館資料 |

「ウェブ検索で複数のサイトが同じことを書いている」 is not a source. Aggregated
content copies itself, and this is exactly how an invented 由緒 propagates.

## Over-generalisation

Flag `overgeneralisation_risk: true` wherever the claim risks
「昔の日本人は全員○○していた」. This is a **factual error, not a style issue**
(`rules.md` §3.3). Ask the checker which class, region, or era the practice
actually belonged to.

## Proposed hedge

For each claim, write how it would read if verification comes back inconclusive:
「〜と言われています」「〜という説があります」「諸説あります」.

If no acceptable hedge exists — if hedging would gut the post — say so. That
tells the checker the post's survival depends on this claim.

## Urgency

| Value | Use |
| --- | --- |
| `standard` | Normal batch flow |
| `seasonal_deadline` | Hard date. Set `needed_by`. Fact-check turnaround is the long pole for 節句 and 二十四節気 posts |
| `correction` | **A published post is suspected wrong. P0** — escalate to a human immediately and prepare a correction draft (`rules.md` §6) |

## On resolution

| Verdict | Action |
| --- | --- |
| `verified` | Proceed. Record `verified_source` on the post |
| `verified_with_hedge` | Apply the hedge, set `hedge_applied: true` |
| `unverifiable` | Hedge, or remove the claim. Never assert it |
| `refuted` + `load_bearing` | **Drop the post.** Also check whether the same claim appears in other drafts |

A refuted claim that already shipped is a `correction` — same day, human,
deletion and a correction post.

## Output
`schemas/x_fact_check_request.schema.json`, one per post.
Set `fact_check_required: true` and `status: fact_check_pending` on the post.
