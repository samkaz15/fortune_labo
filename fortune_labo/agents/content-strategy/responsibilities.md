# Content Strategy Agent — Responsibilities

## A. Triage — build, rewrite, consolidate, or decline

**This runs before anything else.** Every inbound SEO Opportunity is resolved to
exactly one decision:

| Decision | When | Downstream |
| --- | --- | --- |
| `build_new` | No existing URL serves this intent, and the gap is real | Brief → A08 |
| `rewrite` | An existing URL targets this intent but underperforms or is stale | Brief → A08 with `existing_url` + `rewrite_reason` |
| `consolidate` | Two or more URLs compete for one intent | Brief → A08 + redirect instruction → Codex |
| `refresh_only` | Facts/dates stale, structure sound | Lightweight brief → A08 |
| `decline` | Fails the one-line test, not winnable, off-positioning, or over capacity | Decline Record → A01 |

**Default bias is `rewrite`.** A new URL is only justified when no existing page
can be made to serve the intent. Page-count growth is not progress
(`../seo/kpi.md` §Forbidden framings).

Rewrite triggers, in order of strength:

1. Position 5–20 on a Tier A/B keyword with impressions but weak CTR
2. Published > 12 months ago and factually time-bound (dates, festivals, prices)
3. Search intent has shifted since publication (SERP composition changed)
4. Cannibalising another URL
5. Missing the mandatory booking-page link or disclaimer

---

## B. Content theme and cluster

A theme is not a keyword. It is **a reader problem the practice is qualified to
resolve.**

Each brief declares its `topic_cluster` and its role inside it:

```
Practitioner profile (authority hub)
  ├── Annual outlook               flagship
  ├── Shrine cluster hub           hub
  │     └── individual shrine pages   spoke (Tier A)
  ├── Method explainers            supporting (Tier C)
  └── Booking / service page       conversion
```

A spoke with no live hub is deferred until the hub exists. Orphan spokes are the
most common way an editorial calendar produces pages nobody reads.

---

## C. Target persona and reader state

Two fields, and they are different:

- **`target_persona`** — who this person is (situation, stage of life, prior
  exposure to fortune-telling, relationship to the practice)
- **`reader_state`** — what is true *at the moment they type the query*: what
  they already know, what they are anxious about, what they will do next

Persona sources, in priority order:

1. **Real client questions supplied by the practitioner** — the literal language
   of people who already paid. Outranks every other source.
2. A03 Customer/Persona Agent output
3. A02 Research Agent audience research
4. SERP "People also ask" and related searches

Inventing a persona from nothing is a rule violation (`rules.md` §2).

---

## D. Search intent → content intent

SEO Agent supplies `search_intent` (informational / navigational / commercial /
transactional / local). A07 must translate it into **content intent** — what the
page is trying to *do to the reader*:

| Content intent | The page succeeds when the reader… |
| --- | --- |
| `answer` | leaves with the specific question resolved |
| `orient` | understands a landscape they were confused by |
| `decide` | can choose between options they were stuck between |
| `trust` | believes this named practitioner is competent and safe to contact |
| `act` | takes the CTA (booking, LINE registration) |
| `record` | receives a first-hand account only this practice can give |

Mismatch between search intent and content intent is the single most common
cause of "ranks well, converts nothing" (`../seo/kpi.md` §Diagnostic matrix).
A07 states both, so QA can check the pair.

---

## E. Article type

Constrained to the same enum A06 uses, so the two agents cannot drift:

`shrine_visit_report` · `annual_outlook` · `forecast_review` ·
`method_explainer` · `situation_guide` · `practitioner_profile` ·
`service_page` · `hub_page` · `faq_page` · `case_reflection`

`shrine_visit_report`, `annual_outlook`, `forecast_review` and
`case_reflection` are **first-hand paths** and require a `visit_record_id` or a
`practitioner_input_id`. No human input record → no brief (`rules.md` §2).

---

## F. Content angle and unique value

`unique_value` must survive the one-line test (`../seo/positioning.md` §9):

> Could a competitor with no shrine visits and an AI subscription produce this
> same page tomorrow?

If yes, the brief is not issued. Acceptable bases for unique value:

- A first-hand visit (date, season, weather, what was actually observed)
- The practitioner's stated judgment **with its divinatory basis**
- A synthesis of real client questions no public source has assembled
- A local/practical detail obtainable only by being there

Not acceptable: "more comprehensive", "better structured", "more up to date"
alone. Those are table stakes, not a moat.

---

## G. Title and outline

**Title candidates:** 3 minimum, each ≤ 60 characters, each carrying the primary
keyword naturally. All candidates are subject to the compliance rules in
`../seo/rules.md` §4 — a fear-framed title invalidates the whole brief even if
the body is clean.

**Outline:** H2/H3 with, for each section:

- `heading_level`, `heading`
- `purpose` — what the reader gains here
- `source_requirement` — `visit_notes` / `practitioner_judgment` / `research` /
  `ai_structurable` (same enum as A06, deliberately)
- `target_question` — the reader question this section answers
- `featured_snippet_target` — boolean; at most one section per brief

If more than half the outline is `ai_structurable`, the page probably fails the
one-line test. Reconsider before issuing.

---

## H. CTA design

Exactly one **primary** CTA per page. Secondary CTAs are permitted but must not
compete visually or semantically.

| Reader state | Appropriate primary CTA |
| --- | --- |
| First contact, high anxiety | `list_signup` (LINE) — booking is too big an ask |
| Researching, comparing | `related_content` into the trust cluster |
| Situation-specific, ready | `booking` |
| Already a client | `booking` (repeat) |

CTA copy direction must not use urgency-through-fear. "Visiting is good" is
permitted; "not acting is bad" is not (`../seo/rules.md` §4).

Every Tier A and Tier B page carries an outbound link to the booking page
regardless of its primary CTA.

---

## I. Internal link strategy

A07 decides the **editorial** link intent; Codex implements; A06 owns the global
graph. Per brief:

- `inbound_from` — which existing pages should link *to* this page, with anchor
- `outbound_to` — which pages this page links to, with anchor and rationale
- `cluster_role` — hub / spoke / flagship / conversion / supporting

Minimum: 1 outbound to the booking page (Tier A/B), 1 outbound to the cluster
hub, 2 planned inbound links from existing pages. A brief with zero planned
inbound links creates an orphan and is rejected by QA.

---

## J. SNS repurposing decision

A07 decides **whether and where** a piece should be repurposed and *why*.
A10 decides **how**. The `sns_repurpose` block per channel carries:

`channel` · `viability` (`strong` / `possible` / `skip`) · `angle` ·
`objective` · `rationale`

Channels: `instagram`, `tiktok`, `x`, `youtube`, `threads`, `facebook`, `line`,
`ameba`, `note`. Pinterest and email newsletter are out of scope.

`skip` is a first-class answer. A shrine report with no usable photography is
not an Instagram post.

---

## K. Priority and capacity

Priority inherits P0–P3 from the SEO Opportunity but may be **downgraded** by
A07 on editorial grounds (weak angle, missing source material, cluster not
ready). It may not be upgraded past a seasonal deadline set by A06.

**Capacity is a hard constraint.** A07 maintains the editorial calendar against
the practitioner's stated monthly capacity for visits, judgments, and review
time. When the queue exceeds capacity, A07 does not issue more briefs — it
escalates to A01 Strategy Agent with a proposed cut list.
