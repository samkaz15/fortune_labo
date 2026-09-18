# X Content Agent — Writing Specification

How a post is built. `rules.md` says what is forbidden; this file says what
good looks like.

---

## 1. Reading conditions X Content Agent writes for

| Condition | Consequence for the writing |
| --- | --- |
| Read on a phone, one hand, in a scrolling feed | The first line decides everything |
| Only the first 2 lines are visible before 「さらに表示」 | The subject must be clear before the fold |
| The reader was not looking for this | No assumed context, no 「前回の続き」 |
| Attention lasts seconds unless earned | 結論を先延ばししない |
| Reposts strip context | Every post must stand alone |

---

## 2. Post structure

The standard five-part structure. Not every post uses all five, but a post that
skips ③ 理由 is almost always a Tier X-D post in disguise.

```
① Hook           最初の1〜2行で興味を引く
② 情報           読者が「知らなかった」と思える内容
③ 理由           なぜそうなのか  ← the part that gets bookmarked
④ 現代への置き換え 実際にできる行動へ落とし込む
⑤ CTA            必要に応じて
```

**On ③**: this is the section that distinguishes this account. Most 開運
accounts have ① ② ⑤ and nothing else. If ③ cannot be written, the basis rule
(`positioning.md` §3) was probably not satisfied — go back, do not ship.

**On ④**: 「知識で終わらせず、行動につなげる」. A post the reader cannot act on
is an interesting fact, not content for this account. Category A posts may
legitimately stop at ③, but they should still tell the reader what to notice.

**On ⑤**: optional. A CTA on every post reads as marketing. Roughly half a batch
should have no CTA at all.

---

## 3. Angles

The same theme, entered from different doors. One theme → several posts.

| Angle | Shape | Example opening (theme: 瞑想) |
| --- | --- | --- |
| **教養型** | What this actually is | 瞑想とは、そもそも何をするものなのか。 |
| **誤解型** | Corrects a common misunderstanding | 瞑想＝何も考えないこと、ではありません。 |
| **実践型** | A procedure the reader can follow | 朝5分でできる瞑想のやり方。 |
| **開運型** | Ties it to 運気, with a stated basis | 運気を整えたい人に瞑想をすすめる理由。 |
| **歴史型** | Where it comes from in 日本文化 | 日本人は昔から「心を整える時間」を大切にしてきました。 |
| **問題提起型** | Reframes the reader's assumption | 運が悪いと感じたとき、行動を増やすより先にやることがあります。 |
| **比較型** | Distinguishes two things readers conflate | 「休む」と「整える」は違います。 |
| **季節型** | Anchors to the calendar | 秋の入り口は、呼吸が浅くなりやすい時期です。 |
| **失敗型** | What goes wrong when people try | 瞑想が続かない人に共通していること。 |
| **質問回答型** | Answers a real client question | 「毎日やらないと意味がないですか」とよく聞かれます。 |

Rules:

- Angles from one theme are **spread across the calendar**, never consecutive
- Each post stands alone; no cross-references to earlier posts
- If two angles produce near-identical bodies, one was not a real angle
- No angle used more than twice in one batch
- 質問回答型 is the highest-value angle when a real client question exists,
  because the language is the audience's own (`agents/seo/inputs.md`)

---

## 4. Style rules

From the brief, treated as binding:

1. **最初の一文を強くする** — the first sentence carries the post
2. **1文を長くしすぎない** — roughly 40 全角文字 as a ceiling
3. **改行を適切に使う** — a wall of text is not read on a phone
4. **難しい言葉を避ける** — 専門用語は使うなら必ず説明する
5. **一文一義** — one sentence, one idea
6. **結論を先延ばししない** — the payoff is not at the bottom
7. **「なぜ？」と思わせる** — the reader should want ③
8. **知識で終わらせず行動につなげる**
9. **無意味な煽りをしない**
10. **毎回「運気が上がります」で終わらせない**
11. **同じ構成・同じ表現の量産を避ける**

### Concrete formatting

| Element | Guidance |
| --- | --- |
| Line length | ~20–25 全角文字 per visual line on a phone |
| Paragraph | 1–3 lines, then a blank line |
| Blank lines | Used to pace, not to pad. Two consecutive blank lines is padding |
| 体言止め | Sparingly. Overuse reads as a template |
| 箇条書き | Good for 実践型 and 食 posts. Bad for 歴史型 — history needs prose |
| 記号・絵文字 | Default none. This account's tone is a professional's, not a feed's |
| 数字 | Concrete numbers are strong, but each one needs a source (`rules.md` §3) |

### Character budget

X allows 280 weighted characters: 全角 counts as 2, URLs count as 23 regardless
of length. Practical budget:

| Post shape | Budget |
| --- | --- |
| Text only | ~140 全角文字 |
| With one URL | ~128 全角文字 + URL |
| With one hashtag (~6 chars) | subtract ~6 |

**Count after placeholder substitution, never before** — the same trap recorded
in `content/sns/drafts/2026-09/x.md`.

---

## 5. Single post or thread

| Use a single post when | Use a thread when |
| --- | --- |
| ③ 理由 fits in the budget | The explanation genuinely needs more than ~140 chars |
| The point is one idea | The theme has sequential steps (作法, 手順, 暦の流れ) |
| The post is a hook into a longer article | The content would lose meaning if cut |

Thread rules:

- The first post must work **alone**. Most readers never open the thread
- Maximum 5 posts. Longer belongs on Ameba or the site (`repurpose_candidates`)
- No 「続きはリプ欄」 as a device to farm engagement — the first post still has
  to deliver something complete
- Number the posts (1/4 など) so a reader knows the length before committing

---

## 6. Hashtags

- 0–2 per post. Default 0
- Permitted: 神社名, 地域名, 節句・暦の名称, 占術名
- Forbidden: Tier X-D tags (`#今日の運勢` `#無料占い` `#タロット` `#12星座`),
  outcome tags (`#開運確定` `#願いが叶う`), and engagement-farm tags
- A hashtag is not a substitute for a subject line. If the post needs the tag to
  be understandable, rewrite the post

---

## 7. Hook patterns

X Content Agent generates **at least 3 hook candidates per post** and records
why one was chosen (`schemas/x_post.schema.json` → `hook_candidates`).

| Pattern | Template | Example |
| --- | --- | --- |
| **意外な事実** | 実は、○○には△△があります | 実は、寒川神社には知っておいた方がいい歴史があります。 |
| **前提の否定** | ○○だと思っていませんか？ | 瞑想は「何も考えないこと」だと思っていませんか？ |
| **順序の逆転** | 最初に変えてほしいのは○○ではありません | 運気が落ちているとき、最初に変えてほしいのは財布ではありません。 |
| **歴史の引き** | 昔の日本人は、○○していました | 昔の日本人は、朝起きて最初に手を洗っていました。 |
| **問いかけ** | なぜ○○なのか、考えたことはありますか | なぜ節句は奇数の月に重なるのか、考えたことはありますか。 |
| **具体の提示** | ○月○日は、△△の日です | 9月9日は、五節句の最後にあたる日です。 |
| **経験の共有** | ご相談で多いのは、○○です | ご相談で多いのは、決断そのものではなく時期の迷いです。 |

**Hook failure modes — all blocking:**

| Failure | Example | Why |
| --- | --- | --- |
| 恐怖訴求 | 「知らないと損します」「やらないと運気が下がる」 | `rules.md` §2.2 — legal exposure |
| 効果の断定 | 「これで金運が上がる」 | `rules.md` §2.1 |
| 回収されない引き | Hook promises something the body never delivers | Bookmark rate collapses; trust cost is permanent |
| 誇張された数字 | 「99%の人が知らない」 | Invented statistic (`rules.md` §3) |
| 毎回同じ型 | Three 前提の否定 hooks in one batch | `rules.md` §4.3 |

The hard rule: **a hook may not open a gap the body does not close, and may not
use fear to open it.**

---

## 8. CTA

Vary deliberately. The brief is explicit: **CTAを毎回同じにしない。**

| Type | Example | Use when |
| --- | --- | --- |
| `save` | 保存して、季節の変わり目に読み返してください | The post is reference material |
| `try` | 明日の朝、試してみてください | Category B, a concrete action |
| `share` | ご家族にも教えてあげてください | 節句, 七五三, family-facing themes |
| `question` | あなたはどう思いますか | Opinion-adjacent, builds replies |
| `read_more` | 詳しくは記事に書きました | Only when the article actually exists |
| `booking` | ご相談はプロフィールから | Sparingly — at most once per batch |
| `none` | — | Roughly half the batch |

Constraints:

- No CTA type more than twice per batch
- `booking` at most once per batch — this is an authority channel, not a sales channel
- `read_more` requires a live URL. A CTA pointing at nothing is a broken promise
- Never stack two CTAs in one post

---

## 9. Voice

The account speaks as the practitioner, in the first person.

- 敬体 (です・ます). No 断定調 for subjective content
- Subjective claims carry a marker: 「私の見立てでは」「〜と感じています」
  「〜と考えています」 (`agents/seo/rules.md` §3.1)
- Historical uncertainty carries a marker: 「〜と言われています」「諸説あります」
- No 上から目線. The reader is not being corrected, they are being told something
- Admitting limits is on-brand: 「これはお引き受けしていません」「外したこともあります」

**Important**: because the account speaks in the practitioner's first person,
every first-person statement about their practice is effectively a business
fact. X Content Agent may not originate these — the same gate recorded in
`content/sns/README.md` §6.
