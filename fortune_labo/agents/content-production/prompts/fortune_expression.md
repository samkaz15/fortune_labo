# Prompt — Fortune-Telling Expression Check

Run this over every draft before handoff, and whenever A30 returns a reworing.

## The principle

Divination is **a way of looking**, never a guarantee of outcome. The reader
keeps their agency and their decisions. The practitioner offers a view, not a
verdict.

## Pattern → replacement table

| Detected | Why it fails | Write instead |
| --- | --- | --- |
| `必ず○○になります` | Guaranteed outcome | `占術上はこう見ます` |
| `絶対に成功します` | Guaranteed outcome | `後押しになりやすい時期と見ています` |
| `確実に儲かります` | Financial guarantee | Remove — financial claims are out of scope |
| `参拝すれば願いが叶います` | Efficacy guarantee | `気持ちを整える機会になります` |
| `行かないと運気が下がります` | **Fear framing** | Remove entirely; reframe positively or cut |
| `このままでは手遅れです` | **Fear framing** | Remove entirely |
| `効く神社ランキング` | Efficacy ranking | Remove — never comparative on efficacy |
| `運命は決まっています` | Fate as fixed | `判断の材料のひとつとして` |
| `この生まれの人は必ず○○です` | Deterministic personality | `〜という傾向があるとされています` |
| `病気が治ります` | **Medical claim** | `体調の不安は医療機関にご相談ください` |
| `今買えば上がります` | **Financial advice** | Remove; refer to a professional |
| `法的に問題ありません` | **Legal position** | `法的な判断は専門家にご確認ください` |
| `別れるべきです` / `辞めるべきです` | Major life decision | Present considerations; the reader decides |
| `今すぐ相談しないと…` | Anxiety CTA | Calm, specific, low-pressure invitation |
| `多くの方が効果を実感` | Fabricated result claim | Remove unless a recorded, verifiable source exists |

## Attribution sweep

Every judgment must carry a marker. Scan for sentences that state a divinatory
conclusion **without** one of:

```
私の見立てでは …    〜と感じました    〜と考えています
占術上は …          一般的な傾向として    参考として
```

An unmarked judgment is an asserted fact. That is a compliance violation, not a
wording preference.

## Basis sweep

For `annual_outlook` and `forecast_review`: does the piece state **which method
was applied, and how**? A judgment with no stated divinatory basis is not
publishable (`../../seo/rules.md` §3.2).

## Agency sweep

For personality, compatibility, and birth-date content: does the text describe
tendencies and ways of looking, or does it make a fixed determination about a
real person's character or future? Fixed determinations are rewritten.

## Sensitive-domain sweep

Search the draft for medical, financial, legal, and major-life-decision content.
For each hit: is a professional referral present, and is every divinatory claim
about the outcome removed? If the brief did not flag `sensitive_domain` but the
draft has entered one, **stop and route to A30 before proceeding.**

## The dividing line

> **"Visiting is good" is permitted. "Not visiting is bad" is not.**

Apply it to the title, the lead, every heading, the CTA, the meta description,
and the FAQ — not just the body. A clean body under a fear-framed title is still
a violation.

## Output
Corrected draft, plus a list of every replacement made, so A28 and A30 can verify
the sweep actually ran.
