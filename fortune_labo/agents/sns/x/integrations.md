# X Content Agent — Integrations

Read-only by design, and in Phase 1, not connected at all.

## Posting: none, deliberately

**X Content Agent holds no X credentials and no posting capability.**

This is a design decision, not a missing feature. `/AGENTS.md` requires that no
agent autonomously publishes customer-facing content. Posting to X is
customer-facing and effectively irreversible — a deleted post has already been
seen, screenshotted, and possibly reposted.

The agent produces drafts. A human posts them.

If a posting integration is ever built, it must satisfy all of:

1. Human approval recorded **per post**, not per batch
2. Dry-run / preview mode showing the exact rendered post
3. Scoped write credentials, never stored in Git (`/AGENTS.md`)
4. `basis_coverage == 1.0` and zero unresolved placeholders enforced at the
   integration boundary, not only in the agent
5. An audit log of what was posted, when, and under whose approval

Until all five exist, the integration is not built.

## X API — read

| Data | Endpoint area | Phase | Purpose |
| --- | --- | --- | --- |
| Post metrics (impressions, engagements, likes, reposts, replies, bookmarks) | Post analytics | 2 | Tier 3 + `bookmark_rate` |
| Profile clicks, follows attributed to a post | Post analytics | 2 | Tier 2 |
| Link clicks | Post analytics | 2 | Tier 2 |
| Account follower count over time | Account analytics | 2 | Tier 3 |

**A18 Analytics Agent owns the connection.** X Content Agent does not call the
API; it consumes what Analytics caches to `data/`. This mirrors
`agents/seo/integrations.md`.

Note on availability: bookmark counts and per-post profile-click attribution are
not uniformly available across X API access tiers. Where the API does not expose
them, they are read manually from the X analytics UI and entered by a human. This
is acceptable at this volume and must not be worked around by substituting a
proxy metric — `bookmark_rate` has no substitute in this KPI structure.

## GA4

| Data | Phase | Purpose |
| --- | --- | --- |
| Sessions with X as source/medium | 2 | `x_site_sessions` |
| Landing pages from X | 2 | Which posts drove which pages |
| Service / booking page views from X | 2 | `x_service_page_views` |
| Booking conversions with X first-touch attribution | 3 | Tier 1 KGI |

Owned by A18 Analytics Agent. Read-only.

**UTM requirement**: every link posted to X carries a UTM tag identifying the
post `id`, so performance is attributable to a production decision (category,
angle, hook pattern) and not only to a URL. Without this, `outputs.md`'s
handoff to Analytics degrades to guesswork.

## WordPress

Read-only. Published articles are theme sources and `read_more` targets.
X Content Agent never writes to WordPress — that is A25 WordPress Agent's
interface, and it too is human-gated.

## Repository

| Path | Access | Purpose |
| --- | --- | --- |
| `agents/sns/x/` | read | Own specification |
| `agents/seo/` | read | Inherited positioning, rules, seasonal calendar |
| `content/sns/drafts/` | **write** | Batch draft files |
| Visit records (path TBD) | read | `firsthand` basis |
| `data/` (Phase 2) | read | Cached analytics |

Writing batch drafts to the repository is the agent's only write path, and it
writes drafts only — never anything customer-facing.

## Secrets

None held by this agent. Per `/AGENTS.md`, secrets, API keys and tokens are
never committed. Analytics credentials belong to A18 Analytics Agent and live in
environment variables.
