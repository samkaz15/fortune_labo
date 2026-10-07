# fortune_labo

AI-driven operating system for a fortune-telling media and service business.

## Architecture

- **GitHub**: strategy, AI agents, prompts, WBS, content drafts, automation code, analytics specifications, and operational knowledge.
- **WordPress**: production website, landing pages, articles, and customer-facing experience.
- **Human approval**: required before public publishing or irreversible production changes.

## Phase 1

This repository starts as the management and automation foundation. Production WordPress changes are intentionally out of scope until the operating model and integration requirements are defined.

## Planned AI roles

1. Strategy Agent — business goals, priorities, WBS, decisions
2. Research Agent — market, competitors, audience, trends
3. SEO Agent — keyword strategy, search intent, content opportunities
4. Content Agent — articles, LP copy, repurposing
5. SNS Agent — X, Instagram, Threads, TikTok, Facebook, Ameba Blog
6. Analytics Agent — KPI monitoring and reporting
7. CRO Agent — LP conversion experiments and PDCA
8. QA Agent — factual, editorial, SEO, and release checks

## Operating loop

Research → Strategy → Build → Publish → Measure → Learn → Prioritize → Repeat

## Security

Secrets, API keys, tokens, passwords, and production credentials must never be committed to this repository. Use environment variables and `.env` files locally; only `.env.example` belongs in Git.

## Editorial intelligence foundation

The [editorial foundation](docs/editorial/README.md) contains public-safe structured insights, genre taxonomy, access and writing rules, schemas, and opaque source provenance. Private research and article bodies are excluded from this public repository. The [Google Search policy](docs/seo/GOOGLE_SEARCH_POLICY.md) remains a versioned proposal awaiting human approval. Existing A06 specifications remain unchanged.

Run the read-only checks from the repository root with Python 3:

```bash
python3 -B scripts/check_public_export.py --manifest docs/editorial/public-export-manifest.json
python3 -B scripts/validate_editorial.py --schemas-only
python3 -B scripts/verify_test_fixtures.py
python3 -B -m unittest discover -s tests -v
```

These checks validate the editorial artifacts; they do not authorize WordPress writes, publication, SNS posts, or scheduling.

[A07 Content Strategy](fortune_labo/agents/content-strategy/README.md) and [A08 Content Production](fortune_labo/agents/content-production/README.md) provide formal specifications, prompts, schemas and offline execution helpers. The [Content Index](docs/editorial/CONTENT_INDEX_SPEC.md) distinguishes zero existing WordPress articles from three explicitly authorized generated fixtures. [Comparison QA](docs/editorial/TEST_ARTICLE_COMPARISON.md) records the model review and remaining release blockers.
