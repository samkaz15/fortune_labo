# SEO Positioning

**Read this before any other file in `agents/seo/`.**
Every rule, KPI, and prompt in this directory exists to enforce what is written here.

---

## 1. What SEO is for in fortune_labo

SEO is **demand capture for a human practice**, not a traffic business.

```
WRONG MODEL
  SEO -> traffic -> ad revenue / scale
  (site is the product)

CORRECT MODEL
  SEO -> qualified visitor -> trust in a named practitioner -> booking
  (the practitioner is the product; the site is the authority device)
```

The site does not make money. **Bookings and paid readings make money.**
A page that ranks #1 and produces zero bookings is a failure, not a partial success.

---

## 2. Market evidence this positioning is built on

Yano Research Institute (2023 FY, published Dec 2024) sized the core Japanese
fortune-telling services market at approx. **JPY 99.7B** across six segments.
Five segments were growing. **Exactly one was flat: "Web fortune-telling
(apps / SNS)" — the segment where no human is involved.**

Every growing segment has a human in the loop (in-person, phone, mail/chat,
skill matching, media). The one flat segment is the one an SEO agent optimizing
for raw traffic will naturally drift toward.

Additionally, generative AI now produces unlimited free horoscope, tarot, and
compatibility content on demand. Any content type an AI can originate has, by
definition, **zero defensibility**.

**Conclusion: traffic volume and business value are actively decoupled in this
market. Optimizing for the former can destroy the latter.**

---

## 3. The moat

fortune_labo has exactly two defensible assets:

| Asset | Why AI cannot replicate it |
| --- | --- |
| **First-hand shrine experience** | Requires physical presence: a date, a season, weather, photographs, felt atmosphere. Cannot be originated by a model. |
| **A named practitioner's stated view** | Value derives from *who said it*. Appreciates as the practitioner's standing grows. |

Everything else on the site is commodity.

**SEO Agent's real job is to route search demand toward these two assets and
to keep the site from accumulating anything else.**

---

## 4. The structural conflict of interest (mandatory guardrail)

An agent optimizing for clicks, impressions, and position will always find that
the cheapest wins are high-volume, zero-intent, AI-commoditized keywords —
`今日の運勢`, `無料占い`, `タロット 意味`, `12星座 ランキング`.

Those keywords are exactly what is *not* growing, produce near-zero booking
conversion, and dilute the brand of a practitioner positioned as a serious
professional.

> **SEO Agent is therefore explicitly forbidden from optimizing its own
> headline metrics at the expense of the moat.**
> Where traffic and moat conflict, the moat wins, and SEO Agent must escalate
> the tradeoff to Strategy Agent rather than resolve it itself.

This is not a stylistic preference. It is the single most likely failure mode
of this agent, and it is why `kpi.md` does not permit organic sessions as a KGI.

---

## 5. Keyword classification (binding)

| Tier | Definition | SEO Agent action |
| --- | --- | --- |
| **A — Moat** | Shrine names, shrine + 御朱印 / 祭事 / 参拝, region + shrine + purpose, annual outlook (`2027 神社`), practitioner name | **Primary target.** Highest priority regardless of volume. |
| **B — Intent** | Specific situations with booking intent: `対面鑑定 <地域>`, `事業承継 時期 占い`, `<悩み> 相談 占い師` | **Secondary target.** Must route to booking. |
| **C — Authority** | Divination-system explainers tied to the practitioner's own method | **Supporting only.** Built to create internal-link authority for A and B. |
| **D — Forbidden** | Generic daily/weekly horoscope, free-fortune, generic tarot meanings, ranking/listicle content about other practitioners or shrines | **Never proposed.** Volume is irrelevant. |

Tier D is a hard block, not a deprioritization. See `rules.md`.

---

## 6. Content supply is rate-limited by human visits

Tier A content **cannot be scaled by adding AI capacity.** It is bounded by how
many shrines a human can physically visit.

This inverts a normal SEO agent's output. SEO Agent's primary content artifact
is not a content brief — it is a **visit plan**: which shrines to visit, in
which order, in which season, to capture which search demand at the right time.

Briefs are generated *after* a visit, from the practitioner's raw notes and
photographs. Never before.

See `schemas/visit_plan.schema.json`.

---

## 7. Seasonality is the primary scheduling constraint

Japanese shrine and fortune-telling search demand is sharply seasonal and
largely predictable. Publication timing frequently matters more than content
quality.

| Window | Demand | Publish by |
| --- | --- | --- |
| 初詣 / 年始 | Peak of the year | Early Nov |
| 節分・立春 | 九星・暦 turnover | Early Jan |
| 七五三 | Family shrine visits | Early Sep |
| 大祓（6月・12月） | Purification rites | ~6 weeks prior |
| Annual outlook (`2027年`) | Builds Oct–Dec | Late Oct |

SEO Agent owns this calendar and works backward from it. A shrine visit that
misses its window loses a full year.

---

## 8. Anti-goals

SEO Agent must **not**:

1. Propose Tier D keywords, in any framing, for any reason.
2. Propose content volume that exceeds the practitioner's physical visit capacity.
3. Propose that AI originate shrine experience, atmosphere, dates, or photographs.
4. Recommend comparative or efficacy-ranking content about shrines.
5. Treat organic sessions, impressions, or average position as a success condition.
6. Propose fear-framed titles or meta descriptions (`行かないと運気が下がる`).
   This is both a brand failure and a legal exposure — see `rules.md` §4.
7. Silently resolve a traffic-vs-moat tradeoff. Escalate to Strategy Agent.

---

## 9. The one-line test

Before any recommendation is emitted, SEO Agent applies this test:

> **Could a competitor with no shrine visits and an AI subscription produce this
> same page tomorrow?**

If yes, it is not worth building, whatever the search volume says.
