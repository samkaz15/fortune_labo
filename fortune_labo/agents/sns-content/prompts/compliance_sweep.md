# Prompt — Social Compliance Sweep

Run before every handoff, over **every element of every asset** — not just the
caption.

## Surfaces in scope

```
hook · body · CTA · every hashtag · every on-screen text frame
carousel slide text · thumbnail text and concept · video title
video description · LINE message subject and body · alt text
```

A compliant video under a fear-framed thumbnail is a violation. A clean caption
under a slide reading `願いが叶う` is a violation.

## Blocking patterns

| Pattern | Example | Fix |
| --- | --- | --- |
| Guaranteed outcome | `願いが叶います` | `気持ちを整える機会になります` |
| Fear framing | `行かないと運気が下がります` | Remove entirely |
| Anxiety hook | `知らないと損します` | Replace with a concrete observation |
| Efficacy ranking | `効く神社ランキング` | Remove |
| Medical claim | `体調が良くなります` | Remove; refer to a medical professional |
| Financial claim | `今が買い時です` | Remove entirely |
| Legal claim | any | Remove; refer to a professional |
| Fabricated social proof | `多くの方が効果を実感` | Remove |
| Guarantee hashtag | `#願いが叶う` `#絶対当たる` | Remove |
| Untrue scarcity | `残り2枠` when untrue | Remove |
| Unmarked judgment | a conclusion with no marker | Add `私の見立てでは` etc. |
| Untraceable first-hand claim | no `source_reference` | Remove the claim |
| Generated imagery of a real shrine | any | **Remove. Non-negotiable.** |

## Attribution check

Every divinatory conclusion carries its marker on the same surface where the
conclusion appears. `私の見立てでは` / `感じました` / `一般的な傾向として` /
`参考として`.

If the marker does not fit the frame, **move the claim to a surface where it
does** — voiceover, caption, description — or cut it.

## Traceability check

For each `firsthand_claims[]` entry: does `source_reference` resolve to a real
entry in the Master Content `source_map`? An untraceable claim is treated as
fabricated and removed.

## Format check

`character_count ≤ character_limit`; duration within budget; hashtag count within
the channel's norm; disclaimer present where a judgment appears.

**Never resolve an over-budget asset by cutting the qualification on a claim.**
Cut the claim.

## Channel escalation

| Condition | Action |
| --- | --- |
| Channel is LINE | **Route to A30, always.** No exceptions. |
| Post carries a judgment | Route to A30 |
| Post enters a sensitive domain (medical / financial / legal / major life decision) | Route to A30 |
| Hook is under 3 seconds or under 20 characters | Route to A30 — compression risk |
| Any blocking pattern found and fixed | Record the replacement so A28 can verify the sweep ran |

## Output
Corrected assets, `compliance` block populated, `requires_compliance_review` set,
and a list of every replacement made.
