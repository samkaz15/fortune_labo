# SNS Content Agent — Outputs

## Artifact catalogue

| Artifact | Schema | Consumer | Stored at |
| --- | --- | --- | --- |
| **Channel Content** | `channel_content.schema.json` | A28, A30, human, Codex | `content/sns/CC-xxxx.json` |
| Repurpose Plan | `repurpose_plan.schema.json` | Human, A09, A01 | `content/sns/plans/` |

---

## Channel Content — one artifact per channel

`CC-xxxx`. One Master Content typically produces 2–5 Channel Content artifacts,
not nine. Nine is a warning sign, not a target.

```
identity     id, master_content_id, brief_id, channel, revision, status
targeting    target_persona, objective, format
content      hook, body, cta, hashtags[]
direction    visual_direction, video_direction
budget       character_limit, character_count, duration_seconds
traceability source_references[], attribution_markers[], firsthand_claims[]
governance   compliance{}, requires_compliance_review, approval
scheduling   proposed_post_at, sequence_position
```

### Every channel carries the same required core

`hook` · `body` · `cta` · `hashtags` · `target_persona` · `objective` ·
`character_limit` · `compliance`

Per-channel specifics attach as `visual_direction` (Instagram, Facebook, Ameba)
or `video_direction` (TikTok, YouTube), so a single schema covers nine channels
without nine variants drifting apart.

### Traceability carries over from A08

`firsthand_claims[]` lists every first-hand statement in the post with the
`source_reference` it came from. **A social post is a publication.** The claim
that a shrine looked a certain way in December carries the same evidentiary
weight in a 15-character on-screen text frame as in the article, and gets the
same audit trail.

### `skip` is an output, not an absence

A skipped channel is recorded in the Repurpose Plan with its reason. It is not
silently omitted, because a silent omission is indistinguishable from a mistake
and will be re-litigated every time someone reviews the plan.

---

## Repurpose Plan

The per-piece rollout view.

```
id, master_content_id, channels[], sequence[], skipped[], generated_at

channels[]   channel, channel_content_id, objective, proposed_post_at
skipped[]    channel, reason, revisit_condition
sequence[]   ordered post plan with rationale
```

`reason` enum: `no_cleared_visual` · `no_video_footage` ·
`insufficient_substance` · `no_genuine_question` · `compliance_risk` ·
`audience_mismatch` · `strategy_declined` · `capacity`.

---

## Handoff contracts

**→ A28 QA**
Sends: all Channel Content for a piece, plus the Master Content and the brief.
QA checks channel formats, character limits, hashtags, CTA, brand tone, and
consistency with the source article.

**→ A30 Compliance/Risk**
Sends: every Channel Content whose `requires_compliance_review` is true —
**always true for LINE**, and true for any post carrying a judgment, a
sensitive-domain topic, or a compressed hook.

**→ Human approval**
Sends: the approved-pending post set with the Repurpose Plan. **A human approves
every post individually.** Approving a plan is not approving its posts.

**→ Codex**
Sends: nothing directly. Where posting is later automated, Codex builds the
integration, and it must still require an explicit per-post human approval
(`/AGENTS.md`). There is no design in which A10 posts autonomously.

**→ A18 Analytics**
Sends: post ids and channel objectives so performance can be attributed back to
the source piece and the objective it was written for.

**→ A07 Content Strategy**
Sends: feedback where a brief's `sns_repurpose` decision proved unworkable, so
future briefs stop commissioning adaptations the material cannot support.

---

## What A10 never outputs

- A post published to any platform
- A scheduled post
- A direct message to any customer
- Copy for a channel A07 marked `skip`
- Imagery generated to depict a real shrine
- A post whose first-hand claim has no `source_reference`
