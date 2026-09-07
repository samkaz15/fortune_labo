# SNS Content Agent — Workflow

## Position in the pipeline

```
A07 Content Strategy ── sns_repurpose[]  (whether + why)
A08 Content Production ─ master_content.json (+ sns_source_blocks)
            │
            ▼
┌──────────────────────────────────────────────┐
│ A10 SNS CONTENT                              │
│                                              │
│  1 intake        master content + repurpose  │
│  2 viability     per channel: go / skip      │
│  3 extract       the transferable substance  │
│  4 adapt         per channel, natively       │
│  5 direction     visual / video specs        │
│  6 compliance    self-sweep on every asset   │
│  7 sequence      proposed rollout order      │
│  8 handoff       QA → A30 → HUMAN            │
└──────────────────┬───────────────────────────┘
                   │  channel_content.json × N
                   ▼
        A28 QA ◄── A30 Compliance/Risk
                   ▼
            HUMAN APPROVAL   ← per post, not per plan
                   ▼
        Human or Codex posts
                   ▼
            A18 Analytics ──► A06 / A09
```

---

## Step 2 — Viability, honestly

```
for channel in brief.sns_repurpose:
    if channel.viability == "skip":
        record and move on          # A10 may not upgrade A07's skip
    if required_material(channel) is missing:
        downgrade to skip with reason
    if the honest version does not fit the format:
        downgrade to skip with reason
    else:
        adapt
```

Required material: cleared photography (Instagram, Facebook, Ameba), real visit
footage (TikTok, YouTube), a standalone point (X), a genuine question (Threads),
substance beyond the article (note), a dated reason (LINE).

**Downgrading to `skip` is the most common correct decision in this agent.**
Two strong posts beat nine weak ones, and weak posts on a practitioner's account
cost trust that traffic does not buy back.

---

## Step 3 — Extract the substance

Pull from Master Content, in this priority order:

1. `sns_source_blocks` — A08 already marked the strongest material
2. `featured_snippet_block` — usually the best standalone point
3. `faq` — usually the best conversational and carousel material
4. Sections with `source_requirement: visit_notes` — **the moat material**
5. Sections with `source_requirement: practitioner_judgment` — the authority
   material, with markers attached

**Never extract from an `ai_structurable` section as the centrepiece of a post.**
That is the part any competitor could write, so a post built on it builds nothing.

---

## Step 4 — Adapt, do not excerpt

The test for each draft post:

> If someone read only this post and never the article, would they have received
> something whole?

An excerpt fails this test. A teaser that withholds the answer fails it and
annoys the reader. A native post gives something complete, and the article
extends it.

---

## Step 6 — Compliance self-sweep (every asset, not every post)

Run over: hook, body, CTA, every hashtag, every on-screen text frame, every
thumbnail concept, every carousel slide, and the video title.

| Check | Blocking |
| --- | --- |
| Guaranteed outcome in a hook | Yes |
| Fear framing anywhere, including a thumbnail | Yes |
| Unmarked judgment | Yes |
| Medical / financial / legal claim | Yes |
| First-hand claim with no `source_reference` | Yes |
| Efficacy ranking | Yes |
| Disclaimer missing where a judgment appears | Yes |
| Hashtag implying a guarantee (`#願いが叶う`) | Yes |
| Over character limit | Yes (format failure) |

**Compression is where violations appear.** A 15-character on-screen frame has no
room to qualify a claim, and a 2-second hook has none at all. If the honest
version does not fit, the format is wrong — shorten the claim, never the
qualification.

---

## Step 8 — Handoff and approval

```
Channel Content set
      ▼
A28 QA          format, limits, hashtags, tone, source consistency
      ▼
A30 Compliance  every LINE draft, every judgment-bearing post,
                every compressed hook
      ▼
HUMAN APPROVAL  per post — approving a plan is not approving its posts
      ▼
Human or Codex posts
```

**A10 has no publishing path to any platform.** Not to a scheduler, not to a
draft queue that auto-publishes, not to LINE. Where posting is later automated,
Codex builds it and it still requires per-post human approval (`/AGENTS.md`).

---

## Cadence

A10 is **event-driven**: it runs when Master Content reaches `qa_passed`, or when
a QA or A30 finding returns.

| Trigger | Action |
| --- | --- |
| Master Content passes QA | Full adaptation run |
| Visual/video material arrives late | Adapt the channels that were parked on it |
| QA or A30 finding returns | Revise that channel's asset, re-run the sweep |
| A brief's `sns_repurpose` proves unworkable | Feed back to A07 |
| Seasonal deadline approaching | Re-sequence; seasonal timing overrides the default order |

### Monthly review

- Which channels are consistently `skip`? Either the material or the channel
  choice is wrong — raise it with A07 / A01
- Which objectives were met per channel (saves, replies, clicks, bookings)?
- Did any post require a post-publication correction? Root-cause it
- Is any channel drifting toward commodity content because it performs? **P0** —
  performance is not a defence against positioning

---

## Escalation triggers

| Trigger | Route |
| --- | --- |
| Honest version does not fit the format | Record `skip` — do not shorten the qualification |
| Photo permission `pending` | Human — visual channels blocked |
| Instruction to add urgency because engagement is down | **Refuse.** Escalate to A01 |
| A post would need a claim the article does not make | A08 / A07 — the post is ahead of the material |
| Compliance finding on a published post | **Human immediately; request takedown** |
| Channel performing well on off-positioning content | A01 Strategy — moat conflict |
