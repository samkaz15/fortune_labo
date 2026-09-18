# X Content Agent (A10-X)

X（旧Twitter）向けの企画・制作エージェント。
テーマは **歴史・日本文化 × 開運アクション × 占い × 日常生活**。

> **Start with [`positioning.md`](./positioning.md).** It constrains everything
> else in this directory and overrides standard social-media practice where they
> conflict.

## What this agent is

**Channel content producer.** Plans themes, expands them into angles, writes
posts. Does not decide business priority, does not verify its own facts, does
not publish.

```
   A06 SEO Agent          search demand · Tier A/B gaps · seasonal calendar
   A02 Research           verified facts · 由緒 · 暦 · sources
   Practitioner           client questions · visit notes · stated views
          │
          ▼
   A07 Content Strategy Agent      theme approval
          │
          ▼
   ┌──────────────────┐
   │ X CONTENT AGENT  │   theme → angles → hooks → posts → claim classification
   │     (A10-X)      │
   └────────┬─────────┘
            ├────────────► A29 Fact-Check Agent
            │                      │
            ▼                      ▼
        A28 QA Agent  ◄────────────┘
   (compliance → factual → first-hand
    → editorial → SEO → technical)
            │
            ▼
     HUMAN APPROVAL
            │
            ▼
        Post to X       ← by a human. This agent holds no credentials
            │
            ▼
    A18 Analytics Agent
   bookmarks · profile clicks · follows · link clicks · bookings
            │
            ▼
     X CONTENT AGENT ──► A01 Strategy / A06 SEO ──► next batch
```

## Where it sits

| | |
| --- | --- |
| Agent ID | **A10-X** |
| Parent | A10 SNS Content Agent — [`../README.md`](../README.md) |
| Why a sub-agent | So Instagram / Threads / Ameba sub-agents can be added later without overlapping A10's scope |

## Files

| File | Purpose |
| --- | --- |
| [`positioning.md`](./positioning.md) | **Read first.** Why X is an authority channel. The basis rule. X post tiers. Anti-goals |
| [`mission.md`](./mission.md) | Mission, scope, non-goals |
| [`responsibilities.md`](./responsibilities.md) | Theme selection, angle expansion, composition, hooks, fact handling, batches, repurposing |
| [`categories.md`](./categories.md) | The four content categories, each with its required basis and failure modes |
| [`writing.md`](./writing.md) | Post structure, angles, style rules, threads, hashtags, hook patterns, CTA, voice |
| [`rules.md`](./rules.md) | Hard rules: positioning, compliance, factual, subjectivity, operating |
| [`inputs.md`](./inputs.md) | Data sources, phase availability, and the input gaps that exist today |
| [`outputs.md`](./outputs.md) | Artifacts, handoff contracts, batch file format, report format |
| [`workflow.md`](./workflow.md) | Production sequence, cadence, seasonal backward planning, escalation |
| [`kpi.md`](./kpi.md) | Three-tier KPI structure. Bookmarks and profile clicks at the top of Tier 2 |
| [`integrations.md`](./integrations.md) | X API, GA4, WordPress — read-only, and no posting path by design |
| `prompts/` | `_system.md` plus one prompt per task |
| `schemas/` | Four JSON Schemas plus a validator |
| `examples/` | Worked artifacts that validate against the schemas |

## Design decisions worth knowing

**1. The basis rule is the whole design.**
Every post must be traceable to `firsthand`, `practitioner_view`,
`verified_fact`, or `mechanism` — and `mechanism` alone is never enough for a
post about 運気. This is what separates
「財布を整理すると金運が上がります」 (forbidden) from an explanation someone saves.
It is enforced in `x_post.schema.json`: an empty `basis` array cannot be emitted.

**2. SEO's Tier D block transfers in substance, not in wording.**
`agents/seo/positioning.md` §5 bans 今日の運勢 / 無料占い / タロット意味 as
*keywords*. X is not a search channel, and 開運習慣 is this business's actual
subject matter. So the block here targets the **unsupported assertion**, not the
topic. See `positioning.md` §2 — this is the one place this directory
deliberately does not copy the SEO agent verbatim, and it says why.

**3. Bookmarks are the primary quality metric.**
Likes are reflexive; bookmarks are deliberate. Nobody bookmarks an assertion.
`bookmark_rate` is the only metric that detects whether the 理由 section did its
job, and it is what the agent reweights on. Impression-driven reweighting is
explicitly forbidden — it walks the account into Tier X-D, because unsupported
開運 assertions do reach well.

**4. `tier_a_post_ratio` is a P0 alert metric.**
The X analogue of SEO's `firsthand_content_ratio`. If it falls while impressions
rise, the account is drifting to commodity content. Treated as a failure, not a
tradeoff.

**5. Claim classification happens before writing, not after.**
`workflow.md` step 5 precedes step 7 deliberately. A well-written post resting on
an invented fact has to be thrown away, not edited.

**6. Fact-check turnaround is the binding constraint, not writing.**
Category A and D posts are bounded by verification throughput
(`positioning.md` §6). A 節句 post started three days before the date will miss.
A backlog of unverified drafts is not inventory — it is debt.

**7. One theme yields several posts.**
Angle expansion (`writing.md` §3) is what makes sustained cadence possible
without new research every day. It is also where Tier X-A comes from cheaply:
the 質問回答型 and 開運型 angles carry the practitioner's own judgment.

**8. The agent holds no posting credentials.**
Not a missing feature. A posted tweet is effectively irreversible — deleting it
does not unsee it. `integrations.md` lists the five conditions a posting
integration would have to satisfy before it is built.

## Schemas

| Schema | Unit | Consumer |
| --- | --- | --- |
| `x_post.schema.json` | One post | A28 QA → Human → X |
| `x_content_plan.schema.json` | One theme and its angles | Internal; A07 for review |
| `x_fact_check_request.schema.json` | Claims needing verification | A29 Fact-Check via A28 QA |
| `x_performance_record.schema.json` | Measured results | A18 Analytics ⇄ this agent |

`x_post` contains the twelve fields specified in the implementation brief —
`category`, `theme`, `target`, `angle`, `hook`, `body`, `cta`, `hashtags`,
`source_required`, `fact_check_required`, `risk_level`, `repurpose_candidates` —
unchanged, plus the fields needed to make the rules machine-checkable.

Validate with:

```sh
python3 fortune_labo/agents/sns/x/schemas/validate.py
```

The conditional rules are real gates, not documentation. A post with no basis, a
Category B post resting only on `mechanism`, a firsthand post with no
`visit_record_id`, and an `approved` post with unfilled placeholders or an
unresolved claim are all rejected by the schema.

## Implementation phasing

### Now (Phase 1) — no external API required

- [x] Specification (this directory)
- [x] Four schemas + validator + worked examples
- [ ] Theme pool seeded from client questions and the 節句・二十四節気 calendar
- [ ] First batch produced through the full production sequence
- [ ] Baseline `basis_coverage` and `tier_a_post_ratio`
- [ ] Fact-check request queue established with A28/A29
- [ ] 12-month seasonal theme calendar

**Phase 1 is fully operational.** X Content Agent is not blocked on API access.
Category and angle weighting is a documented hypothesis until Phase 2, and every
report must say so.

### Phase 2 — read APIs

- [ ] X post analytics (Analytics Agent fetches, caches to `data/`)
- [ ] GA4 with UTM tagging by post `id`
- [ ] Measured reweighting of categories, angles, hook patterns
- [ ] Tier 2 KPIs (`bookmark_rate`, `profile_click_rate`) actually measured

### Phase 3 — attribution

- [ ] X first-touch attribution to bookings
- [ ] Tier 1 KPIs measurable — **prioritisation is proxy-based until this lands,
      and every report must say so**

### Always requires human approval

- Any post going live
- Any first-person claim about the practitioner's actual practice
- Any post naming a specific shrine
- Any post at `risk_level: high`
- Any theme escalated as reach-vs-basis conflicting

## Consistency with `/AGENTS.md`

| Repository rule | How this directory enforces it |
| --- | --- |
| No autonomous publishing | `integrations.md`; this agent holds no X credentials by design |
| Do not invent business facts | `rules.md` §3 extends this to historical and cultural claims; `placeholders` ships unfilled |
| Use evidence for decisions | `basis` is a required, non-empty field on every post |
| Update hypotheses, not evidence | `x_performance_record.interpretation.hypothesis_update`; mandatory ledger in the monthly report |
| Small reviewable changes | Every artifact is a discrete schema-conforming unit |
| Secrets out of Git | `integrations.md` — no credentials held here |
| Dry-run where practical | Any future posting integration requires preview mode (`integrations.md`) |

## Known gaps

Recorded so nobody mistakes absence for a decision:

- **A07 and A09 do not exist.** X Content Agent currently self-serves theme
  approval, with a human standing in. That is an overreach and is scoped in
  `workflow.md` §Interim operation
- **No visit records exist in the repository.** Tier X-A firsthand posts cannot
  be produced at all until they do
- **No standard disclaimer text exists**, although `agents/seo/rules.md` §3.4
  requires one. A proposal sits unapproved in `content/sns/README.md` §3
- **Business facts are unset** — practitioner name, service, booking URL, region,
  divination method. Posts ship with `{{placeholders}}` and the `booking` CTA
  cannot be used until they are filled
