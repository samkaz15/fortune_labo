# X Content Agent — KPI Structure

## Design principle

The default X metric stack puts impressions and follower count at the top.
**That is wrong for this business** (`positioning.md` §1). Reach sits in the
lowest tier here — a diagnostic, never a goal.

The brief states this directly: **単純に「バズったか」だけでは評価しない。**
This file is that instruction made structural.

The tiering mirrors `agents/seo/kpi.md` so that both channels report in the
same shape and Strategy Agent can compare them.

---

## KGI

> **X-sourced booked readings per month.**

A reading booked by a visitor whose first session came from X.
Secondary KGI: **X-sourced revenue**.

---

## Tier 1 — Business outcome (the only tier that defines success)

| KPI | Definition | Phase |
| --- | --- | --- |
| `x_bookings` | Bookings attributed to an X first touch | 3 |
| `x_revenue` | Revenue from those bookings | 3 |
| `x_site_sessions` | Sessions on the site from X | 2 |
| `x_service_page_views` | Views of the 占いサービス / booking page from X | 2 |
| `x_list_signups` | LINE / email registrations from X | 2 |

**If Tier 1 is flat, no Tier 2 or Tier 3 improvement counts as success.**

---

## Tier 2 — Authority and saveability (leading indicators)

The tier this agent is actually steered by. These four are the metrics the brief
singles out as 重要指標.

| KPI | Definition | Target direction | Why it is here |
| --- | --- | --- | --- |
| **`bookmark_rate`** | ブックマーク / impressions | **↑ — primary quality metric** | Nobody bookmarks an assertion. Bookmarks detect explanatory depth (`positioning.md` §4) |
| **`profile_click_rate`** | プロフィールクリック / impressions | **↑** | The moment the reader asks "who wrote this?". The whole authority model runs through it |
| **`follows_per_post`** | フォロー獲得 / post | ↑ | Sustained interest, not a single hit |
| **`link_click_rate`** | Webサイト遷移 / impressions | ↑ | Intent to go deeper |

Supporting Tier 2 metrics, specific to this implementation:

| KPI | Definition | Target |
| --- | --- | --- |
| `basis_coverage` | Posts with ≥1 basis / posts published | **= 1.0. Any value below 1.0 is a rule violation, not a metric miss** |
| `tier_a_post_ratio` | Tier X-A posts / posts published | **↑, never falling** |
| `verification_hit_rate` | Claims returned `verified` / claims submitted | ↑ — a falling rate means themes are being chosen carelessly |
| `cadence_adherence` | Posts published / posts planned | **≥ 0.9** |
| `seasonal_hit_rate` | Seasonal posts published inside their window / seasonal posts planned | **= 1.0** |
| `correction_count` | Corrections issued for published errors | **= 0** |

`tier_a_post_ratio` is the X-channel analogue of SEO's
`firsthand_content_ratio`. **If it falls while impressions rise, the account is
drifting toward commodity content.** That is a P0 alert, treated as a failure and
not as a tradeoff — the same rule as `agents/seo/kpi.md`.

`basis_coverage` below 1.0 is not a performance problem. It means a post shipped
in breach of `rules.md` §1.1 and the pipeline failed.

---

## Tier 3 — Reach and engagement (diagnostics only)

Standard X metrics. Used to explain Tier 1 and Tier 2 movement.
**Never reported as achievements on their own.**

| KPI | Source |
| --- | --- |
| `impressions` | X analytics |
| `engagement_rate` | X analytics |
| `likes` | X analytics |
| `reposts` | X analytics |
| `replies` | X analytics |
| `follower_count` | X analytics |
| `post_count` | Internal |

---

## The ratio that matters most

```
bookmark_rate ÷ like_rate
```

Likes are cheap and reflexive. Bookmarks are deliberate — the reader intends to
come back. A post with many likes and no bookmarks was **agreeable**.
A post with few likes and many bookmarks was **useful**.

This account is trying to be useful. When the two diverge, follow bookmarks.

Watch the same way for:

```
profile_click_rate ÷ engagement_rate
```

High engagement with low profile clicks means the post performed as content but
did nothing for the practitioner. That is the channel-level version of
`positioning.md` §1's wrong model.

---

## Forbidden framings

X Content Agent must not report, and Strategy Agent must not accept:

- 「バズった」 as a result
- Impressions growth without a Tier 1 or Tier 2 movement attached
- Follower growth as a standalone achievement
- Engagement rate improvement produced by dropping explanation for brevity
- Post-count growth as progress
- A single high-performing post presented as channel performance

Every X report opens with Tier 1, then Tier 2, then Tier 3. Never the reverse.

---

## Diagnostic matrix

Observed pattern → likely cause → owning agent. Used by the monthly review.

| Pattern | Likely cause | Owner |
| --- | --- | --- |
| Impressions ↑, bookmarks flat | Hook works, 理由 is thin or missing | X Content Agent |
| Bookmarks ↑, profile clicks flat | Useful content, but the author is invisible in it | X Content Agent |
| Profile clicks ↑, link clicks flat | Profile copy or link placement | A14 LP / A09 SNS Strategy |
| Link clicks ↑, sessions flat | Landing page mismatch with post intent | A15 CRO |
| Sessions ↑, bookings flat | Wrong audience, or booking friction | A15 CRO / A01 Strategy |
| Impressions ↑, `tier_a_post_ratio` ↓ | **Moat erosion — P0** | X Content Agent → A01 Strategy |
| Replies ↑ with personal consultation requests | Content is landing, but reply handling is unowned | A09 + human |
| `verification_hit_rate` ↓ | Themes chosen without checking sourceability | X Content Agent (own failure) |
| Seasonal post published late | Fact-check lead time underestimated | X Content Agent (own failure) |
| `correction_count` > 0 | A factual or compliance gate failed | X Content Agent + A28 QA |

---

## Phase availability

| Phase | Measurable | Consequence |
| --- | --- | --- |
| **1 — Now** | `basis_coverage`, `tier_a_post_ratio`, `cadence_adherence`, `seasonal_hit_rate`, `verification_hit_rate`, `correction_count` — all internal | Tier 2 process metrics work from day one. Category weighting stays a **documented hypothesis** |
| **2** | All Tier 3, plus bookmark / profile click / follow / link click | Measured reweighting becomes possible |
| **3** | Tier 1 booking attribution | True prioritisation by revenue |

Until Phase 3, **every X report must state that prioritisation is proxy-based** —
the same disclosure `agents/seo/README.md` requires.
