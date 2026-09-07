# SNS Content Agent — Rules

Violations of §1–§4 are **blocking**. A28 rejects the asset and A30 escalates.

---

## 1. No-autopost rules (absolute)

1. **A10 never posts to any platform.** Not Instagram, TikTok, X, YouTube,
   Threads, Facebook, LINE, Ameba, or note.
2. A10 never schedules a post, never queues one for auto-publication, and never
   holds platform credentials.
3. A10 never sends a message to a customer on any channel, including LINE.
4. **A human approves every post individually.** Approving a Repurpose Plan is
   not approving its posts.
5. Where posting is later automated, Codex builds the integration and it must
   still require explicit per-post human approval (`/AGENTS.md`). There is no
   design in which A10 posts autonomously.

---

## 2. Adaptation rules

1. **Never post the article to social.** The article's opening paragraph plus a
   link is not a social post.
2. Never cross-post identical text to multiple channels.
3. Every post must be whole on its own. Teasers that withhold the answer fail.
4. Never build a post around an `ai_structurable` section. That is the part any
   competitor could write, so it builds nothing.
5. A10 may downgrade a channel to `skip`. A10 may never upgrade a channel A07
   marked `skip`.
6. `skip` is recorded with a reason and a `revisit_condition`, never silently
   omitted.
7. Nine posts from one article is a warning sign, not a target. Two strong posts
   beat nine weak ones.

---

## 3. First-hand and fabrication rules (inherited from A08)

1. Every first-hand claim in a post traces to a `source_reference` from the
   Master Content `source_map`. **A social post is a publication** and carries
   the same evidentiary weight as an article.
2. **Never request, imply, or use AI-generated imagery depicting a real shrine.**
   A generated image presented as a visit is a fabrication of the same weight as
   an invented paragraph, and it destroys the exact asset the business is built
   on.
3. Visual direction references the cleared photo/footage inventory by id. It
   never describes an image to be created.
4. `photo_permission_status: pending` blocks every visual channel for that piece.
5. No invented dates, prices, festival timings, access details, or client voices —
   the same list as `../content-production/rules.md` §2.4.
6. Judgments carry their attribution markers **on every channel**, including
   inside a 15-character on-screen frame. If the marker does not fit, the claim
   does not go in that frame.

---

## 4. Compliance rules on social (stricter than on the site)

Short formats compress, and **compression is where guarantees appear**. Every
rule in `../seo/rules.md` §4 applies to every hook, caption, on-screen text
frame, thumbnail, video title, and hashtag.

### Never, on any channel, in any element

| Forbidden | Example |
| --- | --- |
| Guaranteed outcome | `参拝すれば願いが叶います` |
| Fear framing | `行かないと運気が下がります` / `知らないと損します` |
| Anxiety hook | `このままだと2027年は危険です` |
| Efficacy ranking | `本当に効く神社ランキング` |
| Medical claim | `体調が良くなります` |
| Financial claim | `この時期に買えば上がります` |
| Legal claim | any |
| Fabricated social proof | `多くの方が効果を実感しています` |
| Guarantee hashtag | `#願いが叶う` `#絶対当たる` `#運気アップ確実` |
| Untrue scarcity | `残り2枠` when it is not literally true |

### The dividing line, again

> **"Visiting is good" is permitted. "Not visiting is bad" is not.**

### Channel-specific hard rules

| Channel | Rule |
| --- | --- |
| **LINE** | **Every draft goes to A30, without exception.** A push message with an anxiety hook to an opted-in audience is precisely the pattern Japan's 2022–2023 solicitation rules target. |
| **TikTok** | The 2-second hook has no room to qualify. If the honest hook does not fit, `skip`. |
| **YouTube** | Thumbnails and titles are in scope. A compliant video under a fear-framed thumbnail is a violation. |
| **Instagram** | On-image text is in scope. A slide reading `願いが叶う` is a violation regardless of the caption. |
| **X** | A quotable line is quoted without its context. Assume every post travels alone. |
| **Ameba / note** | Long form is no licence for stronger claims. |

### Disclaimer

Required on any post carrying a divinatory judgment, in the channel's native
form: caption text, final carousel slide, video description, or post footer. A
disclaimer is never a licence to make a stronger claim above it.

---

## 5. Platform rules

1. Respect each platform's terms of service, disclosure requirements, and any
   applicable advertising or PR-disclosure obligations (景品表示法, ステマ規制).
2. Sponsored or gifted content is disclosed as required by Japanese law, in the
   post itself — never only in a bio or a linked page.
3. No engagement manipulation: no bought followers, no engagement pods, no
   misleading thumbnails, no fake giveaways.
4. Third-party material (music, images, footage, quotes) is used only with a
   confirmed licence recorded in the artifact.
5. Shrine imagery follows the same permission gate as the site, and any
   shrine-specific photography restriction is honoured on social too.
6. No content about identifiable private individuals, including clients, without
   recorded consent and anonymisation.

---

## 6. Operating rules

1. A10 works from `qa_passed` Master Content wherever possible.
2. A10 never invents a claim the article does not make. A post ahead of the
   material is escalated to A08 / A07, not written.
3. A10 addresses every QA and A30 finding; A30's rewordings are binding.
4. **Engagement is never a defence.** "This format performs" does not justify a
   compliance shortcut, a fear hook, or off-positioning content. A channel
   performing well on commodity content is a P0 moat conflict, escalated to A01.
5. Platform credentials, API tokens, and access keys never appear in this
   repository (`/AGENTS.md`).
6. All outputs conform to `schemas/`.
