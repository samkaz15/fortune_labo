# Codex Interface

> The division of labour between the judgment agents and the engineering agent.

## The split

```
   AI AGENTS decide WHAT should change and why
              │
              ▼
        technical_issue.json
              │
              ▼
   CODEX decides HOW to implement it
```

| Agent | Says | Codex does |
| --- | --- | --- |
| A06 SEO | "This page needs 3 internal links from the shrine hub" | Edits the template, adds the links, opens a PR |
| A07 Content Strategy | "These two URLs should consolidate into one" | Implements the redirect and the canonical |
| A08 Content Production | (nothing directly — reaches Codex only after approval) | Publishes the approved draft |
| A28 QA | "The `Article` markup is missing `author`" | Fixes the structured data |
| A30 Compliance/Risk | "This wording must change" | (nothing — A08/A10 apply rewordings; Codex publishes the result) |

**No judgment agent writes code. Codex makes no editorial, SEO, or compliance
decisions.** Where Codex believes a specification is wrong, it says so and returns
it — it does not silently implement something different.

---

## The one artifact Codex receives

Every technical instruction, from any agent, uses
[`agents/seo/schemas/technical_issue.schema.json`](../../fortune_labo/agents/seo/schemas/technical_issue.schema.json).

One format, regardless of origin. A28 deliberately reuses A06's schema rather
than defining its own so Codex has a single input contract.

```
problem · evidence · cause · severity · recommended_fix
implementation_requirement · acceptance_criteria · verification_method
```

**A technical issue without acceptance criteria and a verification method is
incomplete and is not emitted.** Codex must be able to self-verify, and the
issuing agent must be able to confirm the fix against a stated criterion rather
than a claim.

---

## Codex's surface

| Area | Examples |
| --- | --- |
| **WordPress** | Templates, blocks, taxonomy, publish state, plugin configuration |
| **HTML** | Heading semantics, list semantics, `alt` attributes, accessible markup |
| **Structured data** | `Article`, `Person`, `Place`, `Event`, `FAQPage`, `BreadcrumbList`, `LocalBusiness` |
| **Metadata** | `title`, `meta description`, `canonical`, `robots`, Open Graph |
| **Internal links** | Link injection, anchor updates, hub/spoke wiring |
| **Redirects** | Redirect maps, consolidation, URL changes |
| **Images** | Compression, sizing, format, `alt` implementation |
| **Integrations** | GSC/GA4 read clients, WordPress API, booking events |
| **Automation** | Scheduled pulls, caching, validation scripts, CI |

### Structured data priorities for this site

Carried from `agents/seo/responsibilities.md` §F — these are strategy, not
housekeeping, because the business thesis is a **named individual delivering
in-person readings**:

| Schema | Applied to | Priority |
| --- | --- | --- |
| `Person` | Practitioner profile | **P0** |
| `LocalBusiness` | Booking / location page | **P0** |
| `Article` + `author` → `Person` | Shrine and outlook pages | P0 |
| `BreadcrumbList` | Site-wide | P1 |
| `FAQPage` | **Only where genuine FAQs exist** | P2 |
| `Place`, `Event` | Shrine pages, festivals | P2 |

Marking up an FAQ the page does not actually answer is both a technical and a
compliance problem, and A28 blocks it.

---

## The implementation loop

```
issuing agent ──► technical_issue.json
                        │
                        ▼
                  ★ HUMAN APPROVAL ★     required before any production change
                        │
                        ▼
                     Codex
              branch → implement → test → PR
                        │
                        ▼
                     A28 QA
           verifies against acceptance_criteria
                        │
                        ▼
                  ★ HUMAN APPROVAL ★     required before merge/deploy
                        │
                        ▼
                  merge → deploy
                        │
                        ▼
        issuing agent verifies measurement_kpi
```

**Two human gates**, not one: approval of the change, and approval of the merge.
A self-reported fix is not a verified fix — A28 checks it against the stated
acceptance criterion.

---

## Non-negotiable engineering constraints

Inherited from `/AGENTS.md` and `agents/seo/integrations.md`.

### Secrets

**Never committed.** `.env` locally, `.env.example` in Git only, GitHub Actions
Secrets for CI. No API key, password, token, WordPress application password, or
production credential appears in this repository, in any artifact, at any time.

### Least privilege

| Phase | WordPress access |
| --- | --- |
| 1 | None — human-supplied exports |
| 2 | **Read only** — REST API, application password, least privilege |
| 3 | Write via Codex only — authenticated, explicitly scoped, dry-run first |

No judgment agent ever holds write credentials. That is a structural safeguard,
not a policy preference.

### Dry-run requirement

Bulk operations — mass metadata rewrites, redirect maps, internal-link injection —
**require dry-run output reviewed by a human before execution, without
exception.**

### No autonomous production change

Codex never deploys to production without human approval, never publishes
content, never posts to a social platform, and never sends a customer message.
Where social posting is eventually automated, the integration **must still require
explicit per-post human approval**.

---

## What Codex should build next

Ordered by what unblocks the most of this pipeline.

| # | Task | Unblocks |
| --- | --- | --- |
| 1 | **GA4 booking events** — `booking_start`, `booking_complete`, `list_signup`, `shrine_page_view` | Tier 1 KPIs across every agent. Until `booking_complete` exists, every priority ordering in the system stays labelled `proxy_based`. |
| 2 | **Schema validation in CI** — validate every artifact in `content/` against its JSON Schema on push | Makes the structural guarantees real rather than documentary |
| 3 | **`Person` + `LocalBusiness` structured data** | P0 entity clarity — the whole strategy is a named practitioner |
| 4 | **GSC + GA4 read clients with caching to a git-ignored `data/`** | A06's weekly loop; A18 Analytics |
| 5 | **WordPress read-only client** | URL inventory, publish dates, internal link graph — needed for A07 rewrite triage and A28 cannibalisation checks |
| 6 | **Secret-scanning pre-commit hook** | Enforces the secrets rule mechanically |
| 7 | Artifact id allocator (`CB-`, `MC-`, `CC-`, `QA-`, `RISK-`) | Prevents id collisions across agents |
| 8 | Publishing pipeline: approved `master_content` → WordPress draft (never published state) | Removes manual transcription while keeping the human gate |

Item 2 is worth doing early: the schemas in this repository encode the safety
rules, and validating them in CI turns "A08 must not fabricate" from a document
into a build failure.
