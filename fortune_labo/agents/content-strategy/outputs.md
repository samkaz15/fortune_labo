# Content Strategy Agent — Outputs

Every output conforms to a schema in `schemas/`. Free-form briefs are not
accepted by A08.

## Artifact catalogue

| Artifact | Schema | Consumer | Stored at |
| --- | --- | --- | --- |
| **Content Brief** | `content_brief.schema.json` | A08 Content Production | `content/briefs/CB-xxxx.json` |
| Editorial Calendar | `editorial_calendar.schema.json` | A01 Strategy, human | `content/calendar/` |
| Decline Record | `decline_record.schema.json` | A01 Strategy, A06 SEO | `content/declines/` |

---

## Content Brief — the unit of editorial commitment

`CB-xxxx`. One brief = one URL = one primary keyword cluster = one primary CTA.

Field groups:

```
identity        id, seo_opportunity_id, seo_brief_id, created_at, status
decision        decision (build_new|rewrite|consolidate|refresh_only),
                existing_url, rewrite_reason, consolidation_targets
demand          primary_keyword, secondary_keywords, search_intent, tier
audience        target_persona, reader_state, persona_source
purpose         content_goal, content_intent, reader_value
form            content_type, title_candidates, outline, target_length
moat            unique_value, differentiation_basis, source_requirements,
                visit_record_id, practitioner_input_id
distribution    internal_links, cluster_role, topic_cluster, related_content,
                cta, sns_repurpose
governance      compliance_requirements, priority, publish_by, status
```

**Structural guarantees enforced by the schema:**

| Guarantee | Mechanism |
| --- | --- |
| First-hand content cannot be AI-originated | `content_type` in the first-hand set ⇒ `visit_record_id` or `practitioner_input_id` required |
| No orphan pages | `internal_links.inbound_from` `minItems: 1` |
| Booking path always exists | Tier A/B ⇒ booking link required in `outbound_to` |
| No unowned rewrite | `decision: rewrite` ⇒ `existing_url` + `rewrite_reason` required |
| Compliance is not optional | `compliance_requirements` required; enum mirrors `../seo/rules.md` §4 |
| Annual outlooks state their basis | `content_type: annual_outlook` ⇒ `divinatory_basis_required: true` |

### Relationship to `../seo/schemas/content_brief.schema.json`

Two files share a name. They are different layers and both remain valid:

| | A06 `content_brief` | A07 `content_brief` |
| --- | --- | --- |
| Author | SEO Agent | Content Strategy Agent |
| Question answered | "What must be true for this page to rank and stay compliant?" | "What are we actually publishing, for whom, and why us?" |
| Consumer | A07 | A08 |
| Contains | keyword, intent, SERP gap, structured data, SEO constraints | persona, angle, unique value, outline, CTA, distribution, priority |

A07's brief references the A06 brief by `seo_brief_id` and **re-carries every
constraint A06 set**. A08 therefore only needs to read one file.
See [`../../../docs/agents/CONTENT-PIPELINE.md`](../../../docs/agents/CONTENT-PIPELINE.md).

---

## Decline Record

Declining is a first-class output. Every declined opportunity is recorded so it
is not rediscovered and re-argued next quarter.

```
id, seo_opportunity_id, keyword, decline_reason, evidence, decided_at,
revisit_condition, revisit_after
```

`decline_reason` enum: `fails_one_line_test` · `not_winnable` ·
`off_positioning` · `over_capacity` · `no_source_material` ·
`cluster_not_ready` · `duplicate_of_existing` · `compliance_risk`.

`revisit_condition` is mandatory — a decline is a judgment under current
conditions, not a permanent verdict.

---

## Editorial Calendar

Rolling 90-day view. Ordered by `publish_by`, working backward from A06's
seasonal windows (`../seo/workflow.md` §Seasonal backward planning).

Per slot: brief id, content type, owner, source-material status, publish-by,
QA window, approval window, capacity cost.

**The calendar must never show committed capacity above the practitioner's
stated monthly capacity.** If it does, A07 has failed its own planning rule and
must escalate rather than publish the calendar.

---

## Handoff contracts

**→ A08 Content Production**
Sends: one Content Brief, complete. Never a partial brief, never a bare outline.
For first-hand types, `visit_record_id` / `practitioner_input_id` must resolve to
material already in the repository.
Receives back: `master_content.json`, plus flagged gaps where the brief was
unachievable.

**→ A10 SNS Content**
Sends: the `sns_repurpose` block (channel, viability, angle, objective). A10 also
reads the master content from A08. A07 never writes channel copy.

**→ A28 QA**
Sends: the brief as the acceptance baseline. QA checks the draft *against the
brief*, so an ambiguous brief produces an unusable QA result.

**→ A30 Compliance/Risk**
Sends: `compliance_requirements` and the declared claim types, so risk assessment
starts at brief stage rather than after a draft exists.

**→ A01 Strategy Agent**
Sends: decline records, capacity escalations, cluster gaps, seasonal risk.
Receives back: approved / rejected / deferred with rationale.

**→ Codex**
Sends: nothing directly. Consolidation and redirect work is routed through A06
as a `technical_issue`, keeping one owner for the URL graph.
