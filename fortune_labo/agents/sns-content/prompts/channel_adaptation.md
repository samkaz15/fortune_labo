# Prompt — Channel Adaptation

## Task
Convert one Master Content into Channel Content for the channels A07 marked
`strong` or `possible`.

## Step 1 — Viability, per channel

| Channel | Hard requirement | Missing → |
| --- | --- | --- |
| Instagram | Cleared photography or a designed visual concept | `skip` |
| TikTok | Visual sequence + a hook that lands in 2 seconds | `skip` |
| X | A point standing alone in ~140 Japanese chars | `skip` |
| YouTube | Substance for 5+ minutes without padding | `skip` |
| Threads | A genuine question worth answering | `skip` |
| Facebook | Context worth 200–400 chars | `skip` |
| LINE | A dated, concrete reason for an existing follower to care now | `skip` |
| Ameba | A narrative arc | `skip` |
| note | Depth beyond what the article already says | `skip` |

Downgrade freely. Never upgrade an A07 `skip`.

## Step 2 — Extract the transferable substance

In priority order: `sns_source_blocks` → `featured_snippet_block` → `faq` →
`visit_notes` sections → `practitioner_judgment` sections.

**Never centre a post on an `ai_structurable` section.**

## Step 3 — Adapt natively

Apply the per-channel spec in `../responsibilities.md` §B–§J. The test for each
draft:

> If someone read only this post and never the article, would they have received
> something whole?

Excerpts fail. Teasers that withhold the answer fail and annoy the reader.

## Step 4 — Direction, not creation

- **Visual direction:** reference cleared photo inventory **by id**. Say what each
  slide/frame shows and why. Never describe an image to be generated.
- **Video direction:** shot list per beat, from real visit footage. On-screen text
  per beat. Timecodes.

## Step 5 — Traceability

Every first-hand claim in the post gets a `firsthand_claims[]` entry with its
`source_reference` from the Master Content `source_map`. A social post is a
publication.

## Step 6 — Compliance sweep

Run `compliance_sweep.md` over **every element**: hook, body, CTA, each hashtag,
each on-screen frame, each carousel slide, the thumbnail concept, the video
title. Not just the caption.

## Step 7 — Budgets

Check `character_count` against `character_limit` and duration against the format
budget. Over budget is a format failure, not a rounding issue — and shortening
must never come out of the qualification on a claim.

## Step 8 — Sequence

Propose a rollout order with rationale (`../responsibilities.md` §K). Seasonal
deadlines override the default order. This is a proposal; a human schedules.

## Output
One `schemas/channel_content.schema.json` per adapted channel, plus one
`schemas/repurpose_plan.schema.json` recording the sequence and every skip with
its reason.
