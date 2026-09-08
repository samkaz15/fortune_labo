# X Content Agent — Workflow

## Core loop

The pipeline requested in the implementation brief, drawn against the agents
that actually exist.

```
A06 SEO Agent ────── search demand, Tier A/B gaps, seasonal calendar
A02 Research ─────── verified facts, 由緒, 暦, sources
Practitioner ─────── client questions, visit notes, stated views
        │
        ▼
A07 Content Strategy Agent ── approves themes and clusters
        │
        ▼
   X CONTENT AGENT (A10-X)
        │
        ├─ theme selection      ──► x_content_plan
        ├─ angle expansion      ──► 1 theme → N posts
        ├─ hook writing         ──► ≥3 candidates each
        ├─ post composition     ──► x_post
        └─ claim classification ──► x_fact_check_request
                 │
                 ├──────────────► A29 Fact-Check Agent
                 │                        │
                 │                verified / refuted / unverifiable
                 │                        │
                 ▼                        ▼
            A28 QA Agent  ◄───────────────┘
     (compliance → factual → first-hand
      → editorial → SEO → technical)
                 │
                 ▼
        HUMAN APPROVAL   ◄── mandatory, per /AGENTS.md
                 │
                 ▼
            Post to X    ◄── by a human. This agent holds no credentials
                 │
                 ▼
        A18 Analytics Agent
   impressions / engagement / bookmarks /
   profile clicks / follows / link clicks / bookings
                 │
                 ▼
        X CONTENT AGENT
   (performance interpretation by category,
    angle, hook pattern, CTA)
                 │
                 ▼
   Hypothesis update ──► A01 Strategy / A06 SEO ──► next batch
```

**No path bypasses human approval.**
**No path allows AI to originate first-hand experience or history.**

---

## Interim operation (current state)

A07 Content Strategy Agent and A09 SNS Strategy Agent are **defined in
`docs/agents/AGENT-INDEX.md` but not implemented**. Until they are:

| Normally | Interim |
| --- | --- |
| A07 approves the theme pool | X Content Agent proposes the pool; **the human approves it** as a batch-level decision |
| A09 sets cadence and audience | Assumed from `positioning.md`; recorded as a hypothesis, not a decision |
| A29 verifies claims via A28 | Fact-check requests are emitted and **held**; posts stay `fact_check_pending` until a human resolves them |

This is an overreach by X Content Agent and is recorded as such. It ends when
A07 and A09 exist. It does **not** extend to publishing, which stays human-gated
in every case.

---

## Production sequence for one batch

```
1. Window check        What seasonal windows open in the next 6 weeks?
                       Anything past its publish-by date is already lost.

2. Basis inventory     What firsthand / practitioner_view material exists today?
                       Empty inventory caps the batch at Tier X-B and below.

3. Theme selection     Draw from the approved pool, weighted by:
                       seasonal urgency > client questions > SEO gaps > clusters

4. Angle expansion     Each theme → the angles it genuinely supports.
                       Drop angles that would duplicate another post's body.

5. Claim extraction    Before writing: list every factual claim the post will
                       make. Classify each. This precedes composition — writing
                       first and checking later produces posts that cannot be
                       saved without a rewrite.

6. Fact-check request  Emit x_fact_check_request for everything not `verified`.

7. Composition         Hook candidates → body → 理由 → 現代への置き換え → CTA.
                       Character count. Placeholder marking.

8. Self-compliance     Run rules.md §2 against every post, hooks included.
                       This agent does not delegate this to QA.

9. Batch balance       Category ≤40%, angle ≤2, hook pattern ≤2, CTA type ≤2,
                       booking CTA ≤1, ~half with no CTA.

10. Emit               x_post JSON + generated markdown batch file.

11. Handoff            → QA. Nothing in the batch ships until every post in it
                       is individually resolved. A blocked post does not block
                       the batch; it moves to the next one.
```

Step 5 before step 7 is deliberate. It is the step that prevents a well-written
post resting on an invented fact.

---

## Cadence

### Per batch (default: monthly, ~12–20 posts)

The unit of work. Follows the production sequence above.

### Weekly

- Seasonal window check for the next 6 weeks
- Resolve returned fact-checks; promote or drop `fact_check_pending` posts
- Review the prior week's posts against Tier 2 KPIs
- Capture any new client question worth becoming a theme
- Emit any P0 escalation (compliance or factual error found in a live post)

### Monthly

- Full Tier 1 / 2 / 3 report (`outputs.md` §Report format)
- Category, angle, hook-pattern and CTA performance breakdown
- Theme pool review: promote, demote, retire
- Basis-coverage audit — **what share of the month's posts were Tier X-A?**
  A falling share is the X-channel equivalent of `firsthand_content_ratio`
  declining, and is treated the same way: P0 (`kpi.md`)
- Verification backlog check
- Next batch produced
- **Hypothesis ledger update**

### Quarterly

- Review with A09 SNS Strategy / A01 Strategy Agent
- Category mix recalibration against measured bookmark rate
- Repurposing review — which posts should have become articles
- Regulatory review: has permissible-claim guidance changed?
- Prune: which themes never produced anything worth saving

### Annual

- Seasonal theme calendar rebuild for the next 12 months
- Account positioning review against `positioning.md`
- If any annual-forecast post was published, the **prior-year public review**
  obligation applies here too (`agents/seo/rules.md` §3.3)

---

## Seasonal backward planning

Timing beats quality on this channel more often than anyone wants to admit.
X Content Agent plans backward from the window, the same way SEO Agent does.

```
Seasonal window                e.g. 重陽の節句 = 9月9日
        ↑ 0–3 days
Post                           9月6日〜9日（当日でも遅くない、当日以降は無価値）
        ↑ 3 days
Human approval                 9月3日
        ↑ 3 days
QA (compliance → factual)      8月31日
        ↑ 5–10 days
Fact-check returned            8月25日   ← the long pole for Category A and D
        ↑ 2 days
Fact-check request issued      8月23日
        ↑ 2 days
Draft composed                 8月21日
        ↑
Theme selected                 8月上旬（batch planning）
```

**Fact-check turnaround is the binding constraint**, not writing. A 節句 post
started three days before the date will miss, because verification cannot be
compressed. This is why claim extraction is step 5, not step 9.

Windows this account plans against (from `agents/seo/positioning.md` §7 plus the
節句・二十四節気 calendar):

| Window | Category | Lead time needed |
| --- | --- | --- |
| 二十四節気（24回/年） | A / D | 2 weeks |
| 五節句（1/7・3/3・5/5・7/7・9/9） | A / D | 3 weeks |
| 節分・立春 | A / C | 4 weeks |
| 七五三（9–11月） | A / C | 4 weeks |
| 大祓（6月・12月） | A | 4 weeks |
| 初詣・年始 | A / C | 6 weeks |
| 年間見通し | C | 6 weeks + review obligation |

---

## Escalation triggers

See `rules.md` §6 for the full table. The three that fire most often:

| Trigger | Route | Urgency |
| --- | --- | --- |
| Compliance or factual error in a **published** post | Human | **Immediate. Request deletion, draft correction** |
| Verification backlog exceeds one batch | Human | Cadence is at risk |
| A theme is strategically wanted but has no available basis | A07 (interim: human) | Before the batch is drafted |
