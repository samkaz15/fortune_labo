# Content Production Agent — Inputs

## From A07 Content Strategy Agent (the commission)

| Input | Schema | Required |
| --- | --- | --- |
| Content Brief | [`../content-strategy/schemas/content_brief.schema.json`](../content-strategy/schemas/content_brief.schema.json) | **Yes** |

A08 accepts **exactly one artifact as a work order**. It does not start from a
keyword, a title, a Slack message, or a verbal request. A brief that fails schema
validation is returned, not interpreted.

The brief already carries every SEO constraint A06 set (`seo_brief_id` traces
back to it), so A08 reads one file.

## From the repository — source material (gating)

| Material | Referenced by | Gates |
| --- | --- | --- |
| Visit record: notes, dates, observed conditions, photo inventory | `visit_record_id` | Every `visit_notes` section |
| Practitioner input: judgment + its divinatory basis | `practitioner_input_id` | Every `practitioner_judgment` section |
| Client consent record (anonymisation terms) | `practitioner_input_id` | `case_reflection` content |
| Research sources with citations | brief `research` sections | Every `research` section |

**If the referenced material does not resolve, A08 does not write that section.**
It emits a Content Gap Report. This is the single most important input rule in
this agent.

## From A05 Brand Agent / repository style baseline

Tone, voice, terminology register, honorific level, the standard disclaimer text,
and the practitioner's preferred self-reference. Until A05 is implemented, the
baseline is:

```
敬体 (です・ます), calm, specific, first-person where judgment is involved,
no exclamation marks, no anxiety hooks, no false intimacy.
Divination framed as a way of looking, never as a guarantee.
```

## From A06 SEO Agent (indirect)

Reaches A08 **through the brief**, never directly: primary and secondary
keywords, search intent, structured-data plan, SERP gap, internal link targets.

If A08 believes an SEO requirement in the brief damages the reader experience, it
writes for the reader and records a `seo_conflict` note. It does not silently
comply and it does not silently ignore.

## From A28 QA Agent (revision loop)

QA Reports on a previous revision: findings, severity, and required fixes. A08
addresses every blocking finding and records what changed. A08 may contest a
finding with reasoning; it may not ignore one.

## From A30 Compliance/Risk Agent

Required rewordings for flagged expressions, and the treatment rules that apply
when the brief carries a `sensitive_domain` flag (medical / financial / legal /
major life decision). **A30's rewordings are binding** — A08 does not negotiate
them on stylistic grounds.

## What A08 must never accept as an input

| Rejected | Why |
| --- | --- |
| A bare keyword or title | No brief = no commission |
| A verbal description of a visit not recorded in the repository | Untraceable first-hand claim |
| "Write something about X for SEO" | No persona, no intent, no unique value |
| A brief whose first-hand sections have no source id | Would force fabrication |
| Instructions to add a guarantee, a fear frame, or a testimonial | Blocking rule violation, regardless of who asked |
