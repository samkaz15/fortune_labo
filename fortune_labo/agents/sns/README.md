# A10 — SNS Content Agent

Adapts fortune_labo's core content to each social platform.

This directory holds the **parent scope only**. Actual work is done by
channel sub-agents, because the channels differ enough that a single shared
specification would be too vague to constrain anything.

## Sub-agents

サブエージェントには2種類あります。**チャネル別**（1つのプラットフォーム向け）
と、**フォーマット別**（複数チャネルにまたがる1つの表現形式）です。

### チャネル別

| ID | Channel | Directory | Status |
| --- | --- | --- | --- |
| **A10-X** | X (旧Twitter) | [`x/`](./x/) | **implemented** |
| A10-IG | Instagram | `instagram/` | not implemented |
| A10-TH | Threads | `threads/` | not implemented |
| A10-AB | Ameba ブログ | `ameba/` | not implemented |
| A10-FB | Facebook | `facebook/` | not implemented |

### フォーマット別

| ID | Format | Directory | Status |
| --- | --- | --- | --- |
| **A10-SC** | 動画台本（TikTok / Reels / Shorts / YouTube） | [`script/`](./script/) | **implemented** |

TikTok に単独のチャネルサブエージェントを置いていないのは意図的です。
動画は同じ素材が複数の尺・複数のプラットフォームへ展開されるため、
チャネルごとに同じ仕様を持つより、**1つの台本エージェントが各尺へ
展開する**ほうが整合します。TikTok 固有の作法は
[`script/formats.md`](./script/formats.md) の章別作法にあります。

Until a channel sub-agent exists, drafts for that channel are produced ad hoc
and live in [`../../content/sns/`](../../content/sns/) under the constraints
listed in that directory's README.

## What A10 owns

- Channel-specific adaptation of approved themes
- Channel-native writing (structure, length, hooks, CTA)
- Channel posting cadence and batch composition
- Channel-level performance interpretation, handed to Analytics Agent

## What A10 does not own

| Not owned | Owner |
| --- | --- |
| Which themes are worth publishing at all | A07 Content Strategy Agent |
| Search demand, keyword tiers, seasonal calendar | A06 SEO Agent |
| Long-form articles and LP copy | A08 Content Production Agent |
| Channel-level acquisition strategy and budget | A09 SNS Strategy Agent |
| Fact verification | A28 QA / A29 Fact-Check Agent |
| Publishing | Human approval, then a human or an authorised integration |

## Boundary with A09 SNS Strategy Agent

A09 decides **which channels to invest in and why**.
A10 decides **what to say on a channel that A09 has already chosen**.

If a sub-agent finds that a channel is structurally wrong for this business,
that is an escalation to A09 — not a decision A10 may make.

## Rules inherited by every sub-agent

Every A10 sub-agent inherits, without exception:

1. `/AGENTS.md` — no autonomous publishing, no invented business facts
2. `agents/seo/positioning.md` — the moat definition and the one-line test
3. `agents/seo/rules.md` §2 (first-hand), §3 (subjectivity), §4 (compliance)

A sub-agent may add stricter channel rules. It may never relax an inherited one.
