# Agent Architecture

> How fortune_labo's AI agents fit together, and where the boundaries are.

## The operating loop

```text
        Research
            │
            ▼
           SEO
            │
            ▼
    Content Strategy
            │
            ▼
   Content Production
            │
            ▼
      SNS Content
            │
            ▼
            QA  ◄──────── Compliance/Risk
            │
            ▼
    ★ HUMAN APPROVAL ★
            │
            ▼
        Publish
            │
            ▼
       Analytics
            │
            ▼
           SEO          (loop closes)
```

Implemented agents in that loop:

| Stage | Agent | Status |
| --- | --- | --- |
| Research | A02 Research Agent | ⬜ Not implemented |
| SEO | [A06 SEO Agent](../../fortune_labo/agents/seo/) | ✅ |
| Content Strategy | [A07 Content Strategy Agent](../../fortune_labo/agents/content-strategy/) | ✅ |
| Content Production | [A08 Content Production Agent](../../fortune_labo/agents/content-production/) | ✅ |
| SNS Content | [A10 SNS Content Agent](../../fortune_labo/agents/sns-content/) | ✅ |
| QA | [A28 QA Agent](../../fortune_labo/agents/qa/) | ✅ |
| Compliance/Risk | [A30 Compliance/Risk Agent](../../fortune_labo/agents/compliance-risk/) | ✅ |
| Human approval | — | ✅ Mandatory gate, structurally enforced |
| Publish | Codex | Interface defined ([`CODEX-INTERFACE.md`](./CODEX-INTERFACE.md)) |
| Analytics | A18 Analytics Agent | ⬜ Not implemented |

---

## Full picture with roles and gates

```text
  ┌──────────────────────────────────────────────────────────────┐
  │                     DECIDE WHAT MATTERS                      │
  │   A01 Strategy ⬜        A02 Research ⬜                       │
  └────────────────────────────┬─────────────────────────────────┘
                               ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                      FIND THE DEMAND                         │
  │   A06 SEO Agent ✅                                            │
  │   keyword tiers · SERP · internal links · visit planning     │
  │        │                                                     │
  │        └──► visit_plan ──► ★ HUMAN VISIT ★ ──► notes+photos  │
  └────────────────────────────┬─────────────────────────────────┘
                               ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                   DECIDE WHAT TO BUILD                       │
  │   A07 Content Strategy ✅                                     │
  │   build / rewrite / consolidate / DECLINE · persona · angle  │
  └────────────────────────────┬─────────────────────────────────┘
                               ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                        MAKE IT                               │
  │   A08 Content Production ✅        A10 SNS Content ✅          │
  │   article body, FAQ, CTA          9 channels, natively       │
  └────────────────────────────┬─────────────────────────────────┘
                               ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                       CHECK IT                               │
  │   A28 QA ✅  ◄── layer 1 delegated ──►  A30 Compliance ✅      │
  │   7 layers, one verdict                binding authority     │
  └────────────────────────────┬─────────────────────────────────┘
                               ▼
  ┌──────────────────────────────────────────────────────────────┐
  │              ★ HUMAN APPROVAL — MANDATORY ★                  │
  │   No agent publishes, posts, or messages a customer.         │
  └────────────────────────────┬─────────────────────────────────┘
                               ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                       SHIP IT                                │
  │   Codex — WordPress, HTML, schema, redirects, integrations   │
  │   Human — social posting                                     │
  └────────────────────────────┬─────────────────────────────────┘
                               ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                      MEASURE IT                              │
  │   A18 Analytics ⬜  →  GSC · GA4 · bookings  →  back to A06   │
  └──────────────────────────────────────────────────────────────┘
```

---

## The three structural guarantees

Everything else in this architecture exists to serve these.

### 1. Human approval is unavoidable

No implemented agent holds a publishing path.

| Agent | Can it publish? | Enforced by |
| --- | --- | --- |
| A06 | No — read access to data, write access to nothing | `seo/integrations.md` |
| A07 | No — issues briefs only | `content-strategy/rules.md` §6 |
| A08 | No — cannot even mark its own draft passed | `master_content` schema (`status` enum) |
| A10 | No — no platform credentials, no scheduler | `channel_content` schema (`human_approval_required: true`) |
| A28 | No — clears *for* approval, never approves | `qa_report` schema (fixed `approval_note`) |
| A30 | No — recommends unpublish, never acts | `compliance-risk/rules.md` §1.6 |

This is enforced in the **schemas**, not only in prose, so a violation is
malformed data rather than a judgment call.

### 2. AI cannot originate first-hand experience

The moat is the practitioner's actual shrine visits and stated views
(`seo/positioning.md` §3). The chain that protects it:

```
visit_plan → HUMAN VISIT → visit record in repo
    → content_brief.visit_record_id       (schema-required for first-hand types)
    → master_content.source_map           (with verbatim_anchor per section)
    → A28 layer 3                          (claim vs anchor — catches extrapolation)
    → A30 domain C                         (untraceable claim = misrepresentation)
```

A08 may structure and tighten human material. It may never originate it, and a
missing source is a gap report rather than a sentence.

### 3. Compliance authority is separated from schedule pressure

A28 is the release gate and therefore sits under deadline pressure. A30 has no
throughput incentive and adjudicates compliance independently.

**A28 cannot overrule, downgrade, or pass around an A30 blocking finding.** Only a
human may accept a flagged risk, on the record. See
[`A30-IDENTIFICATION.md`](./A30-IDENTIFICATION.md) §3.

---

## Judgment vs implementation

```
  WHAT should change and why          HOW it is implemented
 ─────────────────────────────       ──────────────────────
  A06  "add 3 internal links"    ──►  Codex edits templates
  A07  "rewrite this page"       ──►  A08 writes, Codex publishes
  A28  "the schema is invalid"   ──►  Codex fixes the markup
  A30  "this wording is a risk"  ──►  A08/A10 apply the reworing
```

The AI agents decide; **Codex implements**; a human approves the boundary between
them. No agent both decides and executes on production.
[`CODEX-INTERFACE.md`](./CODEX-INTERFACE.md) defines the contract.

---

## Refusal paths are part of the design

| Agent | Refusal | Healthy state |
| --- | --- | --- |
| A06 | `not_winnable`, Tier D exclusion | Declining to compete is expected output |
| A07 | `decline_record` | 30–60% decline rate |
| A08 | `content_gap_report` | Zero gaps on first-hand-heavy months is **suspicious** |
| A10 | `skip` per channel | Two strong posts beat nine weak ones |
| A28 | `fail` | Zero findings is a warning sign, not an achievement |
| A30 | `block` | But a rising false-positive rate means it will be routed around |

**A pipeline that never refuses is not working.** Every agent's KPI structure
treats an unnaturally clean record as a signal to investigate.

---

## KPI inheritance

Every implemented agent inherits the same KGI and reports in the same order.

```
KGI: organic-sourced booked readings with a named practitioner

Tier 1  business outcome / trustworthiness / escape prevention
Tier 2  moat and authority
Tier 3  diagnostics — never reported as achievement alone
```

No agent has an independent success definition. This is deliberate: it prevents
any single function from succeeding while the business does not — the failure
mode `seo/positioning.md` §4 was written to prevent.

| Agent | Tier 1 is about | Tier 3 (diagnostic only) |
| --- | --- | --- |
| A06 | Bookings, revenue, CVR | Clicks, impressions, position |
| A07 | Decision quality, decline rate | Briefs issued |
| A08 | Fabrication = 0, traceability = 1.0 | Word count, turnaround |
| A10 | Social-sourced bookings, LINE retention | Reach, followers |
| A28 | Escape rate = 0 | Pass rate, turnaround |
| A30 | Published violations = 0 | Findings count, turnaround |

---

## Not yet implemented

| Agent | Why it matters to this pipeline | Priority |
| --- | --- | --- |
| **A18 Analytics** | The loop cannot close without it; every priority ordering stays labelled `proxy_based` until booking attribution exists | **Next** |
| **A02 Research** | A06 currently works from manual observation | High |
| **A01 Strategy** | Receives every escalation this pipeline generates and currently has no home | High |
| A09 SNS Strategy | A10 operates on defaults without it | Medium |
| A29 Fact-Check | A28 layer 2 covers the basics today | Medium |
| A32 Editorial | A28 layer 4 covers the basics today | Low |
| A05 Brand | A08 and A10 use a baseline voice definition | Low |

Per `AGENT-INDEX.md`: agents are added when the operating bottleneck justifies
them, not because a slot exists.
