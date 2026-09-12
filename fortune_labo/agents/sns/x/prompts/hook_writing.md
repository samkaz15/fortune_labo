# Prompt — Hook Writing

## Task
Generate at least three hook candidates for a post and choose one, recording why.

The hook decides whether anything else in the post is read. Only the first two
lines are visible before 「さらに表示」, and the reader was not looking for this.

## Patterns

| Pattern | Template | Example |
| --- | --- | --- |
| `surprising_fact` | 実は、○○には△△があります | 実は、寒川神社には知っておいた方がいい歴史があります。 |
| `premise_denial` | ○○だと思っていませんか？ | 瞑想は「何も考えないこと」だと思っていませんか？ |
| `order_reversal` | 最初に変えてほしいのは○○ではありません | 運気が落ちているとき、最初に変えてほしいのは財布ではありません。 |
| `historical_pull` | 昔の日本人は、○○していました | 昔の日本人は、朝起きて最初に手を洗っていました。 |
| `question` | なぜ○○なのか、考えたことはありますか | なぜ節句は奇数の月に重なるのか、考えたことはありますか。 |
| `concrete_date` | ○月○日は、△△の日です | 9月9日は、五節句の最後にあたる日です。 |
| `shared_experience` | ご相談で多いのは、○○です | ご相談で多いのは、決断そのものではなく時期の迷いです。 |

## The two constraints

**1. The hook may not open a gap the body does not close.**
An unredeemed hook costs a bookmark now and trust permanently. Before choosing,
check: does ③ 理由 actually answer what the hook implied?

**2. The hook may not use fear to open the gap.**
「知らないと損します」「やらないと運気が下がる」 are blocked by `rules.md` §2.2 —
legal exposure, not tone. Hooks are in compliance scope: a compliant body under
a fear-framed hook is still a violation.

## Also blocked

| Failure | Example |
| --- | --- |
| 効果の断定 | 「これで金運が上がる」 |
| 誇張された数字 | 「99%の人が知らない」 — an invented statistic |
| 煽り | 「まだ○○してるの？」 |
| 同じ型の反復 | Three `premise_denial` hooks in one batch |

## Method

1. Write three candidates using **three different patterns**. Same-pattern
   variants are one candidate, not three
2. For each, name the reader it catches — different patterns catch different
   readers
3. Check each against the two constraints
4. Choose the one whose promise the body actually keeps. When two are equal,
   prefer the one that carries information over the one that only creates
   curiosity
5. Record the rejected ones and why

`historical_pull` and `concrete_date` carry information in the hook itself.
`premise_denial` and `question` carry only curiosity — stronger openers, but
they fail harder when ③ is thin.

## Output
`hook`, `hook_pattern`, `hook_candidates` (≥3), `hook_choice_rationale`
on the `x_post`.
