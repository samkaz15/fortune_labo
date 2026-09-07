# Content Strategy Agent — Inputs

## From A06 SEO Agent (primary)

| Input | Schema | Required |
| --- | --- | --- |
| SEO Opportunity | [`../seo/schemas/seo_opportunity.schema.json`](../seo/schemas/seo_opportunity.schema.json) | **Yes** |
| SEO requirement set (keyword, intent, SERP gap, structured data, compliance flags) | [`../seo/schemas/content_brief.schema.json`](../seo/schemas/content_brief.schema.json) | Yes for Tier A/B |
| Keyword register entry (tier, booking_potential, moat_fit, cannibalisation) | [`../seo/schemas/keyword_register.schema.json`](../seo/schemas/keyword_register.schema.json) | Yes |
| Visit plan and seasonal publish-by dates | [`../seo/schemas/visit_plan.schema.json`](../seo/schemas/visit_plan.schema.json) | For Tier A |

**A07 does not accept a bare keyword.** An opportunity with
`moat_alignment: conflicting` is never accepted — it belongs to A01 Strategy
Agent, and accepting it would launder an escalation into a brief.

## From the human practitioner (irreplaceable)

| Input | Why it cannot come from anywhere else |
| --- | --- |
| Visit notes, photographs, observed conditions | The moat itself; gates every Tier A brief |
| Divinatory basis for a judgment | Only the practitioner holds the method |
| **Real client questions, in their own words** | Highest-value persona and angle source in the system |
| Monthly capacity (visits, writing, review) | Bounds the editorial calendar |
| Photo permission status per shrine | Legal gate |

## From A03 Customer/Persona Agent

Personas, jobs-to-be-done, journey stages. Used to populate `target_persona` and
`reader_state` when direct client language is unavailable.

## From A02 Research Agent

Audience research, competitor content inventory, shrine event calendars,
regulatory changes affecting permissible claims.

## From A18 Analytics Agent

Per-URL performance for rewrite triage: sessions, engagement, scroll depth,
CTA click-through, booking attribution, publish/update dates.

## From A01 Strategy Agent

Current business priority, capacity constraints, approved and rejected
directions, service/pricing changes that alter which CTA is appropriate.

## From the repository

| Source | Use |
| --- | --- |
| `content/briefs/` | Existing briefs — duplicate detection |
| `content/drafts/` | In-flight work — capacity accounting |
| Published URL inventory | Rewrite vs build-new triage |

## Availability by phase

| Phase | Available | A07 operates on |
| --- | --- | --- |
| **1 — Now** | SEO opportunities, human input, manual SERP observation, published URL list | Full triage, briefs, editorial calendar. **Not blocked.** |
| **2** | GSC + GA4 read | Evidence-based rewrite triage |
| **3** | Booking attribution | Priority ordering by realised revenue, not proxy |

Until Phase 3, every priority ordering A07 emits must be labelled
**proxy-based**, matching A06's disclosure requirement
(`../seo/integrations.md` §Google Analytics 4).
