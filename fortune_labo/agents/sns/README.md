# A10 — SNS Content Agent

Adapts fortune_labo's core content to each social platform.

This directory holds the **parent scope only**. Actual work is done by
channel sub-agents, because the channels differ enough that a single shared
specification would be too vague to constrain anything.

## Sub-agents

| ID | Channel | Directory | Status |
| --- | --- | --- | --- |
| **A10-X** | X (旧Twitter) | [`x/`](./x/) | **implemented** |
| A10-IG | Instagram | `instagram/` | not implemented |
| A10-TH | Threads | `threads/` | not implemented |
| A10-AB | Ameba ブログ | `ameba/` | not implemented |
| A10-FB | Facebook | `facebook/` | not implemented |
| A10-TT | TikTok | `tiktok/` | not implemented |

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
