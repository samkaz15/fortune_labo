# SNS Content Agent — KPI Structure

## Design principle

Every default social metric — followers, likes, impressions, viral reach — is a
vanity metric for this business. The market evidence in
`../seo/positioning.md` §2 is explicit: the one flat segment of the Japanese
fortune-telling market is the one with no human in the loop, and that is exactly
the segment a follower-maximising social account drifts into.

**A10 is measured on whether social produces qualified contact with a named
practitioner — not on audience size.**

---

## KGI

> Inherited: **organic-sourced and social-sourced booked readings**.

A10 does not get an independent success definition.

---

## Tier 1 — Business outcome

| KPI | Definition | Phase |
| --- | --- | --- |
| `social_sourced_bookings` | Bookings whose first touch was a social channel | 3 |
| `social_list_signups` | LINE / email registrations attributed to social | 2 |
| `profile_to_booking_rate` | Profile visits → booking page → booking | 3 |
| `line_retained_rate` | LINE followers still opted in after 90 days | 2 |

`line_retained_rate` is a **compliance metric wearing a performance costume**.
Blocks and unfollows are what over-messaging and anxiety hooks produce, and a
block is permanent. A falling retention rate means the tone has drifted, and it
is investigated as a compliance question first.

---

## Tier 2 — Authority and moat

| KPI | Definition | Target |
| --- | --- | --- |
| `branded_search_lift` | Practitioner-name searches after a social push | ↑ — the primary social objective |
| `firsthand_post_ratio` | Posts built on visit or judgment material / all posts | **≥ 0.7, never falling** |
| `saves_per_post` (Instagram) | Saves / reach | ↑ — saves indicate real utility |
| `reply_rate` (X, Threads) | Genuine replies / posts | ↑ — conversation, not broadcast |
| `watch_through_rate` (TikTok, YouTube) | Completion | ↑ |
| `skip_rate_with_reason` | Skipped channels with a recorded reason / all skips | **= 1.0** |

`firsthand_post_ratio` is stricter than the site's 0.6 threshold, deliberately:
social has no ranking benefit to trade against, so there is no reason to post
commodity content at all.

`branded_search_lift` connects social directly to A06's Tier 2. When people
leave TikTok and search the practitioner's name, social is doing its job.

---

## Tier 3 — Reach and engagement (diagnostics only)

Never reported as achievement on their own.

| KPI |
| --- |
| `reach`, `impressions`, `views` |
| `likes`, `shares`, `comments` |
| `follower_growth` |
| `link_clicks`, `profile_visits` |
| `posts_published` |
| `hashtag_performance` |

**Follower growth is explicitly Tier 3.** An account of 100,000 followers who
will never book an in-person reading is worth less than 500 who might.

---

## Per-channel objective mapping

Each Channel Content declares one `objective`, and is measured against that one:

| Channel | Primary objective | Measured by |
| --- | --- | --- |
| Instagram | `saves` | saves / reach, profile visits |
| TikTok | `reach` | views, watch-through, branded search lift |
| X | `engagement` | replies, quotes, profile visits |
| YouTube | `trust` | watch time, subscribers, booking-page clicks |
| Threads | `engagement` | genuine replies |
| Facebook | `booking` | link clicks → booking page |
| LINE | `retention` | open rate, retained opt-ins, bookings |
| Ameba | `reach` | platform reach, site referrals |
| note | `trust` | read-through, follows, referrals |

Judging Instagram by reach or X by follower count produces the wrong content.
Each channel is judged on what it is for.

---

## Forbidden framings

A10 must not report, and A09 / A01 must not accept:

- Follower count as a result
- Viral reach on off-positioning content as a success
- "This format performs" as a reason to relax compliance or positioning
- Post count as productivity
- Any Tier 3 movement without a Tier 1 or Tier 2 movement attached

---

## Diagnostic matrix

| Pattern | Likely cause | Owner |
| --- | --- | --- |
| High reach, no branded search lift | Content is generic — anyone could have posted it | **A10** |
| High saves, no profile visits | No path from value to the practitioner | **A10** — CTA |
| LINE opt-outs rising | Over-messaging or tone drift | **A10** — compliance first |
| Engagement good, bookings zero | Wrong audience or wrong channel objective | A09 / A01 |
| A channel skipped every cycle | Material or channel choice is wrong | A07 / A01 |
| Commodity content outperforming first-hand | **Moat conflict — P0** | A01 Strategy |
| A post needed a post-publication correction | Compliance sweep failed | **A10** → A30 |
| `firsthand_post_ratio` falling | Drift toward commodity social | **A10** → A01, P0 |
