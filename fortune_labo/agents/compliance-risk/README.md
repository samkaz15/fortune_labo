# A30 — Compliance/Risk Agent

Adjudicates **legal, regulatory, platform, privacy and reputational risk** for
everything fortune_labo publishes.

> **A30 was identified from the existing specification, not chosen.** It is
> already defined in [`AGENT-INDEX.md`](../../../docs/agents/AGENT-INDEX.md) §6
> as the Compliance/Risk Agent, and A06 SEO Agent already routes work to it.
> See [`A30-IDENTIFICATION.md`](../../../docs/agents/A30-IDENTIFICATION.md).

## What this agent is

**The compliance authority.** It owns layer 1 of the QA gate, and its blocking
verdicts cannot be overruled by any other agent.

```
   A07 brief (sensitive_domain flags)  ─┐   pre-drafting review
   A08 master_content                  ─┼──►  A30 COMPLIANCE/RISK
   A10 channel_content (all LINE)      ─┤
   A28 QA (layer 1 delegation)         ─┘
                                            │  risk_assessment.json
                                            ▼
                                        A28 enforces the verdict
                                            ▼
                                     HUMAN APPROVAL
                                            ▼
                                     WordPress / SNS
                                            │
                                            ▼
                              A30 monitors published content
```

## Why it is separate from A28 QA

A28 is the release gate, so it sits under deadline pressure — and a missed
seasonal window costs a full year (`../seo/positioning.md` §7).

**The agent under deadline pressure must not be the agent deciding what counts as
legal risk.** A30 has no throughput incentive, and A28 is structurally unable to
trade a blocking finding against a publication date.

## The regulatory context this exists for

Japan tightened regulation of spiritual-claim solicitation in 2022–2023:

- **Amended Consumer Contract Act** — effective 2023-01-05
- **Act on Prevention of Unjust Solicitation of Donations** — fully effective
  2023-06-01

Rescission windows for spiritual-knowledge-based solicitation were extended to
**3 years from realisation / 10 years from the act**, and family members may
exercise the right by subrogation. The exposure window on a single non-compliant
page is measured in years, not weeks.

A30 is not a style reviewer. It is the function that keeps a fortune-telling
business on the right side of a specific, recently tightened body of law.

## The dividing line

> **"Visiting is good" is permitted. "Not visiting is bad" is not.**

Inherited verbatim from [`../seo/rules.md`](../seo/rules.md) §4. Everything else
in this directory elaborates it.

## Files

| File | Purpose |
| --- | --- |
| [`mission.md`](./mission.md) | Mission, scope, authority, non-goals |
| [`responsibilities.md`](./responsibilities.md) | Six risk domains, check by check |
| [`inputs.md`](./inputs.md) | What arrives, and what must always be reviewed |
| [`outputs.md`](./outputs.md) | Risk Assessment, Risk Register, Regulatory Watch |
| [`workflow.md`](./workflow.md) | Review loop, incident response, monitoring |
| [`rules.md`](./rules.md) | Authority rules and the non-override rule |
| [`kpi.md`](./kpi.md) | Zero-incident stack |
| [`prompts/`](./prompts/) | System prompt + per-domain prompts |
| [`schemas/`](./schemas/) | `risk_assessment`, `risk_register_entry` |

## A30 is not a lawyer

A30 applies documented rules and escalates uncertainty to a human. Where a
question turns on genuine legal interpretation rather than an established rule,
A30's output is **"a qualified professional must review this"**, and that is a
blocking condition — not a judgment call it resolves itself.
