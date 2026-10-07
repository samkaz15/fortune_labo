# Content Opportunity Index

Version: 1.0.0. `generate_opportunities(inventory, topics)` compares evidence-linked topic candidates against existing titles, topic clusters, and registered keywords. `topics_from_intelligence` reads the explicit `topic_candidates` arrays in structured Content Intelligence. A keyword is a planning candidate, not measured search demand.

Each opportunity contains `opportunity_id`, `genre`, `topic`, `keyword`, `search_intent`, `reader_need`, `existing_content_overlap`, `free_premium_candidate`, `reason`, `evidence_refs`, and `priority_candidate`. IDs are stable hashes of genre/topic/keyword/intent. Identical input topics deduplicate. There is no numeric priority or score; the optional labels are `review`, `consider`, and `defer`.

Overlap records preserve matching content IDs and reasons: same registered keyword, same topic cluster, same title, or keyword in title. Strong overlaps are returned in `suppressed` for consolidation or distinct-intent review. A07 must inspect overlap resolutions before selecting them. Light overlaps remain review candidates. FREE/PREMIUM here is only a candidate; A07 must use Content Intelligence and FREE_PREMIUM_RULES for its decision.

`coverage_status` separates three cases:

- `potential_gap`: no index match, but inventory completeness is partial or unknown. It does not establish that the theme has never been written.
- `no_index_match`: no registered match in a confirmed complete snapshot. Semantic coverage still needs editorial review.
- `overlap_review`: some existing index evidence overlaps.

The current user-confirmed empty initial inventory can be compared against the approved topic catalog. The three A07/A08 test fixtures are a separate draft register: future planning should also compare against that register to avoid commissioning duplicate work. A07 receives both the actual inventory and draft index, together with selected opportunity evidence.

The schema is [content_opportunity_index.schema.json](schemas/content_opportunity_index.schema.json). Topic evidence references must be nonempty. Unknown keyword, intent, need or priority remains null. No measured demand, priority weight, or automatic commission is fabricated.

The current registered test drafts are included in the comparison through `draft_index=...`. A reviewed coverage mapping can be supplied as `reviewed_overlaps=[{opportunity_id, content_ids, evidence_refs, reason}]`; each referenced content ID must exist in either compared index, and each opportunity ID must exist in the supplied catalog. This records an explicit editorial judgment instead of guessing semantic similarity from titles.

[reviewed-opportunity-overlaps.json](reviewed-opportunity-overlaps.json) records the assistant's editorial review of two overlaps: career planning with FL-TEST-A / FL-TEST-C, and contact decisions with FL-TEST-B. These are review judgments with brief references, not human publication approval. The current opportunity register contains **9 active candidates and 2 suppressed overlap candidates** from 11 initial topics. All remain subject to human review. The existing WordPress article count remains zero.

To regenerate, read `existing-content-index.json`, `test-content-index.json`, and `content-intelligence.json`; call `topics_from_intelligence`, then `generate_opportunities(existing, topics, draft_index=tests, reviewed_overlaps=review_document['overlaps'])`. Exact or reviewed matches in draft content suppress duplicate new commissions just as matches in existing content do. A07 must read both indexes and resolve suppressed topics upstream before selecting one.
