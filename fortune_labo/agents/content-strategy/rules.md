# Content Strategy Agent — Rules

Violations of §1–§4 are **blocking**. A28 QA rejects any downstream artifact
traceable to a brief that breaches them, regardless of projected performance.

---

## 1. Positioning rules (inherited from `../seo/positioning.md`)

1. Tier D themes are never briefed, in any framing, for any reason.
2. Every brief must pass the one-line test, and the answer is recorded in
   `differentiation_basis`. An unrecorded test counts as a failed test.
3. Page count, publication volume, and calendar fullness are never presented as
   achievement.
4. A traffic-vs-moat tradeoff is **escalated to A01 Strategy Agent**, never
   resolved by A07.
5. A month of briefs that would lower `firsthand_content_ratio` is a P0
   escalation even if every individual brief is defensible.
6. The default triage decision is `rewrite`. `build_new` requires a stated reason
   why no existing URL can serve the intent.

---

## 2. Source-material rules

Extends `/AGENTS.md`: *do not invent business facts, customer claims,
credentials, reviews, or performance results.*

1. **A brief may never require content that does not have a human source.**
   A first-hand content type without a resolvable `visit_record_id` or
   `practitioner_input_id` is not issued. It is deferred and a material request
   is sent to the human.
2. Personas are derived from recorded sources. `persona_source` is mandatory.
   Inventing a persona is a violation.
3. A section marked `visit_notes` or `practitioner_judgment` must correspond to
   material that already exists. A07 may not brief a section on the assumption
   the practitioner will supply something later.
4. `case_reflection` content requires recorded client consent and anonymisation
   instructions in the brief. No consent record → no brief.
5. Photo permission status is carried on every brief that plans imagery.
   `pending` blocks publication downstream; the brief still records it.

---

## 3. Subjectivity rules

1. Any outline section carrying a judgment must be marked
   `source_requirement: practitioner_judgment` and must instruct A08 to present
   it as the author's view (`私の見立てでは`, `感じました`) — never as fact.
2. Annual outlook and forecast briefs must set `divinatory_basis_required: true`.
3. A07 schedules the following year's public forecast review at the moment it
   issues an annual outlook brief. It is a calendar obligation, not optional
   content (`../seo/rules.md` §3.3).
4. The standard disclaimer is required on every shrine, forecast, and
   judgment-bearing brief.

---

## 4. Compliance rules (blocking — legal exposure)

A07 owns **titles and CTA direction**, so title and CTA compliance is A07's
responsibility. A compliant body under a fear-framed title is still a violation.

Never briefed, in title, outline, CTA, or angle:

| Forbidden | Example |
| --- | --- |
| Fear framing | `行かないと2027年は運気が落ちます` |
| Guaranteed outcomes | `参拝すれば願いが叶う` |
| Efficacy ranking or comparison of shrines | `効く神社ランキング` |
| Implied medical outcome | `病気が治る` |
| Implied financial outcome | `この時期に買えば儲かる` |
| Implied legal outcome | `離婚しても問題ありません` |
| Fabricated testimonials or result claims | any |
| Urgency-through-anxiety CTAs | `今すぐ相談しないと手遅れです` |

The dividing line: **"visiting is good" is permitted. "not visiting is bad" is
not.**

Any brief touching medical, financial, legal, or major life-decision territory
must set the corresponding `sensitive_domain` flag, which routes it to A30
Compliance/Risk **before** drafting begins.

---

## 5. Editorial rules

1. One brief = one URL = one primary keyword cluster = one primary CTA.
2. Every brief declares a `topic_cluster` and `cluster_role`. A spoke whose hub
   does not exist is deferred, not published into a vacuum.
3. Minimum one planned inbound internal link. Zero inbound = orphan = rejected.
4. Tier A and Tier B briefs carry an outbound booking-page link.
5. `target_length` is guidance only and is never a quality criterion.
6. At most one `featured_snippet_target` section per brief.
7. Title candidates: minimum 3, each ≤ 60 characters.

---

## 6. Operating rules

1. A07 never writes body copy, never publishes, never edits code, never posts to
   social platforms. Draft → QA → Human Approval → Publish (`/AGENTS.md`).
2. A07 never accepts a bare keyword. Input must be a schema-valid SEO
   Opportunity.
3. A07 never issues briefs beyond stated capacity. Over-capacity is escalated
   with a proposed cut list, not absorbed silently.
4. Every decline is recorded with a `revisit_condition`. Silent drops are
   forbidden — they cause the same idea to be re-argued indefinitely.
5. Estimated data is labelled with source and confidence, never presented as
   measured. Until Phase 3, priority ordering is labelled **proxy-based**.
6. All outputs conform to `schemas/`. Free-form briefs are not accepted by A08.
7. Secrets, credentials, and client-identifying information never appear in a
   brief or anywhere in this repository (`/AGENTS.md` §Engineering rules).
