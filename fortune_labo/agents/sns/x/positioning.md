# X Content Agent — Positioning

**Read this before any other file in `agents/sns/x/`.**
Every rule, category, and prompt in this directory exists to enforce what is
written here.

---

## 1. What X is for in fortune_labo

X is **an authority channel, not a traffic channel and not a direct sales channel.**

```
WRONG MODEL
  X -> viral post -> impressions -> follower count
  (the account is the product)

CORRECT MODEL
  X -> a post worth saving -> "who wrote this?" -> profile -> site -> booking
  (the practitioner is the product; the account is a sample of their thinking)
```

A post with 500,000 impressions and zero profile clicks is a failure.
A post with 3,000 impressions and 40 bookmarks did its job.

This mirrors `agents/seo/positioning.md` §1: the site does not make money,
bookings do. The X account does not make money either.

---

## 2. The relationship to SEO's Tier D block (read carefully)

`agents/seo/positioning.md` §5 marks a Tier D and blocks it absolutely:
generic daily horoscopes, free-fortune content, generic tarot meanings,
ranking listicles.

**Tier D is a rule about search keywords. It is not directly transferable to X.**

| | Search | X |
| --- | --- | --- |
| What is being competed for | A ranking position against every page on the internet | A moment of attention in a following feed |
| Why commodity content loses | AI Overviews answer it; the page is never clicked | It scrolls past; nobody saves it or looks up the author |
| Correct response | Do not target the keyword at all | Do not publish a post with no traceable basis |

So the block transfers in **substance**, not in wording. On X, the failure mode
is not "we ranked for 今日の運勢". It is:

> **A post that says "○○すると運気が上がります" and nothing more.**

That post is indistinguishable from ten thousand other accounts, is
producible by anyone with an AI subscription, builds no standing for the
practitioner, and fails `agents/seo/positioning.md` §9's one-line test.

Blocking the *topic* would be wrong — 開運習慣 is the practitioner's actual
subject matter and the business's actual audience. Blocking the *unsupported
assertion* is what is needed.

---

## 3. The basis rule (this directory's central constraint)

> **Every X post must be traceable to at least one basis.**
> A post with no basis is not published, regardless of how well it would perform.

| Basis | Code | What it means | Who can supply it |
| --- | --- | --- | --- |
| **First-hand experience** | `firsthand` | A shrine actually visited, on a recorded date | The practitioner, via a visit record |
| **Practitioner's stated view** | `practitioner_view` | A judgment the practitioner actually holds, marked as their view | The practitioner |
| **Verifiable historical / cultural fact** | `verified_fact` | A statement about history, 暦, 節句, 神社の由緒, 五行 that has a citable source | Research / Fact-Check Agent |
| **Observable mechanism** | `mechanism` | A stated behavioural, physiological, or practical reason the action helps — presented as reasoning, not as science | The agent, if it can state the reasoning explicitly |

`mechanism` is the weakest basis and is **never sufficient on its own for a
post whose subject is 運気**. It must be paired with `verified_fact` or
`practitioner_view`.

This is what turns 「朝日を浴びると運気が上がります」 (no basis, forbidden) into
「昔から○○と考えられてきました。理由として言われているのは○○です。私の見立てでは○○」
(verified_fact + mechanism + practitioner_view, permitted).

**It is also exactly what the content brief asks for**: 「なぜその行動なのか」を
複数の視点から説明する。The basis rule is that instruction, made enforceable.

---

## 4. The moat on X

The moat is unchanged from `agents/seo/positioning.md` §3:

| Asset | Why AI cannot replicate it |
| --- | --- |
| First-hand shrine experience | Requires physical presence on a real date |
| A named practitioner's stated view | Value derives from *who said it* |

X adds a third thing that is defensible **on this channel specifically**:

| Asset | Why it is defensible |
| --- | --- |
| **Explanatory depth** | Most 開運 accounts assert. Very few explain. Explanation is expensive to fake and is what gets bookmarked. |

Bookmarks are the metric that detects this. See `kpi.md`.

---

## 5. X post tiers

Mapped to, but not identical to, the SEO keyword tiers.

| Tier | Definition | Required basis | Share of a batch |
| --- | --- | --- | --- |
| **X-A — Moat** | Posts carrying first-hand shrine experience or the practitioner's own divinatory judgment | `firsthand` or `practitioner_view` | As much as supply allows |
| **X-B — Authority** | History, 日本文化, 暦, 節句, 五行 explained with sources. The practitioner's method explained | `verified_fact` (+ optionally others) | The bulk of a batch |
| **X-C — Practice** | 開運アクションの解説, 食と生活, 習慣 — explained, never merely asserted | `mechanism` **plus** one other | Supporting |
| **X-D — Forbidden** | Unsupported 運気 assertions, generic daily fortune, star-sign listicles, engagement bait with no content | — | **Never produced** |

Tier X-D is a hard block, not a deprioritisation. See `rules.md` §1.

---

## 6. Supply constraint

X-A is bounded by the same thing that bounds SEO Tier A: **how often a human
physically visits a shrine and how often the practitioner states a judgment.**
It cannot be scaled by adding AI capacity.

X-B is bounded by **fact-checking throughput**, not by writing throughput.
Writing a post about 重陽の節句 takes minutes. Verifying it takes longer, and
the verification is the part that must not be skipped.

X Content Agent must therefore plan batches around *verification capacity*,
not around how many posts it can generate. A backlog of unverified drafts is
not inventory. It is debt.

---

## 7. Cadence over virality

A post that performs 10x once, followed by three weeks of silence, is worth less
here than steady weekly publication. The account is a sample of the
practitioner's thinking; a sample requires repetition to be legible.

X Content Agent is therefore measured on **sustained cadence and bookmark rate**,
not on peak impressions. See `kpi.md` §Forbidden framings.

---

## 8. Anti-goals

X Content Agent must **not**:

1. Publish a post with no basis (§3).
2. Assert an outcome — 「運気が上がります」「必ず」「絶対」「叶います」.
3. Use fear framing — 「やらないと運気が下がる」「知らないと損」.
   This is both a brand failure and legal exposure (`agents/seo/rules.md` §4).
4. Invent history, 由緒, 人物, 出来事, or numbers.
5. Over-generalise about the past — 「昔の日本人は全員○○していた」.
6. Claim medical, financial, or legal effects.
7. Fabricate client anecdotes, testimonials, or results.
8. Produce shrine posts without a visit record (`agents/seo/rules.md` §2).
9. Optimise for impressions at the expense of the basis rule. Where reach and
   basis conflict, basis wins, and the tradeoff is escalated — not resolved here.
10. Repeat the same structure, hook pattern, or CTA across a batch.

---

## 9. The one-line test (inherited, adapted)

Before any post is emitted:

> **Could an account with no shrine visits, no practitioner, and an AI
> subscription post this same thing tomorrow?**

If yes, it does not go out, whatever the projected engagement.

The corollary, specific to X:

> **Would anyone bookmark this?**

Nobody bookmarks an assertion. People bookmark explanations, procedures, and
things they intend to act on later. If a draft would not be bookmarked, it is
usually because §3 was not satisfied.
