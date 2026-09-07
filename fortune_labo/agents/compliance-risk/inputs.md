# Compliance/Risk Agent — Inputs

## Mandatory review triggers

These reach A30 **always**, not on request:

| Trigger | Stage |
| --- | --- |
| A07 brief carrying any `sensitive_domain` flag | **Before drafting** |
| Every LINE channel asset, without exception | Before QA passes |
| Any artifact where A28 delegates layer 1 (i.e. every artifact) | QA layer 1 |
| Any content mentioning health, money, law, or a major life decision | Any stage |
| Any `case_reflection` content | Before drafting and before publication |
| Any content about an identifiable individual | Before publication |
| A compliance concern raised by any agent or human | Immediately |
| Compliance risk suspected in **published** content | **Immediately — incident** |

Pre-drafting review exists because a treatment rule issued before A08 writes is
one revision; the same rule issued after is three.

## Artifacts assessed

| Input | Schema |
| --- | --- |
| Content Brief | [`../content-strategy/schemas/content_brief.schema.json`](../content-strategy/schemas/content_brief.schema.json) |
| Master Content | [`../content-production/schemas/master_content.schema.json`](../content-production/schemas/master_content.schema.json) |
| Channel Content | [`../sns-content/schemas/channel_content.schema.json`](../sns-content/schemas/channel_content.schema.json) |
| Published pages and posts | Live inventory, for monitoring sweeps |

### Fields A30 relies on specifically

| Field | Use |
| --- | --- |
| `compliance_requirements.sensitive_domain` | Which treatment rules apply |
| `source_map` + `verbatim_anchor` | Whether a first-hand claim is traceable |
| `attribution_markers` | Whether judgments are marked or asserted |
| `photo_permission_status` | Image rights gate |
| `client_consent_recorded` | Consent gate for `case_reflection` |
| `compliance.replacements_made` (A10) | Whether the social sweep actually ran |
| `cta` + surrounding text | The anxiety-adjacency check |

## Evidence sources

| Source | Use |
| --- | --- |
| Consent records | Verifying, not assuming, consent |
| Photo permission records | Verifying shrine and third-party image rights |
| Licence records | Music, footage, third-party content |
| Visit and practitioner input records | Verifying first-hand traceability |
| The risk register | Prior decisions, accepted risks, open items |
| Prior assessments for the same piece | Repeat findings |

**A30 verifies records; it never accepts an assurance in place of one.** "Consent
was given" is not a consent record, and "the shrine said it was fine" is not a
permission record.

## From A02 Research Agent

Regulatory changes, Consumer Affairs Agency guidance, platform policy changes,
and enforcement actions against comparable businesses. Feeds the quarterly
regulatory watch.

## From A18 Analytics

Signals suggesting reputational or compliance problems in the wild: complaint
volume, LINE block rate, negative sentiment spikes, platform warnings or
takedowns.

A rising LINE block rate is treated as a **compliance signal first** and a
performance signal second.

## What A30 must never accept

| Rejected | Why |
| --- | --- |
| A request to clear content for a deadline | Deadlines do not change the law |
| A request to downgrade a blocking finding | Only a human may *accept* a risk, on the record |
| A verbal assurance of consent, permission, or licence | Records are verified |
| An artifact whose `source_map` ids do not resolve | Untraceable claims are unverifiable |
| A legal interpretation question framed as a routine check | Escalates to a qualified professional |
| "This performs well" as a reason to relax a rule | Performance is not a compliance argument |
