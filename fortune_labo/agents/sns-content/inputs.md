# SNS Content Agent — Inputs

## From A08 Content Production (the source material)

| Input | Schema | Required |
| --- | --- | --- |
| Master Content | [`../content-production/schemas/master_content.schema.json`](../content-production/schemas/master_content.schema.json) | **Yes** |

Used specifically:

| Field | Use |
| --- | --- |
| `sns_source_blocks` | Pre-marked strongest observation, clearest answer, quotable judgment, visual moment |
| `source_map` | The only permitted basis for a first-hand claim in a post |
| `attribution_markers` | Carried into every channel, unchanged |
| `featured_snippet_block` | Often the best X post and TikTok payoff |
| `faq` | Often the best Threads and Instagram carousel material |
| `disclaimer` | Required on channels carrying judgments |

A10 works from `qa_passed` Master Content wherever possible. Adapting a draft
still in revision means re-doing the work when the draft changes.

## From A07 Content Strategy (the commission)

The `sns_repurpose` block of the Content Brief: per channel, `viability`,
`angle`, `objective`, `rationale`.

A10 **may downgrade** a channel to `skip`. A10 **may not upgrade** a channel A07
marked `skip` — that is a strategy decision A07 already made.

## From the human practitioner

| Input | Gates |
| --- | --- |
| Cleared photographs (with permission status) | Instagram, Facebook, Ameba |
| Video footage from actual visits | TikTok, YouTube |
| Voice/appearance availability for talking-head video | YouTube |
| Approval of every post before it goes live | **Everything** |

**No cleared visual material → no visual channel.** A10 never requests or implies
AI-generated imagery of a real shrine. A generated image of a real place
presented as a visit is a fabrication with the same weight as an invented
paragraph.

## From A05 Brand Agent / repository baseline

Voice, register per channel, terminology, the standard disclaimer, and the
practitioner's self-reference. Until A05 exists, the baseline in
`../content-production/inputs.md` applies, adjusted per channel for register only
— never for the compliance posture.

## From A09 SNS Strategy Agent (when implemented)

Channel priority, audience definitions, cadence, campaign context, and the
posting calendar. Until A09 exists, A10 uses the defaults in
`responsibilities.md` §K and flags strategy-level questions to A01.

## From A18 Analytics

Per-channel performance: reach, saves, engagement, profile visits, link clicks,
follower growth, and (Phase 3) booking attribution by channel. Used to tune
format and hook choices, never to justify a compliance shortcut.

## From A30 Compliance/Risk

Binding rewordings, and the standing rule that **every LINE draft is reviewed**
regardless of content.

## What A10 must never accept

| Rejected | Why |
| --- | --- |
| A URL and "make posts for this" | No brief, no source map, no traceability |
| A request to post the article body to a channel | That is not adaptation |
| A request to generate imagery of a real shrine | Fabricated first-hand material |
| A trending format with no connection to the practice | Off-positioning |
| A request to post directly | A10 has no publishing path |
| An instruction to add urgency because engagement is down | Blocking violation |
