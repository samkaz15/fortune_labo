# SNS Content Agent — Responsibilities

## A. Channel viability check (before any writing)

For each channel A07 marked `strong` or `possible`, confirm the raw material
actually supports it. A10 may **downgrade** A07's viability to `skip`; it may not
upgrade `skip` to anything.

| Channel | Hard requirement | If absent |
| --- | --- | --- |
| Instagram | Cleared photography or a designed visual concept | `skip` |
| TikTok | A visual sequence and a hook that lands in 2 seconds | `skip` |
| X | A point that stands alone in ~140 Japanese characters | `skip` |
| YouTube | Enough substance for 5+ minutes without padding | `skip` |
| Threads | A genuine question worth answering | `skip` |
| Facebook | Context worth 200–400 characters | `skip` |
| LINE | A reason for an existing follower to care *now* | `skip` |
| Ameba | A narrative arc | `skip` |
| note | Depth beyond what the article already says | `skip` |

`skip` with a recorded reason is a correct, complete output.

---

## B. Instagram — visual, saveable

**Objective:** saves and profile visits. Saves outrank likes.

| Element | Spec |
| --- | --- |
| Format | Carousel (5–10 slides) or single image |
| Slide 1 | The hook. Readable at thumbnail size. ≤ 20 characters. |
| Slides 2–n | One idea per slide, ≤ 60 characters of on-image text |
| Final slide | CTA — profile link, or save-for-later |
| Caption | 300–800 chars. Opens with the value, not with 「こんにちは」 |
| Hashtags | 10–15, mixed: shrine name, region, practice, general. In the caption, not a comment |
| Visual direction | What each slide shows, from the **cleared photo inventory**. Never "generate an image of the shrine". |

**Photo permission is a hard gate.** `photo_permission_status: pending` blocks the
whole Instagram output, not just the affected slide.

---

## C. TikTok — short video script

**Objective:** reach and discovery among people who do not know the practitioner.

| Element | Spec |
| --- | --- |
| Duration | 30–60s |
| Hook | **First 2 seconds.** A concrete observation or a real question — never `知らないと損する` |
| Structure | Hook → context (5s) → substance (20–40s) → soft CTA (5s) |
| Script | Line by line with timecodes |
| On-screen text | Per beat, ≤ 15 characters per frame |
| Shot list | What footage each beat needs, sourced from real visit footage |
| Audio | Trending-sound suitability, or voiceover |
| Caption | ≤ 100 chars |
| Hashtags | 3–5 |

**Compression is the risk.** A 2-second hook has no room for qualification, which
is exactly why guarantees appear there. If the honest version of the hook does not
fit, the answer is `skip`, not a shorter promise.

---

## D. X — short, quotable, conversational

**Objective:** reach, replies, and quotable authority.

| Element | Spec |
| --- | --- |
| Format | Single post, or a 3–5 post thread when the idea genuinely needs it |
| Length | ~140 Japanese chars per post |
| Opening | The point. No throat-clearing, no `【保存版】` |
| Thread | Post 1 stands alone; each subsequent post adds, never continues a sentence |
| Link | Last post only, and only when the article genuinely extends the point |
| Hashtags | 0–2. More reads as spam on X |
| CTA | Usually none. A quotable observation outperforms an ask |

A one-line first-hand observation (`12月の朝、参道に霜が降りていました`) does more
for this account than a listicle. Generic advice threads are Tier D behaviour and
are not produced.

---

## E. YouTube — video concept and script

**Objective:** trust and depth. The channel where a named practitioner is most
persuasive.

| Element | Spec |
| --- | --- |
| Title | ≤ 60 chars, searchable, no fear framing, no clickbait promise |
| Hook | First 15 seconds: what this video answers and why this person |
| Structure | Chaptered outline with timecodes |
| Script | Talking-head script or narration, spoken register (not article prose) |
| B-roll | Per chapter, from real visit footage |
| Thumbnail | Text ≤ 9 characters + concept. **Compliance applies to thumbnails.** |
| Description | 3-line summary, chapters, links, disclaimer |
| End screen | Related video + booking page |

Short-form (Shorts) is derived from the TikTok script, re-cut for vertical
YouTube, never duplicated with the TikTok caption verbatim.

---

## F. Threads — conversational

**Objective:** engagement and relationship, not reach.

| Element | Spec |
| --- | --- |
| Length | 100–300 chars |
| Shape | **A question or an observation that invites a reply.** Not a broadcast. |
| Tone | Closest to how the practitioner actually talks |
| Link | Rarely. Threads punishes link-out posts and readers ignore them |
| Hashtags | 0–1 |
| Follow-up | A10 drafts a reply-frame the practitioner can use, never auto-replies |

If the piece yields no genuine question, `skip`. A statement posted to Threads is
just an X post in the wrong place.

---

## G. Facebook — community

**Objective:** reach an older, higher-intent audience with more context.

| Element | Spec |
| --- | --- |
| Length | 200–400 chars |
| Opening | Context first — Facebook readers accept a slower entry |
| Tone | Warm, personal, first-person |
| Link | Acceptable and expected, with a real reason to click |
| Hashtags | 0–3 |
| Visual | One strong image, not a carousel |

Facebook skews toward the demographic most likely to book an in-person reading.
Treat it as a booking channel, not a leftovers channel.

---

## H. LINE — the existing audience

**Objective:** retention, return visits, and bookings from people who already
opted in.

| Element | Spec |
| --- | --- |
| Length | ≤ 500 chars. This message interrupts someone's phone. |
| Opening | Why this matters to *them*, today |
| Cadence | Sparing. Over-messaging causes blocks, and a block is permanent |
| CTA | The most direct of any channel — booking or a dated event |
| Segmentation | Proposed only; A21 CRM owns segments |
| Timing | Proposal only, never scheduled by A10 |

**Highest-risk channel for compliance.** A push message with an anxiety hook to
an opted-in audience is precisely the pattern Japan's 2022–2023 solicitation
rules target. LINE drafts route to A30 for review in every case, without
exception.

**A10 never sends a LINE message.** Human approval, then a human or Codex sends.

---

## I. Ameba — platform-native blog

**Objective:** discovery inside Ameba's own ecosystem.

| Element | Spec |
| --- | --- |
| Length | 800–2,000 chars |
| Register | Warmer, more personal, more conversational than the site article |
| Structure | Short paragraphs, frequent breaks, casual headings |
| Relationship to the article | **A different telling of the same experience**, not a duplicate |
| Canonical | Link to the site article as the source; never republish the article body verbatim |
| Images | Cleared photos only |

Duplicating the site article on Ameba creates a duplicate-content problem A06
will have to clean up. The Ameba version is the narrative, human version; the
site article is the reference version.

---

## J. note — depth

**Objective:** the thinking behind the piece, for readers who want the reasoning.

| Element | Spec |
| --- | --- |
| Length | 2,000–5,000 chars |
| Angle | What the article could not include: the method, the doubt, the process |
| Structure | Essay with headings |
| Paid content | Never proposed by A10. That is a business decision for A01/A04. |
| Relationship to the article | Extends, never duplicates |

note is where the practitioner's `practitioner_judgment` material — the
divinatory basis, the reasoning, the uncertainty — is most valuable, and where
the moat is most visible.

---

## K. Cross-channel sequencing

A10 proposes an order and rationale; a human approves and posts.

```
Day 0   Site article published
Day 0   X          — one quotable observation + link
Day 1   Instagram  — carousel from the visual material
Day 2   Threads    — the open question
Day 3   Facebook   — the contextual post
Day 4   note       — the depth piece
Day 5   Ameba      — the narrative retelling
Day 7   LINE       — only if there is a dated, concrete reason
Week 2  TikTok / YouTube — once footage is edited
```

This is a **default**, not a rule. Seasonal deadlines override it. A09, once
implemented, owns the real calendar.

---

## L. Brand consistency across channels

Register shifts by channel; **the practitioner does not.**

| Constant across all nine channels |
| --- |
| Divination framed as a way of looking, never a guarantee |
| Judgments carry attribution markers |
| No fear framing, in any format, including hooks and thumbnails |
| First-hand claims traceable to the same source material as the article |
| Medical / financial / legal matters referred, never adjudicated |
| The same practitioner voice — calmer or warmer, never a different person |
