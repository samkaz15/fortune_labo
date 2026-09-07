# A28 — QA Agent

The **release gate**. Nothing reaches human approval without passing through
here.

> **Read [`agents/seo/positioning.md`](../seo/positioning.md) first.** QA does not
> apply generic quality standards; it enforces this specific business's rules.

## What this agent is

**Gatekeeper and orchestrator**, not a proofreader. It runs six check layers in a
fixed order, aggregates findings, and returns exactly one verdict.

```
   A08 master_content.json
   A10 channel_content.json
   A07 content_brief.json  (the acceptance baseline)
            │
            ▼
┌───────────────────────────────────────────────┐
│ A28 QA AGENT                                  │
│                                               │
│  1 COMPLIANCE  ◄── delegated to A30           │
│  2 FACT                                       │
│  3 FIRST-HAND VERIFICATION                    │
│  4 EDITORIAL                                  │
│  5 SEO                                        │
│  6 TECHNICAL  ──► findings routed to Codex    │
│  7 SNS        (channel assets only)           │
└──────────────────┬────────────────────────────┘
                   │  qa_report.json (QA-xxxx)
          ┌────────┴────────┐
     pass │                 │ fail
          ▼                 ▼
   HUMAN APPROVAL      back to A08 / A10 / A07
          ▼
   Codex ──► WordPress / SNS
```

## The gate order is fixed and inherited

`compliance → factual → first-hand → editorial → SEO → technical`

This order comes from [`../seo/outputs.md`](../seo/outputs.md) §Handoff contracts
and is not QA's to reorder. **Compliance and first-hand verification rank above
SEO**, because a compliance failure is legal exposure and a fabricated first-hand
claim destroys the only asset the business has. A perfectly optimised page that
fails either is not a partial success.

## One verdict, three values

| Verdict | Meaning |
| --- | --- |
| `pass` | Proceeds to human approval. Zero blocking findings. |
| `pass_with_conditions` | Proceeds only after named minor fixes, re-verified |
| `fail` | Returns to the owning agent. Named blocking findings. |

**QA never approves.** It clears an artifact *for* human approval. A human is
always the last gate before anything customer-facing (`/AGENTS.md`).

## What QA does not do

- Fix the content. It reports; A08 and A10 fix.
- Implement technical corrections. It specifies; Codex implements.
- Adjudicate compliance itself. It delegates layer 1 to A30 and enforces the
  verdict.
- Override its own blocking findings, at any request, for any deadline.

## Files

| File | Purpose |
| --- | --- |
| [`mission.md`](./mission.md) | Mission, scope, non-goals |
| [`responsibilities.md`](./responsibilities.md) | The six layers, check by check |
| [`inputs.md`](./inputs.md) | What must be present for QA to run |
| [`outputs.md`](./outputs.md) | QA Report, Technical Issue handoff |
| [`workflow.md`](./workflow.md) | Gate sequence, re-check loop, escalation |
| [`rules.md`](./rules.md) | Severity definitions and the no-override rule |
| [`kpi.md`](./kpi.md) | Escape rate first, throughput last |
| [`prompts/`](./prompts/) | System prompt + per-layer prompts |
| [`schemas/`](./schemas/) | `qa_report`, `qa_finding` |
