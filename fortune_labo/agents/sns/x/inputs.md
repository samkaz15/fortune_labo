# X Content Agent — Inputs

## From the human practitioner (irreplaceable)

| Input | Why it cannot come from anywhere else |
| --- | --- |
| **Real client questions and their exact phrasing** | The audience's own language. Highest-value theme source in the system (same ranking as `agents/seo/inputs.md`) |
| Visit notes, photographs, impressions | The `firsthand` basis. The moat itself |
| Stated views and judgments | The `practitioner_view` basis |
| Divinatory basis for any forecast statement | Only the practitioner holds the method |
| Confirmation of first-person practice claims | These are business facts (`rules.md` §4.4) |
| Shrine photo permission status | Legal gate |
| Posting capacity and cadence tolerance | Bounds batch size |

**Without at least one of the first three, a post cannot reach Tier X-A.**

## From A06 SEO Agent

| Input | Use |
| --- | --- |
| Tier A / B keyword gaps | Themes the site will need authority for later |
| Seasonal calendar (暦・節句・祭事・publish-by dates) | The primary scheduling constraint |
| SERP gaps | Topics where no good explanation exists anywhere |
| Search intent definitions | Who the reader is and what they actually want |
| Visit plans | Advance warning of when `firsthand` material will exist |

## From A07 Content Strategy Agent

| Input | Use |
| --- | --- |
| Approved topic clusters | The theme pool X may draw from |
| Editorial calendar | Alignment with article publication |
| Content priorities | Which cluster to weight this month |

## From A09 SNS Strategy Agent

| Input | Use |
| --- | --- |
| Channel role and target audience for X | Who the account is speaking to |
| Cadence targets | Posts per week |
| Campaign windows | When to concentrate output |

## From A02 Research Agent / A29 Fact-Check Agent

| Input | Use |
| --- | --- |
| Verified historical and cultural facts | The `verified_fact` basis |
| Source references | `source_candidates`, and the citation in the post |
| Shrine 由緒 and 祭事 calendars | Category A and D material |
| Regulatory changes affecting permissible claims | `rules.md` §2 updates |

## From A18 Analytics Agent

| Input | Source | Phase |
| --- | --- | --- |
| Impressions, engagements, likes, reposts, replies | X analytics | 2 |
| **Bookmarks** | X analytics | 2 |
| **Profile clicks** | X analytics | 2 |
| **Follows attributed to a post** | X analytics | 2 |
| **Link clicks to the site** | X analytics + GA4 | 2 |
| Site sessions and behaviour from X | GA4 | 2 |
| Bookings attributed to an X first touch | GA4 + booking system | 3 |

The four bold metrics are the ones this agent is actually steered by (`kpi.md`).

## From A08 Content Production Agent

Published articles and Ameba posts, as theme sources and as `read_more` targets.
X Content Agent does not re-research what the site already published.

## Availability by phase

| Phase | Available | X Content Agent operates on |
| --- | --- | --- |
| **1 — Now** | Repo docs, practitioner input, seasonal calendar, manual observation | Theme pool, angle expansion, batch drafting, fact-check requests. **Fully operational** |
| **2** | X analytics + GA4 read | Measured reweighting of categories, angles, hook patterns |
| **3** | Booking attribution | Tier 1 KPI; true prioritisation by revenue |

**Phase 1 is fully operational.** X Content Agent is not blocked on API access.
Until Phase 2, category and angle weighting is a documented hypothesis, and every
report must say so.

## Input gaps as of implementation

Recorded so downstream agents do not mistake absence for a decision:

| Missing | Consequence |
| --- | --- |
| Practitioner name, service menu, booking URL, region, divination method | Posts ship with `{{placeholders}}`; `booking` CTA cannot be used |
| Any visit record in the repository | Tier X-A firsthand posts cannot be produced at all |
| Standard disclaimer text (`agents/seo/rules.md` §3.4 requires one; none exists) | A proposed draft is in `content/sns/README.md` §3, unapproved |
| A07 / A09 specifications | X Content Agent currently self-serves theme approval, which is a temporary overreach — see `workflow.md` §Interim operation |
