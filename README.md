# fortune_labo

AI-driven operating system for a fortune-telling media and service business.

## Architecture

- **GitHub**: strategy, AI agents, prompts, WBS, content drafts, automation code, analytics specifications, and operational knowledge.
- **WordPress**: production website, landing pages, articles, and customer-facing experience.
- **Human approval**: required before public publishing or irreversible production changes.

## Phase 1

This repository starts as the management and automation foundation. Production WordPress changes are intentionally out of scope until the operating model and integration requirements are defined.

## AI agents

The **content pipeline is implemented end to end.** Six agents are live; each has
a mission, rules, prompts, and JSON Schemas for its inputs and outputs.

| ID | Agent | Role | Spec |
| --- | --- | --- | --- |
| A06 | SEO Agent | Finds search demand worth capturing, and plans the shrine visits that supply it | [`agents/seo/`](./fortune_labo/agents/seo/) |
| A07 | Content Strategy Agent | Decides what to build, for whom, and why — including what **not** to build | [`agents/content-strategy/`](./fortune_labo/agents/content-strategy/) |
| A08 | Content Production Agent | Writes the article body from real source material, never from invention | [`agents/content-production/`](./fortune_labo/agents/content-production/) |
| A10 | SNS Content Agent | Re-cuts one piece natively for nine channels, or declines them | [`agents/sns-content/`](./fortune_labo/agents/sns-content/) |
| A28 | QA Agent | The release gate: seven check layers, one verdict | [`agents/qa/`](./fortune_labo/agents/qa/) |
| A30 | Compliance/Risk Agent | Adjudicates legal and regulatory risk with binding authority | [`agents/compliance-risk/`](./fortune_labo/agents/compliance-risk/) |

The full 42-agent map, with implementation status, is in
[`docs/agents/AGENT-INDEX.md`](./docs/agents/AGENT-INDEX.md).

## The pipeline

```text
   Research
      ↓
     SEO                  A06  · demand, keyword tiers, visit plans
      ↓
Content Strategy          A07  · what to build — and what to decline
      ↓
Content Production        A08  · the article body
      ↓
  SNS Content             A10  · nine channels, natively
      ↓
      QA  ◄── Compliance  A28 ◄── A30
      ↓
★ HUMAN APPROVAL ★             mandatory, structurally enforced
      ↓
WordPress / SNS                Codex publishes; a human posts
      ↓
  Analytics
      ↓
     SEO                       the loop closes
```

Every stage may refuse: A07 declines, A08 reports gaps, A10 skips a channel, A28
fails, A30 blocks. **A pipeline that never refuses is not working**, and each
agent's KPI structure treats an unnaturally clean record as a signal to
investigate.

| Document | What it covers |
| --- | --- |
| [`docs/agents/ARCHITECTURE.md`](./docs/agents/ARCHITECTURE.md) | How the agents fit together and the three structural guarantees |
| [`docs/agents/CONTENT-PIPELINE.md`](./docs/agents/CONTENT-PIPELINE.md) | The artifact chain and every handoff contract |
| [`docs/agents/CODEX-INTERFACE.md`](./docs/agents/CODEX-INTERFACE.md) | Judgment vs implementation; what Codex builds next |
| [`docs/agents/HUMAN-APPROVAL.md`](./docs/agents/HUMAN-APPROVAL.md) | The gate no agent may pass |
| [`content/`](./content/) | Where the pipeline's working artifacts live |

## Two rules the whole system is built around

**1. A human approves everything customer-facing.** No agent holds a publishing
path — not to WordPress, not to any social platform, not to LINE. This is
enforced in the JSON Schemas, not only in prose: A08 cannot mark its own draft
passed, A10 cannot set a post to `approved`, and A28 clears artifacts *for*
approval rather than approving them.

**2. AI never originates first-hand experience.** Shrine visits, atmosphere,
dates, photographs, and the practitioner's judgment come from recorded human
material. A08 may structure and tighten it; it may never invent it. A missing
source produces a gap report, never a plausible sentence. A28 verifies each claim
against the source line it rests on.

## Operating loop

Research → Strategy → Build → Publish → Measure → Learn → Prioritize → Repeat

## Security

Secrets, API keys, tokens, passwords, and production credentials must never be committed to this repository. Use environment variables and `.env` files locally; only `.env.example` belongs in Git.
