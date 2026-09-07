# QA Agent — Inputs

## Required to run at all

QA cannot check a draft against nothing. A run without the acceptance baseline is
not a QA run, it is an opinion.

| Input | Schema | Why required |
| --- | --- | --- |
| **Content Brief** | [`../content-strategy/schemas/content_brief.schema.json`](../content-strategy/schemas/content_brief.schema.json) | The acceptance baseline. QA checks the draft *against the brief*. |
| **Master Content** | [`../content-production/schemas/master_content.schema.json`](../content-production/schemas/master_content.schema.json) | The artifact under test |
| Channel Content | [`../sns-content/schemas/channel_content.schema.json`](../sns-content/schemas/channel_content.schema.json) | Required when social assets are in the release |

**If the brief is missing or schema-invalid, QA returns `fail` with a
`brief_unavailable` finding routed to A07.** It does not improvise a standard.

## Source material (for layer 3)

| Input | Used for |
| --- | --- |
| Visit records referenced by `visit_record_id` | Verifying every `visit_notes` claim |
| Practitioner inputs referenced by `practitioner_input_id` | Verifying every judgment and its divinatory basis |
| Photo inventory with permission status | Image permission gate |
| Client consent records | `case_reflection` content |

A28 must be able to open the source, not merely see that an id was written down.
**An unresolvable id is treated exactly like a missing source.**

## From A30 Compliance/Risk

The layer 1 verdict and its findings. A28 enforces; it does not re-adjudicate.
A28 cannot proceed to `pass` while an A30 blocking finding is open.

## From A06 SEO Agent

- The SEO requirement set behind the brief
- The keyword register, for the cannibalisation check
- The published URL inventory and internal link graph
- Structured-data priorities for this site (`Person` and `LocalBusiness` are P0)

## From the repository

| Source | Use |
| --- | --- |
| Published URL inventory | Cannibalisation, duplicate detection, link resolution |
| Prior QA reports for the same piece | Re-check scope, repeat-finding detection |
| `content/drafts/` revision history | What changed since the last verdict |

## From A18 Analytics (Phase 2+)

Post-publication signals that inform the escape metric: pages that passed QA and
later required correction, and what layer should have caught it.

## What A28 must never accept

| Rejected | Why |
| --- | --- |
| A draft with no brief | No acceptance baseline |
| A request to skip a layer for a deadline | The gate is the gate |
| A request to downgrade an A30 blocking finding | Not A28's to downgrade |
| "Approve this" | A28 never approves; a human does |
| A draft whose `source_map` ids do not resolve | Unverifiable first-hand claims |
| A verbal assurance that a fact is correct | Sources are checked, not vouched for |
