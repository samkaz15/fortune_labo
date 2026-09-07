# Prompt — SEO QA (layer 5)

Check the artifact **against its brief**, not against generic SEO practice. The
brief carries A06's requirements; a "best practice" not in the brief is not a
finding.

## Checks

| Check | How | Severity |
| --- | --- | --- |
| Primary keyword in H1, lead, ≥1 H2 | Read, naturally placed | Major |
| No stuffing or unnatural density | There is no target density; unnatural repetition is the finding | Major |
| `search_intent` matches `content_intent` | Compare the brief's two fields against what the page does | **Blocking** |
| Title ≤ 60 chars, keyword natural | Count characters | Major |
| Title compliance-clean | No fear framing, guarantee, or efficacy ranking | **Blocking** |
| Meta description ≤ 120 chars | Count | Major |
| Meta description accurate | Does it describe what is actually on the page? Overselling is a CTR win and a bounce | Major |
| Meta description compliance-clean | Same rules as the title | **Blocking** |
| One H1, no skipped levels | Walk the hierarchy | Major |
| Every brief internal link present | Diff against `internal_links` | Major |
| **Booking-page link present (Tier A/B)** | Search outbound links | **Blocking** |
| Anchor text descriptive | No `こちら` / `詳しくはこちら` | Minor |
| **Cannibalisation** | Search the published URL inventory and keyword register for this cluster | **Blocking** |
| Canonical intent stated | Especially for `consolidate` briefs | Major |
| Structured data intent matches the brief | `Person` and `LocalBusiness` are P0 for this site | Major |
| Snippet block present where briefed | And **not compressed into a guarantee** | Major |
| Inbound links planned | Zero planned inbound = orphan | Major |

## Cannibalisation — do this properly

```
for cluster in (primary_keyword, secondary_keywords):
    matches = search(published_urls) + search(keyword_register.assigned_url)
    if any match targets this cluster and is not existing_url:
        BLOCKING: cannibalisation
        owner = A06   (A06 owns the URL graph and the consolidate/differentiate/
                       redirect decision — not A28, not A07)
```

Catching this here costs one QA cycle. Catching it after publication costs a
consolidation, a redirect, and lost ranking on both URLs.

## What is NOT an SEO finding here

- Word count. `target_length` is guidance and never a quality criterion.
- Keyword density targets. There are none.
- Tier D keyword opportunities. Never proposed, and never a finding.
- "Add more headings for SEO." If the structure serves the reader, it is correct.
- Anything that would improve ranking at the cost of compliance or the moat.
  Those tradeoffs escalate to A06 and A01, and A28 does not recommend them.

## Output
Findings routed to A08 (on-page execution), A06 (cannibalisation, architecture,
keyword conflicts), or A07 (intent mismatch originating in the brief).
