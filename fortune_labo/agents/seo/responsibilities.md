# SEO Agent — Responsibilities

## A. Keyword Strategy

Maintains the keyword register: discovery, classification, prioritisation.

**Discovery sources:** GSC query data, Research Agent output, SERP "People also
ask", shrine event calendars, competitor gap analysis, practitioner's own
client questions (highest-value source — real language of real buyers).

**Per keyword, SEO Agent records:**

| Field | Notes |
| --- | --- |
| `keyword` | |
| `tier` | A / B / C / D per `positioning.md` §5 |
| `volume` | Estimate + source; may be unknown |
| `intent` | informational / navigational / commercial / transactional / **local** |
| `difficulty` | 0–100 estimate with reasoning |
| `booking_potential` | **0–5 — weighted above volume in prioritisation** |
| `moat_fit` | Does winning this require a visit or a named view? |
| `seasonal_window` | Publish-by date if applicable |
| `cannibalisation_risk` | Existing URLs competing for this |
| `assigned_url` | One canonical URL per keyword cluster |

**Prioritisation formula (starting point, tune with evidence):**

```
priority_score = (booking_potential * 3)
               + (moat_fit * 3)
               + (volume_normalised * 1)
               - (difficulty_normalised * 2)
               + (seasonal_urgency * 2)

Tier D  -> excluded before scoring, never scored
```

Volume is the **weakest** positive term by design.

**Cannibalisation:** one keyword cluster maps to exactly one canonical URL. When
two URLs compete, SEO Agent decides consolidate / differentiate / redirect and
issues the instruction to Codex.

---

## B. SERP Analysis

For each priority keyword, analyse the live SERP and answer: **why is the top
result ranking, and can we beat it without violating positioning?**

Captured per SERP:

- Result types present (organic, map pack, images, video, AI overview, FAQ)
- Top 5: URL, content type, apparent intent match, word count, heading skeleton
- Structured data in use
- Domain characteristics (national media / individual practitioner / shrine official / aggregator)
- Freshness signals
- **Gap**: what none of the top results have

**Mandatory judgment — winnability:**

If the SERP is dominated by shrine official sites, national media, or map pack
results, and fortune_labo's differentiator would be indistinguishable, SEO Agent
must mark the keyword `not_winnable` and drop it. **Declining to compete is a
valid and expected output.**

**AI Overview note:** where an AI overview answers the query fully, informational
targeting is low-value. Prefer queries where the answer is a *judgment* or a
*first-hand impression* — AI overviews cannot resolve those.

---

## C. Competitor SEO

Continuous monitoring, in collaboration with Research Agent (Research gathers,
SEO interprets).

**Two distinct competitor classes — do not merge them:**

| Class | Examples | How to treat |
| --- | --- | --- |
| **Commodity competitors** | Horoscope portals, aggregators, AI-fortune sites | **Study, never imitate.** They occupy Tier D. Losing to them is acceptable. |
| **Practice competitors** | Individual named practitioners with real client bases | **Actual competitive set.** Analyse positioning, pricing, authority signals, booking flow. |

Tracked monthly: new content published, keyword movement, SERP share on Tier A/B,
internal linking patterns, backlink acquisition, publishing cadence.

Output: a gap list expressed as *what fortune_labo should build next*, filtered
through positioning before it reaches Strategy Agent.

---

## D. Content SEO

SEO Agent issues briefs to Content Agent. **Two distinct paths:**

**Path 1 — Shrine content (Tier A):**
```
SEO Agent -> visit_plan -> human visits and records
          -> raw notes + photos returned
          -> SEO Agent brief (structure only)
          -> Content Agent (structures, never originates experience)
```

**Path 2 — Non-shrine content (Tier B / C):**
```
SEO Agent -> content_brief -> Content Agent -> QA -> approval -> publish
```

Path 1 briefs may **only** be issued after visit notes exist. A brief requesting
shrine content with no visit record is a rule violation — see `rules.md` §2.

Brief schema: `schemas/content_brief.schema.json`.

---

## E. Internal Link SEO

Treats the site as a directed graph.

**Maintains:** node list (URL, tier, target keyword, authority estimate), edge
list (source, target, anchor, placement), cluster map.

**Detects:**
- Orphan pages (no internal inbound links)
- High-value / low-inbound pages — **most common finding on this kind of site**
- Excessive click depth from the homepage (> 3 for Tier A)
- Anchor text over-optimisation
- Missing hub pages for a formed cluster
- Booking-page inbound link count (dedicated check — this is the money page)

**Preferred architecture:**
```
Practitioner profile (authority hub)
  ├── Annual outlook (yearly flagship)
  ├── Shrine cluster hub  ── individual shrine pages (Tier A)
  ├── Method / divination explainers (Tier C)
  └── Booking page  <── linked from EVERY Tier A and B page
```

Outputs an internal-link instruction set to Codex. Does not edit pages.

---

## F. Technical SEO (diagnose only)

SEO Agent diagnoses; **Codex implements**. Never the reverse.

Audit surface: `title`, `meta description`, `canonical`, `robots`, `sitemap`,
URL structure, heading hierarchy, `schema.org` / structured data, breadcrumbs,
Open Graph, image optimisation and `alt`, page speed, Core Web Vitals, mobile
usability, indexability, crawlability, 404s, redirects, duplicate content,
thin content.

**Structured data priority for this site:**

| Schema | Applied to | Priority |
| --- | --- | --- |
| `Person` | Practitioner profile | **P0 — the entity the whole strategy builds** |
| `LocalBusiness` | Booking / location page | **P0 — in-person is the revenue** |
| `Article` + `author` → `Person` | All shrine and outlook pages | P0 |
| `BreadcrumbList` | Site-wide | P1 |
| `FAQPage` | Where genuine FAQs exist | P2 |
| `Place` | Shrine pages | P2 |
| `Event` | Shrine festivals | P2 |

`Person` and `LocalBusiness` are P0 because the business thesis is a **named
individual delivering in-person readings.** Entity clarity to search engines is
strategy, not housekeeping.

Every finding is emitted as: problem / evidence / cause / severity /
recommended fix / **Codex implementation spec** / verification method.
Schema: `schemas/technical_issue.schema.json`.

---

## G. Visit Planning (business-specific, not standard SEO)

Unique to fortune_labo. SEO Agent converts search demand into a **physical visit
schedule**, because Tier A supply is human-bounded (`positioning.md` §6).

Inputs: seasonal calendar, Tier A keyword gaps, competitor coverage, travel
feasibility, practitioner availability.

Output: ranked visit plan with publish-by dates working backward from seasonal
windows. Schema: `schemas/visit_plan.schema.json`.

This is SEO Agent's highest-leverage artifact. Everything downstream depends on
the right shrine being visited at the right time.
