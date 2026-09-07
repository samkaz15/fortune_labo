# A30 — Identification Record

> Why A30 is the **Compliance/Risk Agent**, and why that was found rather than
> chosen.

## 1. A30 was already specified

A30 is **not** an unassigned slot. It is defined in the existing
[`AGENT-INDEX.md`](./AGENT-INDEX.md) §6 "Quality, risk & governance agents":

| ID | Agent | Primary mission | Main outputs | Priority |
|---|---|---|---|---|
| A30 | Compliance/Risk Agent | Detect legal, platform, privacy and reputational risks | Risk register, warnings, review requirements | P1 |

The task brief asked what "A30" means in the existing architecture. The answer is
in the repository, so no candidate selection was required. This document records
the identification and the corroborating evidence rather than inventing an
alternative.

## 2. Corroborating evidence across the existing specification

The A06 SEO Agent — the only agent implemented before this work — already depends
on a compliance function it does not itself own:

| Existing reference | What it implies |
| --- | --- |
| [`agents/seo/rules.md`](../../fortune_labo/agents/seo/rules.md) §4 | An entire ruleset headed "Compliance rules (blocking — legal exposure)", citing Japan's amended Consumer Contract Act (effective 2023-01-05) and the Act on Prevention of Unjust Solicitation of Donations (fully effective 2023-06-01) |
| [`agents/seo/outputs.md`](../../fortune_labo/agents/seo/outputs.md) | The QA gate order is **`compliance → factual → first-hand → editorial → SEO → technical`** — compliance is named as the *first* gate |
| [`agents/seo/schemas/seo_opportunity.schema.json`](../../fortune_labo/agents/seo/schemas/seo_opportunity.schema.json) | Carries a `compliance_flags` enum and `"type": "compliance"` as a first-class opportunity type |
| [`agents/seo/workflow.md`](../../fortune_labo/agents/seo/workflow.md) | Escalation trigger: "Compliance risk found in published content → **Human immediately; request unpublish**" |
| [`agents/seo/workflow.md`](../../fortune_labo/agents/seo/workflow.md) §Quarterly | "Regulatory review (has permissible-claim guidance changed?)" |

The architecture already routes work to a compliance owner. Before this change,
that owner did not exist, and the compliance gate was implicitly assigned to A28
QA Agent.

## 3. Why the function must be separate from A28

A28 QA Agent is the release gate and therefore sits under schedule pressure: it
is the agent standing between a finished draft and a seasonal deadline that
cannot slip (`agents/seo/positioning.md` §7 — a missed shrine window costs a full
year).

**The agent under deadline pressure must not be the agent deciding what counts as
legal risk.** Separating adjudication (A30) from orchestration (A28) means the
compliance verdict is issued by a function with no throughput incentive, and A28
is structurally unable to trade a blocking finding against a publication date.

This is the same separation-of-concerns logic the existing specification already
applies elsewhere: A06 diagnoses but Codex implements; A06 finds demand but A07
decides what deserves a page.

## 4. Why it is P0 in practice, not P1

The index lists A30 at P1. The implemented pipeline treats it as a **blocking
dependency of A28**, which is P0, for three reasons specific to this business:

1. **Named legal exposure.** Japan's 2022–2023 amendments extended rescission
   windows for spiritual-knowledge-based solicitation to 3 years from realisation
   / 10 years from the act, exercisable by family members through subrogation.
   The exposure window on a single non-compliant page is measured in years.
2. **The pipeline now publishes to ten surfaces.** With A10 in place, one piece
   of content can reach nine social channels plus the website. Compression on
   short-form channels is precisely where guarantees and fear framing appear.
3. **Sensitive domains are unavoidable.** Fortune-telling content touches
   health, money, relationships, and major life decisions by its nature. Every
   one of those is a domain where a divinatory claim can become a regulated
   claim.

The index priority is left unchanged; the pipeline wiring makes the dependency
explicit instead.

## 5. Scope boundary against neighbouring agents

| Agent | Owns | Does not own |
| --- | --- | --- |
| **A28 QA** | The release gate, six other check layers, verdict, routing | Deciding what is a compliance violation |
| **A29 Fact-Check** | Verifying factual claims and sources | Legal and regulatory judgment |
| **A30 Compliance/Risk** | Legal, regulatory, platform, privacy and reputational risk adjudication; the risk register; the regulatory watch | Content quality, SEO, publishing, gate orchestration |
| **A31 Security** | Credentials, integrations, operational access | Content risk |
| **A32 Editorial** | Consistency, readability, brand quality | Risk |

A29, A31 and A32 remain unimplemented. Where their scope overlaps A30 today —
fact-checking a claim that is also a risk claim, for instance — A30 handles the
risk dimension only and flags the rest.

## 6. Implementation

[`fortune_labo/agents/compliance-risk/`](../../fortune_labo/agents/compliance-risk/),
following the same file convention as A06 SEO Agent.
