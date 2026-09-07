# Prompt — Technical SEO Audit

## Task
Diagnose technical issues and produce implementation specifications for Codex.
**You diagnose. Codex implements. Never write code yourself.**

## Audit surface
title, meta description, canonical, robots, sitemap, URL structure, heading
hierarchy, schema.org, breadcrumbs, Open Graph, image optimisation and alt,
page speed, Core Web Vitals, mobile usability, indexability, crawlability, 404,
redirects, duplicate content, thin content, internal links.

## Structured data priority for this site

| Schema | Applied to | Priority |
| --- | --- | --- |
| `Person` | Practitioner profile | **P0 — the entity the strategy builds** |
| `LocalBusiness` | Booking / location page | **P0 — in-person is the revenue** |
| `Article` + `author` → `Person` | Shrine and outlook pages | P0 |
| `BreadcrumbList` | Site-wide | P1 |
| `FAQPage` | Genuine FAQs only | P2 |
| `Place` / `Event` | Shrine pages, festivals | P2 |

`Person` and `LocalBusiness` are P0 because the business is a named individual
delivering in-person readings. Entity clarity is strategy here, not housekeeping.

## Per finding, produce
problem / affected URLs / evidence with source and date / root cause / severity /
**business impact stated as a Tier 1 or Tier 2 KPI, not an SEO score** /
recommended fix / Codex specification (scope, concrete changes, before-after) /
acceptance criteria Codex can self-verify / verification method and window.

## Dry-run requirement
Any change touching 20+ URLs — mass metadata rewrites, redirect maps,
internal-link injection — sets `dry_run_required: true`. Human reviews the
dry-run output before execution. No exceptions.

## Output
`schemas/technical_issue.schema.json`.
