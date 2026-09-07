# Prompt — Repurpose Plan

## Task
Produce the rollout plan for one piece across its viable channels.

## Step 1 — Resolve every channel

Every one of the nine channels ends in exactly one state: an adapted Channel
Content artifact, or a recorded `skip` with a reason and a revisit condition.

**No channel is silently omitted.** A silent omission is indistinguishable from
an oversight and will be re-argued every time someone reviews the plan.

Skip reasons: `no_cleared_visual` · `no_video_footage` ·
`insufficient_substance` · `no_genuine_question` · `compliance_risk` ·
`audience_mismatch` · `strategy_declined` · `capacity`.

## Step 2 — Sequence

Default order (`../responsibilities.md` §K):

```
Day 0   article publishes
Day 0   X          quotable observation + link
Day 1   Instagram  carousel
Day 2   Threads    the open question
Day 3   Facebook   contextual post
Day 4   note       depth piece
Day 5   Ameba      narrative retelling
Day 7   LINE       only with a dated, concrete reason
Week 2  TikTok / YouTube once footage is edited
```

Override for: seasonal deadlines (which always win), footage availability, and
practitioner availability for talking-head video.

Each entry carries a rationale. "It's next in the list" is not a rationale.

## Step 3 — Sanity-check the volume

```
if channels_adapted >= 7:
    re-examine. Nine posts from one article is a warning sign.
    Which of these are actually strong?
```

## Step 4 — Approval framing

The plan is a **proposal**. Mark clearly:

- Each post requires individual human approval
- Approving the plan approves nothing
- Proposed times are proposals; a human schedules and posts
- LINE requires A30 review before it reaches the human

## Step 5 — Feedback to A07

Where a brief's `sns_repurpose` decision proved unworkable, record it so future
briefs stop commissioning adaptations the material cannot support.

## Output
`schemas/repurpose_plan.schema.json`.
