# AGENTS.md

## Mission

Build and operate fortune_labo as an AI-assisted business operating system for a fortune-telling website and its acquisition channels.

## Repository role

This repository is the source of truth for:

- business strategy and decisions
- WBS and project plans
- AI-agent specifications
- prompts and operating procedures
- content drafts and reusable content assets
- SNS planning
- analytics and KPI definitions
- CRO experiment definitions
- automation and integration code

The production WordPress site is a separate system of record for published customer-facing content.

## AI role separation

- Strategy: priorities, hypotheses, decisions, WBS
- Research: evidence gathering and competitor/audience research
- SEO: search demand, intent, information architecture, internal linking
- Content: drafts and content repurposing
- SNS: channel-specific distribution and creative variations
- Analytics: KPI collection, diagnosis, reporting
- CRO: experiments, hypotheses, conversion improvements
- QA: factual, editorial, technical, SEO, and release checks

AI agents should produce artifacts that another agent or a human can inspect and reuse.

## Publishing rule

No agent may autonomously publish customer-facing content or make irreversible production changes without explicit human approval.

Required flow:

1. Draft
2. QA
3. Human approval
4. Publish
5. Measure
6. Record result

## Engineering rules

- Keep secrets out of Git.
- Prefer small, reviewable changes.
- Document assumptions when requirements are unknown.
- Do not invent business facts, customer claims, credentials, reviews, or performance results.
- Use evidence for research-driven decisions.
- Production integrations must have a dry-run or preview mode where practical.
- Any WordPress write operation must be authenticated and explicitly scoped.

## Decision hierarchy

1. User's explicit business objective
2. Measured KPI evidence
3. Verified research
4. Strategic hypotheses
5. Agent suggestions

When evidence conflicts with an existing hypothesis, update the hypothesis rather than forcing the evidence to fit.
