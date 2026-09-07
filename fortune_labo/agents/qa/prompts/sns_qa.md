# Prompt — SNS QA (layer 7)

Runs on Channel Content assets. Every surface is in scope — not just the caption.

## Surfaces
```
hook · body · CTA · hashtags · on-screen text frames · carousel slide text
thumbnail text and concept · video title · video description · LINE subject/body
```

## Format checks

| Check | Severity |
| --- | --- |
| `character_count` ≤ `character_limit` | **Blocking** |
| Video within duration budget | **Blocking** |
| Format matches the channel (carousel / thread / short video / essay) | Major |
| Hashtag count within the channel's norm | Minor |
| Thread post 1 stands alone; later posts add rather than continue a sentence | Major |
| Not a verbatim cross-post of another channel | Major |
| Post is whole on its own, not an excerpt or a withholding teaser | Major |

**Never accept an over-limit asset that was shortened by cutting the
qualification on a claim.** Check what was removed — if the hedge went and the
claim stayed, that is a blocking compliance finding, not a length fix.

## Compliance checks (all blocking)

| Check |
| --- |
| No guaranteed outcome in any surface, including the hook |
| No fear framing in any surface, including thumbnails |
| No efficacy ranking |
| No medical, financial, or legal claim |
| No fabricated social proof |
| No hashtag implying a guarantee (`#願いが叶う`, `#絶対当たる`, `#運気アップ確実`) |
| No untrue scarcity |
| Attribution markers present on every judgment, on every surface it appears |
| Disclaimer present where a judgment appears |
| Required sponsorship disclosure present (景品表示法 / ステマ規制) |

## Traceability checks (all blocking)

| Check |
| --- |
| Every `firsthand_claims[]` entry resolves to the Master Content `source_map` |
| No claim the source article does not make |
| Photo permission `confirmed` for every visual channel |
| Every `asset_reference` and `footage_reference` resolves to real cleared material |
| **No AI-generated imagery depicting a real place** |

## Channel gates

| Channel | Gate |
| --- | --- |
| **LINE** | A30 review completed. **Blocking without it, always.** |
| TikTok / YouTube Shorts | Hook checked frame by frame — 2 seconds has no room to qualify |
| YouTube | Title and thumbnail compliance-clean |
| Instagram | Every slide's on-image text swept; permission confirmed |
| X | Each post checked as if quoted alone, without its thread |
| Threads | Genuinely conversational, not a broadcast in the wrong place |
| Facebook / Ameba / note | Long form is no licence for stronger claims |

## Consistency check

Does the post contradict the article, or make a claim the article does not?
A post ahead of its source material is a finding routed to A10 and A08 — not a
reason to strengthen the article.

## Output
Findings per channel asset, routed to A10 (format, hooks, hashtags), A30
(compliance adjudication), or the human (photo permission).
