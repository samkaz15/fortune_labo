# SEO Agent — Integration Policy

## Principle

SEO Agent has **read access to data, write access to nothing.** All writes are
executed by Codex after human approval, per `/AGENTS.md`.

---

## Google Search Console

| Item | Value |
| --- | --- |
| API | Search Console API (`searchanalytics.query`, `urlInspection.index.inspect`) |
| Access | **Read only** |
| Auth | Service account, credentials via env vars — never in Git |
| Owner | Analytics Agent fetches; SEO Agent interprets |
| Phase | 2 |

Pulled: query/page/country/device dimensions, clicks, impressions, CTR,
position, index status, CWV field data.

**Not permitted:** URL removal requests, sitemap submission, or any state-changing
GSC call from SEO Agent. Those are Codex actions with human approval.

## Google Analytics 4

| Item | Value |
| --- | --- |
| API | GA4 Data API (`runReport`) |
| Access | **Read only** |
| Phase | 2 (traffic), 3 (booking attribution) |

Required custom events for Tier 1 KPIs (Codex implements, Phase 3):

```
booking_start        booking form opened
booking_complete     booking confirmed        <- KGI event
list_signup          LINE / email registration
shrine_page_view     with shrine_id parameter
```

Without `booking_complete`, Tier 1 KPIs cannot be measured and SEO Agent must
explicitly label all prioritisation as **proxy-based**. This is a known Phase 1–2
limitation and must be stated in every report until Phase 3.

## WordPress

| Phase | Access | Method |
| --- | --- | --- |
| 1 | None | Human-supplied exports |
| 2 | **Read only** | REST API, application password, least privilege |
| 3 | Write via Codex only | Authenticated, explicitly scoped, dry-run first |

Per `/AGENTS.md`: *any WordPress write operation must be authenticated and
explicitly scoped.* SEO Agent never holds write credentials — not as policy
preference but as a structural safeguard.

Recommended plugin surface kept minimal: one SEO plugin (Yoast or SEO SIMPLE
PACK) plus a schema layer. Every plugin is a maintenance and speed liability.

## Codex handoff

```
SEO Agent  ──► technical_issue.json ──►  Codex
                                          │
                     branch → implement → test → PR
                                          │
                                     QA Agent
                                          │
                                   HUMAN APPROVAL
                                          │
                                       merge → deploy
                                          │
                    SEO Agent ◄── verification (measurement_kpi)
```

Every `technical_issue` must contain acceptance criteria specific enough for
Codex to self-verify. A technical issue without a verification method is
incomplete and QA rejects it.

**Dry-run requirement:** production integrations must have a dry-run or preview
mode where practical (`/AGENTS.md`). Bulk operations — mass metadata rewrites,
redirect maps, internal-link injection — require dry-run output reviewed by a
human before execution, without exception.

## Secrets

Never committed. `.env` locally, `.env.example` in Git only, secrets in GitHub
Actions Secrets for CI. Per `/AGENTS.md` §Engineering rules.

## Rate limits and cost

GSC and GA4 APIs are quota-limited. Analytics Agent caches daily pulls to
`data/` (git-ignored). SEO Agent reads cache, never calls APIs directly — this
keeps SEO Agent deterministic and independently testable.
