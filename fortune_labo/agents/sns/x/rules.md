# X Content Agent — Rules

Violations of §1–§4 are **blocking**. QA Agent rejects any post that breaches
them, regardless of projected engagement.

These rules extend, and never relax, `/AGENTS.md` and `agents/seo/rules.md`.

---

## 1. Positioning rules

1. **Every post must carry at least one basis** (`positioning.md` §3):
   `firsthand` / `practitioner_view` / `verified_fact` / `mechanism`.
   A post with `basis: []` is not emitted.
2. `mechanism` alone is never sufficient for a post whose subject is 運気.
3. Tier X-D posts are never produced, drafted, or scheduled:
   - Unsupported 運気 assertions (「○○すると運気が上がります」 and nothing else)
   - 今日の運勢 / 今週の運勢 / 星座別ランキング / タロットの意味一覧
   - Engagement bait with no informational content
   - 「効く神社ランキング」「最強パワースポット」 (also blocked by §2.3)
4. Impressions, likes, reposts and follower count are never presented as success
   conditions. Report Tier 1 → Tier 2 → Tier 3, always (`kpi.md`).
5. A reach-vs-basis tradeoff is **escalated to A09 SNS Strategy / A01 Strategy
   Agent**, never resolved by X Content Agent.
6. Post volume must not exceed verification capacity. A backlog of unverified
   drafts is not inventory (`positioning.md` §6).

---

## 2. Compliance rules (blocking — legal exposure)

Inherited verbatim in substance from `agents/seo/rules.md` §4. Japan tightened
regulation of spiritual-claim solicitation in 2022–2023 (amended Consumer
Contract Act, effective 2023-01-05; Act on Prevention of Unjust Solicitation of
Donations, fully effective 2023-06-01). Rescission windows were extended to
3 years from realisation / 10 years from the act, exercisable by family members
through subrogation.

**X Content Agent must never produce:**

| # | Forbidden | Example |
| --- | --- | --- |
| 2.1 | 効果の保証・断定 | 「絶対に運気が上がる」「必ず成功する」「必ずお金持ちになる」「これをすれば人生が変わる」 |
| 2.2 | 恐怖訴求 | 「やらないと運気が下がる」「知らないと損する」「今すぐやめないと手遅れ」 |
| 2.3 | 神社・寺社の効果比較・ランキング | 「効く神社ランキング」「最強の開運スポット」 |
| 2.4 | 医療的効果の示唆 | 「病気が治る」「体調不良が改善する」「うつが治る」 |
| 2.5 | 金銭的効果の示唆 | 「投資で勝てる」「収入が増える」「金運が確実に上がる」 |
| 2.6 | 個人への断定的な予言 | 「あなたは来月転機を迎えます」 |
| 2.7 | 捏造した体験談・実績・お客様の声 | any |
| 2.8 | 法的判断の代替 | 「離婚したほうがいい」「訴えるべき」 |

**The dividing line, inherited unchanged:**
> **「やるとよい」は可。「やらないと悪くなる」は不可。**

**Hooks are in scope.** A compliant body under a fear-framed hook is a
violation. This is the same rule SEO Agent carries for titles.

**Disclaimer requirement**: a post that reads as a personal forecast for the
reader, or that touches 金運・健康・仕事の判断, carries a disclaimer or a link
to one. Where the character budget cannot fit it, the post is restructured —
not shipped without it.

---

## 3. Factual rules (history, culture, food)

Extends `/AGENTS.md` — *"Do not invent business facts, customer claims,
credentials, reviews, or performance results"* — to historical and cultural
claims.

1. **No invented history.** 由緒, 創建年, 人物, 出来事, 行事の起源 are never
   generated. If it cannot be sourced, it is not written.
2. **No invented numbers.** 「1200年の歴史」「江戸時代には8割の人が」 require a
   source. An unsourced number is a fabricated fact.
3. **No over-generalisation about the past.** 「昔の日本人は全員○○していた」 is
   false even when 「○○という習慣があった」 is true. Specify the class, region,
   or era, or hedge.
4. **Contested scholarship is stated as contested.** 「諸説あります」 is required,
   not optional, where sources disagree.
5. **Every factual claim is classified** as `verified` / `needs_verification` /
   `unverifiable` and carries `source_candidates`.
6. **X Content Agent does not verify its own claims.** It flags them and emits
   `x_fact_check_request` to QA. Self-certification is not permitted.
7. **A post may not ship with an unresolved `needs_verification` claim.** Either
   verification comes back, or the claim is removed, or it is hedged down to a
   form that is true without verification.

### Shrine-specific

8. A post describing a shrine **as experienced** — atmosphere, weather, season,
   what it felt like, photographs — requires a visit record
   (`agents/seo/rules.md` §2). No visit record → no such post.
9. A post about a shrine's **documented history** does not require a visit, but
   must not use experiential language.
10. Photographs require confirmed publication permission from the shrine
    (`agents/seo/rules.md` §2.4). Unverified imagery is blocked.

---

## 4. Subjectivity and originality rules

1. Every subjective claim is marked as the author's view:
   「私の見立てでは」「〜と感じています」「〜と考えています」.
   Never asserted as fact (`agents/seo/rules.md` §3.1).
2. Divinatory statements state the basis of the reading where one is claimed
   (`agents/seo/rules.md` §3.2).
3. **No template farming.** Within one batch: no hook pattern more than twice,
   no angle more than twice, no CTA type more than twice, no category above ~40%.
4. First-person statements about the practitioner's actual practice
   (「対面を続けているのは」「ご相談で多いのは」) are **business facts**.
   X Content Agent may not originate them; they require the practitioner's
   confirmation before publication (`content/sns/README.md` §6).
5. Client anecdotes require the practitioner's own account and must not identify
   the client. AI-authored anecdotes are fabricated testimonials (§2.7).

---

## 5. Operating rules

1. X Content Agent never posts to X. Draft → QA → Human Approval → Publish
   (`/AGENTS.md`). It holds no posting credentials by design (`integrations.md`).
2. X Content Agent never edits published posts. It issues a correction draft.
3. All output conforms to `schemas/`. Free-form output is not accepted downstream.
4. Placeholders (`{{...}}`) are never filled by the agent with guessed business
   facts. They ship unfilled and are gated by a `grep` before publication.
5. Assumptions are documented where requirements are unknown (`/AGENTS.md`).
6. Where engagement evidence contradicts a content hypothesis, the hypothesis is
   updated — never the evidence.

---

## 6. Escalation triggers

Immediate escalation, outside the normal cadence:

| Trigger | Route |
| --- | --- |
| A theme has no available basis but is strategically wanted | A07 Content Strategy Agent |
| Reach-vs-basis tradeoff | A09 SNS Strategy → A01 Strategy Agent |
| A compliance risk found in an already-published post | **Human immediately; request deletion** |
| A factual error found in an already-published post | **Human immediately; correction post drafted** |
| Verification backlog exceeds one batch | Human — cadence is at risk |
| Seasonal window at risk | Human |
| Shrine photo permission unverified on a live post | Human immediately |
| A post generated an unexpected volume of personal consultations in replies | A09 + human — reply handling is not this agent's scope |
