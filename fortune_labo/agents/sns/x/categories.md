# X Content Agent — Content Categories

Four categories. Every post belongs to exactly one, recorded in the `category`
field of `schemas/x_post.schema.json`.

Category is **what the post is about**. Tier (`positioning.md` §5) is **how
defensible it is**. They are independent: a Category C post can be X-A if it
carries the practitioner's own judgment, or X-C if it only carries a mechanism.

---

## A. 歴史・日本文化

**What it covers**

神社の由緒と歴史 / 日本の暦 / 旧暦 / 二十四節気 / 七十二候 / 五節句 /
節分・立春 / 大祓 / 年中行事 / 昔の日本人の生活習慣 / 歴史上の人物と習慣 /
地域の信仰 / 日本文化の背景

Seed examples from the brief:

- 寒川神社は昔どんな場所だったのか
- 伊勢神宮の歴史
- 神社にまつわる日本文化
- 昔の日本人が行っていた習慣
- 日本の暦 / 二十四節気 / 節句 / 重陽の節句 / 旧暦
- 日本の伝統的な開運習慣
- 歴史上の人物と運気・習慣

**Required basis**: `verified_fact`, always. This category cannot rest on
`mechanism` or `practitioner_view` alone.

**Why this category exists**: it is the cheapest way to be genuinely
non-commodity without requiring a shrine visit. History has sources. Sources
are checkable. Checkable content is what gets bookmarked.

**Failure modes specific to A**

| Failure | Why it is a failure |
| --- | --- |
| 由緒の創作 | Fabricating a shrine's history. Absolutely forbidden (`rules.md` §3) |
| 存在しない人物・出来事 | Same |
| 「昔の日本人は全員○○していた」 | Over-generalisation. A class, a region, or an era is not "everyone" |
| 出典のない数字 | 「1200年の歴史」 without a source is an invented fact |
| 諸説あるものを断定 | Where scholarship differs, the post must say so |

**Handling uncertainty**: 「〜と言われています」「〜という説があります」「諸説あります」
are permitted and expected. They are not weak writing here — they are accuracy.
A post that hedges correctly is stronger than one that asserts wrongly.

**Shrine-specific rule**: a post about a *specific* shrine that describes the
place as experienced — atmosphere, season, what it felt like — requires a visit
record (`agents/seo/rules.md` §2). A post about a shrine's *documented history*
does not, but it must not slip into experiential language.

---

## B. 開運アクションの具体的解説

**What it covers**

瞑想 / 朝の散歩 / 掃除と運気 / 部屋の整理 / 朝日を浴びる / 感謝を言葉にする /
神社参拝の作法 / 財布の整理 / 不要なものを捨てる / 人間関係の整理 /
睡眠環境 / 食生活を整える

**Required basis**: `mechanism` **plus** at least one of `verified_fact` or
`practitioner_view`. Never `mechanism` alone.

**The rule that defines this category**

> 「○○すると運気が上がります」で終わらせない。
> **なぜその行動なのか**を説明する。

The brief asks for multiple viewpoints, and this agent treats that as a
structural requirement rather than a suggestion. The standard three:

| Viewpoint | What it supplies | Basis it maps to |
| --- | --- | --- |
| **昔からの考え方** | Where the practice comes from, how it was understood | `verified_fact` |
| **心理・行動面** | Why it plausibly changes how a person feels or acts | `mechanism` |
| **現代生活への取り入れ方** | What the reader actually does tomorrow morning | — (the 現代への置き換え section) |

A Category B post that carries only one viewpoint is thin. Two is the working
minimum. Three is the target.

**Boundary — the mechanism claim**

`mechanism` is *reasoning*, not science. Permitted:

> 朝日を浴びると体内時計が整うと言われています。私の見立てでは、生活のリズムが
> 決まると判断がぶれにくくなります。

Not permitted:

> 朝日を浴びるとセロトニンが分泌され、うつ病が改善します。

The second makes a medical claim (`rules.md` §2). Where a post wants to reach
for physiology, it either cites a source and stays descriptive, or it drops the
claim. It never upgrades a plausible mechanism into a health outcome.

---

## C. 占い・開運コンテンツ

**What it covers**

運気を意識した行動 / 運気が落ちているときの過ごし方 / 運がいい人の習慣 /
金運・恋愛運・仕事運・人間関係を整える習慣 / 運気の切り替わりのサイン /
開運日 / 季節ごとの開運アクション / 日本の暦と運気 /
九星気学・算命学など占術に関連する話

**Required basis**: `practitioner_view` or `verified_fact`.
This is the category where the basis rule matters most, because it is the
category where unsupported assertion is easiest.

**Framing requirements** (all from `agents/seo/rules.md` §3–4)

| Instead of | Write |
| --- | --- |
| 「金運が上がります」 | 「金運を意識するなら、昔から○○と言われてきました」 |
| 「この行動が正解です」 | 「占いの考え方では、○○と捉えます」 |
| 「運気が下がります」 | 「整えるきっかけとして○○があります」 |
| Asserting a judgment as fact | 「私の見立てでは」「〜と感じています」 |

**The 「やめた方がいい習慣」 problem**

The brief lists 「運気が落ちているときにやめた方がいい習慣」 as a theme. It is a
legitimate theme and it sits one word away from a compliance violation.

- Permitted: 「調子が出ないときは、決断を増やすより減らすほうがうまくいく、と
  私は考えています」 — a recommendation, framed as the author's view
- Forbidden: 「これをやめないと運気が下がり続けます」 — fear framing, and
  `agents/seo/rules.md` §4 blocks it outright

The dividing line is the one SEO Agent already carries:
**「やるとよい」は可。「やらないと悪くなる」は不可。**

**Divination content**: posts touching 九星気学・算命学 must state that they are
describing how the method reasons, not predicting an individual's outcome. Any
post that reads as a personal forecast for the reader requires a disclaimer
(`rules.md` §2.6).

---

## D. 食・生活と開運

**What it covers**

季節の食材 / 節句の食べ物 / 五行と食 / 旧暦と食生活 / 朝に食べたいもの /
昔の日本人の食事 / 季節と体調 / 食習慣と生活リズム

**Required basis**: `verified_fact` (the cultural or seasonal claim) plus
`mechanism` or `practitioner_view`.

**The narrative shape the brief asks for**

```
歴史  →  日本文化  →  季節  →  食べ物  →  現代の生活  →  開運という考え方
```

This is not decoration. It is what separates this category from
「これを食べると運気が上がる」, which is a Tier X-D post.

Worked shape, using 重陽の節句:

| Step | Content |
| --- | --- |
| 歴史 | 五節句のひとつ。中国から伝わった行事 — *needs verification* |
| 日本文化 | 菊を用いる行事として定着した — *needs verification* |
| 季節 | 旧暦9月9日。新暦では10月頃にあたる — *needs verification* |
| 食べ物 | 菊酒、栗ごはん — *needs verification* |
| 現代の生活 | 今の暦なら、秋の入り口に季節のものを食べる日として使える |
| 開運の考え方 | 季節の変わり目に体を整える区切りとして意識する |

Note that five of six steps are marked *needs verification*. That is normal and
correct for this category. See `positioning.md` §6 — verification, not writing,
is the bottleneck.

**Hard limits**

1. No health claims. 「体にいい」 is borderline; 「病気が治る」 is forbidden
   (`rules.md` §2)
2. No 「食べれば運気が上がる」 as the whole structure
3. Dietary advice stays general. Anything resembling individual medical or
   nutritional prescription is out of scope and routed to a professional
4. Seasonal food facts are still facts — they need sources like any other
   Category A claim

---

## Category mix in a batch

No category above roughly 40% of a batch (`responsibilities.md` §G).

Suggested steady-state mix, to be recalibrated against measured bookmark rate
per category (`kpi.md`):

| Category | Share | Rationale |
| --- | --- | --- |
| A 歴史・日本文化 | ~35% | Highest bookmark potential, verifiable, no visit required |
| B 開運アクション | ~30% | Highest action potential, drives replies |
| C 占い・開運 | ~20% | Closest to the service, but the thinnest basis — kept deliberately below A and B |
| D 食・生活 | ~15% | Strong seasonal hooks, high verification cost |

The C share being lowest is a deliberate guard. It is the category the account
will drift toward if left unchecked, and it is the one that most resembles what
every other 開運 account already posts.
