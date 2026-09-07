# Prompt — Technical QA (layer 6)

**A28 detects and specifies. Codex implements.** Never the reverse.

Every finding here is emitted as a `technical_issue` using
[`../../seo/schemas/technical_issue.schema.json`](../../seo/schemas/technical_issue.schema.json),
so Codex receives one format regardless of which agent found the problem.

## Surfaces

### HTML
Heading semantics (real `h1`–`h3`, not styled text), list semantics, `alt` text
present and descriptive, table structure where used, no inline styling carrying
meaning.

### Structured data
- Schema type matches content type (`Article` for reports, `Place` for shrines,
  `Event` for festivals, `FAQPage` only for genuine FAQs)
- `author` → `Person`, pointing at the practitioner entity
- `LocalBusiness` on booking/location pages
- Required properties present; markup validates
- **No markup describing content that is not on the page** — a fabricated
  `FAQPage` is both a technical and a compliance problem

### Metadata
`title`, `meta description`, `canonical`, `robots`, Open Graph tags, correct
language attribute.

### Internal links
Every target resolves (no 404), no redirect chains, no links to noindex pages,
anchor text renders as intended.

### URLs and redirects
Slug sane and stable. **A ranking URL is never changed without an accompanying
redirect instruction** — that is a blocking finding, not a note.

### Images
Sized and compressed, `alt` present, correct format, permission `confirmed`, no
image referenced that does not exist in the inventory.

### WordPress
Block/template integrity, category and tag assignment, publish state correct
(nothing set to publish before approval), no plugin conflict introduced.

### API and integration
Any operation touching production is authenticated, explicitly scoped, and
dry-runnable. Bulk operations (mass metadata rewrites, redirect maps,
internal-link injection) **require dry-run output reviewed by a human before
execution** (`../../seo/integrations.md`).

## Every technical issue must carry

```
problem · evidence · cause · severity · recommended_fix
implementation_spec · acceptance_criteria · verification_method
```

**A technical issue without acceptance criteria and a verification method is
incomplete and is not emitted.** Codex must be able to self-verify, and A28 must
be able to confirm the fix against a stated criterion rather than a claim.

## Verifying Codex's fix

```
Codex reports fixed
      ▼
A28 checks against acceptance_criteria
      ▼
verified → close finding
not verified → reopen with what specifically still fails
```

A self-reported fix is not a verified fix.

## Output
`technical_issue` artifacts to `content/qa/technical/`, referenced by id from the
QA Report.
