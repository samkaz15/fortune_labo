# A10 — SNS Content Agent

Re-cuts one Master Content into **channel-native content** for nine destinations.

> **Read [`agents/seo/positioning.md`](../seo/positioning.md) first.** The moat
> rules apply on social exactly as they apply on the site — arguably harder,
> because social is where commodity fortune-telling content is cheapest to make
> and hardest to distinguish from.

## What this agent is

**Channel editor.** It does not copy-paste. It asks, per channel, *"what is this
piece, expressed as something that belongs here?"* — and is allowed to answer
"nothing".

```
   A08 Content Production ── master_content.json (+ sns_source_blocks)
   A07 Content Strategy   ── sns_repurpose[] (channel, viability, angle, objective)
            │
            ▼
   ┌──────────────────────┐
   │ A10 SNS CONTENT      │
   └──────────┬───────────┘
              │  channel_content.json (CC-xxxx) — one per channel
              ▼
      A28 QA ◄── A30 Compliance/Risk
              ▼
       HUMAN APPROVAL          ← mandatory. A10 never posts.
              ▼
   Instagram · TikTok · X · YouTube · Threads
   Facebook · LINE · Ameba · note
              ▼
       A18 Analytics ──► A06 / A09
```

## Channels in scope

| Channel | What it is here for |
| --- | --- |
| **Instagram** | Visual, saveable reference. Saves > likes. |
| **TikTok** | Short-video script. Hook in the first 2 seconds or nothing. |
| **X** | Short, quotable, conversational. Reach and replies. |
| **YouTube** | Long-form video concept and script. Depth and trust. |
| **Threads** | Conversational prompt. A question, not a broadcast. |
| **Facebook** | Community post. Longer, warmer, context-first. |
| **LINE** | Existing audience. Retention and return visits. |
| **Ameba** | Blog post in Ameba's own register. Discovery inside the platform. |
| **note** | Deep-dive essay. The thinking behind the piece. |

**Out of scope:** Pinterest and email newsletter.

## The rule that defines this agent

**Never post the article to social.** A link plus the first paragraph is not a
social post; it is a failure to do this job. Each channel gets content built for
how people actually read on that channel, or it gets `skip`.

**`skip` is a correct answer.** A shrine report with no cleared photography is
not an Instagram post. A judgment that needs 400 words of context is not an X
post. A10 declining a channel is a better outcome than A10 producing something
that will embarrass the practitioner.

## Files

| File | Purpose |
| --- | --- |
| [`mission.md`](./mission.md) | Mission, scope, non-goals |
| [`responsibilities.md`](./responsibilities.md) | Per-channel adaptation specs |
| [`inputs.md`](./inputs.md) | Master content, repurpose decisions, brand voice |
| [`outputs.md`](./outputs.md) | Channel Content, Repurpose Plan |
| [`workflow.md`](./workflow.md) | Adaptation loop, approval, scheduling |
| [`rules.md`](./rules.md) | Compliance on social, platform rules, no-autopost |
| [`kpi.md`](./kpi.md) | Per-channel objectives and the booking-first stack |
| [`prompts/`](./prompts/) | System prompt + per-channel prompts |
| [`schemas/`](./schemas/) | `channel_content`, `repurpose_plan` |

## Compliance on social is stricter, not looser

Short formats compress, and compression is where guarantees appear. `参拝すれば
願いが叶う` fits a hook perfectly and is a blocking violation. Every rule in
[`../seo/rules.md`](../seo/rules.md) §4 applies to every hook, caption, on-screen
text frame, thumbnail, and hashtag.
