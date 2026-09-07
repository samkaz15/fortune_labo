# Prompt — Short Video Script (TikTok / YouTube Shorts)

## Task
Write a 30–60 second vertical video script from Master Content.

## Precondition
**Real visit footage exists.** No footage → `skip`. Never propose generated
imagery of a real shrine, and never propose stock footage presented as the
practitioner's own visit.

## Structure

| Beat | Time | Content |
| --- | --- | --- |
| Hook | 0–2s | A concrete observation or a real question |
| Context | 2–7s | Where we are, who is speaking |
| Substance | 7–45s | The single transferable idea, from first-hand material |
| Close | 45–60s | Soft CTA — profile, or "the full account is on the site" |

## The hook — your highest-risk sentence

**Two seconds. No room to qualify. That is exactly why guarantees appear here.**

| Never | Why |
| --- | --- |
| `参拝すれば願いが叶います` | Guaranteed outcome |
| `知らないと損します` | Fear framing |
| `絶対に行くべき神社` | Overclaim |
| `2027年、この星座は危険です` | Anxiety hook |

| Instead |
| --- |
| `12月の朝、参道に霜が降りていました` (concrete observation) |
| `この神社、実は参拝の順路が決まっています` (specific, checkable) |
| `お客様からいちばん多い質問がこれです` (real question) |

The strongest hook available to this account is a **real observation from a real
visit**. No competitor with an AI subscription has one.

If the honest hook does not fit in two seconds, `skip`. Do not shorten the
qualification to make room.

## Script format

```
[00:00–00:02]  VISUAL: <footage ref id>
               ON-SCREEN: <≤15 chars>
               VO/SPEECH: <line>
```

Every beat carries a footage reference id from the cleared inventory. No beat
says "b-roll of a shrine".

## On-screen text
≤15 characters per frame, and **every frame is compliance-scoped**. A frame
reading `運気アップ` is a violation regardless of what is said aloud.

If a judgment appears, its attribution marker appears with it. If the marker does
not fit the frame, the judgment does not go in that frame — put it in the
voiceover instead.

## Caption and hashtags
Caption ≤100 chars, complete on its own. 3–5 hashtags, none implying a guarantee
(`#願いが叶う`, `#絶対当たる`, `#運気アップ確実` are all violations).

## Audio
Note whether a trending sound is suitable. Third-party music requires a confirmed
licence recorded in the artifact. Voiceover is preferred where a judgment is
being stated — the practitioner's voice is the asset.

## Disclaimer
Any video carrying a divinatory judgment carries the disclaimer in the caption or
a closing frame.

## Output
`video_direction` and content fields of `schemas/channel_content.schema.json`.
YouTube Shorts re-cuts the same script for its own caption and title; it never
duplicates the TikTok caption verbatim.
