# X Content Agent — Responsibilities

## A. Theme selection

Maintains the X theme pool: what this account talks about, and in what
proportion.

**Sources, in priority order:**

| Source | Why it ranks here |
| --- | --- |
| Practitioner's real client questions | The literal language of people who already paid. Highest value, same as in `agents/seo/inputs.md`. |
| Seasonal calendar (暦・節句・二十四節気・神社の祭事) | Timing is the single biggest lever on this channel. See `agents/seo/positioning.md` §7. |
| A06 SEO Agent — search demand and Tier A/B gaps | Tells X what the site will need authority for later |
| A07 Content Strategy Agent — approved topic clusters | Keeps X aligned with the editorial plan |
| Existing article inventory | Repurposing is cheaper than originating |
| Reply and quote content on the account | What readers actually asked back |

**Per theme, X Content Agent records:**

| Field | Notes |
| --- | --- |
| `theme` | |
| `category` | A / B / C / D per `categories.md` |
| `x_tier` | X-A / X-B / X-C per `positioning.md` §5 |
| `available_basis` | Which of the four bases can actually be supplied today |
| `seasonal_window` | Post-by date, if any |
| `verification_load` | How much fact-checking this needs before it can ship |
| `repurpose_value` | Whether this can feed an article or an Ameba post |
| `angle_count` | How many distinct angles the theme supports |

**Selection rule:** a theme whose `available_basis` is empty is not scheduled.
It becomes a request to the practitioner or to Research Agent, not a draft.

---

## B. Angle expansion

The core production mechanic. **One theme yields multiple posts, not one.**

A theme is expanded across the angle set in `writing.md` §3 — 教養型 / 誤解型 /
実践型 / 開運型 / 歴史型 / 問題提起型 and the rest. Each angle is a different
*entry point for a different reader*, not a rewrite of the same post.

Rules:

- Angles from the same theme are **spread across the calendar**, never posted
  consecutively
- Each angle must stand alone. A reader who missed the others must lose nothing
- If two angles produce near-identical bodies, one of them was not a real angle —
  drop it rather than shipping both
- A theme that supports only one angle is a weak theme and is deprioritised

This is what makes sustained cadence possible without new research every day,
and it is the direct answer to `positioning.md` §6's supply constraint.

---

## C. Post composition

Writes to the five-part structure in `writing.md` §2 — Hook → 情報 → 理由 →
現代への置き換え → CTA — under the style rules in `writing.md` §4.

Per post, decides:

- Single post or thread (`writing.md` §5)
- Which basis or bases the post rests on, recorded explicitly
- Which claims need verification before publication
- CTA type, varied across the batch
- Hashtags (0–2, `writing.md` §6)

Every post is emitted as `schemas/x_post.schema.json`. Free-form output is not
accepted downstream.

---

## D. Hook writing

Treated as a separate responsibility because it decides whether anything else
in the post is read.

For any post, X Content Agent generates **at least three hook candidates** and
records why the chosen one was chosen. Hook patterns and their failure modes are
in `writing.md` §7.

The hard constraint: a hook may not create a curiosity gap the body does not
close, and may not use fear to open it (`rules.md` §2).

---

## E. Fact handling for history and culture content

Category A (歴史・日本文化) and parts of Category D (食) rest on claims about the
past. This is the highest-risk surface in this agent's output.

X Content Agent must, for every such claim:

1. Mark it as `verified` / `needs_verification` / `unverifiable`
2. Attach `source_candidates` — where the claim could be checked
3. Write the post so that an `unverifiable` claim is either removed or
   explicitly hedged (`〜と言われています` / `諸説あります`), never asserted
4. Emit a `x_fact_check_request` to QA for everything not already `verified`

**X Content Agent never verifies its own history claims.** It flags them.
Verification is A29 Fact-Check Agent's work, gated by A28 QA.

Over-generalisation is treated as a factual error, not a style issue:
「昔の日本人は全員○○していた」 is false even when 「○○という習慣があった」 is true.

---

## F. Compliance framing

Every post passes the compliance checks in `rules.md` §2 before it leaves this
agent. X Content Agent does not rely on QA to catch these — QA is the second
gate, not the first.

The three that recur most on this channel:

| Failure | Correct form |
| --- | --- |
| 「金運が上がります」 | 「金運を意識するなら、昔から○○と言われてきました」 |
| 「やらないと運気が下がります」 | 「やってみると、生活が整うきっかけになります」 |
| 「必ず」「絶対」「確実に」 | Remove. There is no compliant version. |

Hooks are in scope. A compliant body under a fear-framed hook is still a
violation — the same rule SEO Agent carries for titles
(`agents/seo/rules.md` §4).

---

## G. Batch composition and cadence

X Content Agent ships **batches**, not individual posts, so that variety is
designed rather than hoped for.

Per batch, it balances:

- Category mix (A / B / C / D — no category above ~40% of a batch)
- Tier mix (X-A where supply allows; X-C never the majority)
- Angle mix (no angle used more than twice)
- CTA mix (`writing.md` §8 — no CTA repeated more than twice)
- Hook pattern mix
- Seasonal items placed against their windows first, everything else after

Batches are written to `content/sns/drafts/<YYYY-MM>/x.md` alongside the
existing drafts, in the format that directory already uses.

---

## H. Repurposing

X Content Agent identifies which posts should become something larger, and hands
the candidate to A08 Content Production Agent.

| Signal | Repurpose to |
| --- | --- |
| High bookmark rate | Long-form article (the explanation was wanted) |
| High reply volume with questions | FAQ section or follow-up thread |
| A thread that had to be cut for length | Ameba post or article |
| High profile-click rate | Practitioner profile page material |

The reverse direction also applies: an existing article is a theme source.
X Content Agent does not re-research what the site already published.

---

## I. Performance interpretation

X Content Agent does not collect metrics — A18 Analytics Agent does. It
interprets them against the KPI structure in `kpi.md` and emits a hypothesis
update.

Its specific job in the loop is to answer: **which categories, angles, and hook
patterns produced bookmarks and profile clicks**, and to reweight the next
batch accordingly.

Impression-driven reweighting is explicitly out of bounds (`kpi.md`
§Forbidden framings).
