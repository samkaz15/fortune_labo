# SEO Agent — Workflow

## Core loop

```
Research Agent ─── market, competitor, demand data
        │
        ▼
   SEO Agent ───── keyword discovery + classification (Tier A/B/C, D excluded)
        │
        ├──────────► Visit Plan ──────► HUMAN VISIT ──► visit notes + photos
        │                                                      │
        ▼                                                      ▼
   SEO Strategy ◄──────────────────────────────────── raw material exists
        │
        ├──► Content Brief ────► Content Agent ──► draft
        ├──► Technical Issue ──► Codex ──────────► PR
        └──► Link Instruction ─► Codex ──────────► PR
                                     │
                                     ▼
                                 QA Agent
                        (compliance → factual → first-hand
                         → editorial → SEO → technical)
                                     │
                                     ▼
                            HUMAN APPROVAL  ◄── mandatory, per /AGENTS.md
                                     │
                                     ▼
                                 Publish
                                     │
                                     ▼
                          GSC / GA4 / booking data
                                     │
                                     ▼
                            Analytics Agent
                                     │
                                     ▼
                               SEO Agent
                          (performance analysis)
                                     │
                                     ▼
                        Hypothesis update ──► next cycle
```

**No path bypasses human approval.** No path allows AI to originate first-hand
shrine content — the visit branch is a hard dependency for Tier A.

---

## Cadence

### Daily (automated, Phase 2+)

Alert-only. No strategy work.

- Index coverage errors, new 404s
- Sudden position drops (> 5 places on a Tier A/B page)
- Site availability, crawl errors
- Broken internal links

Emits P0 opportunities only. Silence is the normal state.

### Weekly (analysis)

- Tier 1 movement vs prior week
- Query-level winners and losers
- Impressions-up / clicks-flat detection → title & meta review
- New content performance (first 14 days)
- Competitor new publications on Tier A/B
- **Seasonal calendar check: what must be visited or published in the next 6 weeks**
- Emit and re-prioritise opportunities

### Monthly (strategy)

- Full Tier 1 / 2 / 3 report
- `firsthand_content_ratio` audit — **moat check**
- Branded search trend — **authority check**
- Keyword register review: promote, demote, retire; cannibalisation sweep
- Internal link graph audit: orphans, weak high-value pages, booking-page inbound count
- Technical audit sweep
- Competitor SERP share on Tier A/B
- Visit plan for the next 90 days
- **Hypothesis ledger update**

### Quarterly (direction)

- Strategy review with Strategy Agent
- Keyword tier reclassification against market shift
- Content pruning: thin, stale, or off-positioning pages → improve / consolidate / remove
- Architecture review
- Prioritisation formula recalibration against realised booking data
- Regulatory review (has permissible-claim guidance changed?)

### Annual (flagship)

- Annual outlook publication — **publish by late October** for the following year
- **Prior-year forecast public review** (hits and misses) — mandatory, `rules.md` §3.3
- Seasonal calendar rebuild
- Full site architecture and moat assessment

---

## Seasonal backward planning

Seasonal windows are non-negotiable deadlines. SEO Agent plans backward:

```
Target window opens          e.g. 初詣 demand builds from early December
        ↑ 4 weeks
Publish                      early November
        ↑ 2 weeks
QA + human approval          late October
        ↑ 2 weeks
Draft (Content Agent)        mid October
        ↑ 1 week
Brief issued (SEO Agent)     early October
        ↑ 2–4 weeks
VISIT COMPLETED              September
        ↑
Visit plan issued            August
```

**A visit plan issued in November for 初詣 has already failed.** SEO Agent's
weekly seasonal check exists to prevent exactly this.

---

## Escalation triggers

Immediate escalation to Strategy Agent / human, outside cadence:

| Trigger | Route |
| --- | --- |
| `moat_alignment: conflicting` on any opportunity | Strategy |
| `firsthand_content_ratio` declining | Strategy — P0 |
| Recommended volume exceeds practitioner capacity | Human |
| Seasonal deadline at risk | Human |
| Suspected manual action or major algorithmic drop | Strategy + human |
| Compliance risk found in published content | **Human immediately; request unpublish** |
| Shrine photo permission unverified on a live page | Human immediately |
