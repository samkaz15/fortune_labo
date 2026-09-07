# content/

Working artifacts produced by the content pipeline. Every file here conforms to a
JSON Schema in [`fortune_labo/agents/*/schemas/`](../fortune_labo/agents/).

## Layout

```
content/
├── briefs/       CB-xxxx.json     A07 Content Strategy — editorial commitments
├── declines/     DEC-xxxx.json    A07 — opportunities deliberately not built
├── calendar/     CAL-yyyy-mm.json A07 — rolling 90-day plan
├── drafts/       MC-xxxx.json     A08 Content Production — master content
├── gaps/         GAP-xxxx.json    A08 — briefs that cannot be written honestly
├── sns/          CC-xxxx.json     A10 SNS Content — per-channel assets
│   └── plans/    RP-xxxx.json     A10 — rollout proposals
├── qa/           QA-xxxx.json     A28 QA — verdicts
│   └── technical/                 A28 — technical_issue artifacts for Codex
└── compliance/   RISK-xxxx.json   A30 Compliance/Risk — assessments
    └── register/ REG-xxxx.json    A30 — the standing risk register
```

See [`docs/agents/CONTENT-PIPELINE.md`](../docs/agents/CONTENT-PIPELINE.md) for
the artifact chain and the handoff contracts.

## Rules

### Never commit

- **API keys, passwords, access tokens, WordPress credentials** — of any kind, in
  any file, ever (`/AGENTS.md`)
- **Client-identifying information.** Client stories are anonymised at the source
  and require a recorded consent; the consent record itself does not live here.
- Personal data of any identifiable individual
- Raw analytics exports (git-ignore them under `data/`)

### Always

- Validate against the schema before committing. The schemas encode the safety
  rules — first-hand traceability, human approval, compliance gates — so an
  artifact that does not validate has usually broken one of them.
- Keep revisions. A revised draft is a new revision, not an overwrite: the QA
  trail is the audit trail.
- Record refusals. Declines, gaps, and skips are committed like any other
  artifact. A pipeline that never refuses is not working.

### Approval state lives in the artifact

Nothing in this directory is published. `approved` and `posted` states require a
recorded human approver and timestamp — see
[`docs/agents/HUMAN-APPROVAL.md`](../docs/agents/HUMAN-APPROVAL.md).
