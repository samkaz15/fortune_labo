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
