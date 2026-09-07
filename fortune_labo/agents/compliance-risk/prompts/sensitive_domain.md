# Prompt — Sensitive Domain Treatment

Run **before drafting** when A07 flags a `sensitive_domain`, and again after
drafting to verify the rules were followed.

Pre-drafting costs one revision. Post-drafting costs three, and burns
practitioner review time — the scarcest resource in this system.

## The principle

**Divination is never a substitute for professional judgment in these domains —
not even implicitly, through sequence or juxtaposition.**

A passage that describes a health worry, then offers a reading, then says nothing
about seeing a doctor, has made an implicit claim even with no explicit one.

---

## Medical

| Never | Required |
| --- | --- |
| Diagnosis, prognosis, or naming a condition | Refer to a medical professional |
| `病気が治ります` / `体調が良くなります` | `体調の不安は医療機関にご相談ください` |
| Advice to start, stop, or change treatment | Never, in any framing |
| Divinatory claim about a health outcome | Never |
| Mental-health adjudication | Refer; if crisis-adjacent, prominent support referral |

Referral placement: **in the same section as the topic**, not only in a footer.

---

## Financial

| Never | Required |
| --- | --- |
| Investment, trading, or purchase-timing advice | Financial claims are out of scope entirely |
| `この時期に買えば上がります` | Remove — no compliant reworing exists |
| Business-outcome guarantees | Never |
| `金運が上がる` as a promise | Reframe as a way of looking, or remove |
| Divinatory claim about a market or a return | Never |

Money is the domain where the solicitation rules bite hardest, because a
financial-anxiety claim adjacent to a paid service is close to the exact
mechanism the 2023 legislation describes.

---

## Legal

| Never | Required |
| --- | --- |
| Statement of legal position or rights | `法的な判断は専門家にご確認ください` |
| Contract, dispute, or divorce outcome claims | Refer |
| `法的に問題ありません` | Remove |
| Divinatory claim about a legal outcome | Never |

---

## Major life decisions

| Never | Required |
| --- | --- |
| `別れるべきです` / `辞めるべきです` / `引っ越すべきです` | Present considerations; the reader decides |
| Framing a decision as fated or unavoidable | Preserve the reader's agency |
| Timing pressure on an irreversible decision | Never |

Acceptable framing: `判断の材料のひとつとして` · `ご自身で決められることですが` ·
`一般的な傾向として`.

---

## Crisis adjacency

Where a reader's situation plausibly involves harm to themselves or others:

1. **No divinatory claim about the outcome**, in any framing
2. A referral to appropriate professional support, **prominently placed**
3. No CTA to a paid service adjacent to the crisis content
4. Escalate to the human — this is not a routine treatment rule

---

## Output — treatment rules (pre-drafting)

Per flagged domain:

```
domain
what_may_not_be_claimed     explicit list
required_referral           the exact referral text
required_framing            how the topic may be discussed at all
required_placement          where the referral must appear
disclaimer_text             if additional to the standard one
cta_restriction             whether a CTA may appear near this content
```

Binding on A08 and A10.

## Output — verification (post-drafting)

Confirm each rule was followed, and check specifically for the **implicit** claim:
does the sequence of topic → reading → CTA imply that the reading addresses the
sensitive matter, even where no sentence says so? If yes, that is a finding.
