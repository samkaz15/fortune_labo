# Existing Article Classification

Version: 1.0.0. Classifications are separate candidate artifacts. The importer and classifier never rewrite article bodies or silently replace canonical metadata.

`classify_article(record, intelligence, taxonomy, mappings=None)` returns candidates for `genre`, `subgenre`, `access_type`, `search_intent`, `reader_need`, and `cta_role`. Each candidate has `value`, `confidence`, `evidence_refs`, and `reason`. It also retains taxonomy/intelligence versions and the FREE/PREMIUM rationale fields `acquisition_role`, `engagement_role`, `conversion_role`, `retention_role`, and `premium_value` where known.

| Confidence | Evidence and treatment |
| --- | --- |
| high | Explicit editorial metadata compatible with the supplied taxonomy/intelligence. It remains a candidate until human acceptance. |
| medium | One exact taxonomy category-name match or one operator-reviewed category/title/intent/CTA mapping. This is editorial evidence, not measured search behavior. |
| low | Missing or conflicting evidence. Value is null; human review is required. |

Aggregate confidence is the lowest confidence among the six requested fields. Consequently an article with a strong genre candidate but unknown subgenre is still queued for human review. `classify_inventory` reports `classified` as the number with a genre candidate, `unclassified` as the number without a genre candidate, and `human_review` separately. None of these counts means approval has been granted.

Subgenres must exist in the supplied taxonomy. The current foundation does not invent subgenre labels when the taxonomy has none. A genre's general reader needs are not automatically copied into every article. Existing access metadata is checked against the relevant FREE/PREMIUM role in Content Intelligence and references [FREE_PREMIUM_RULES.md](FREE_PREMIUM_RULES.md); actual monetization suitability remains an editorial decision. A long article, public page, the word PREMIUM, and a paid service link are insufficient to establish its access type.

Optional mapping format:

```json
{
  "category_genres": {"verified-category-id": "approved-genre-id"},
  "title_genres": {"reviewed-literal-phrase": "approved-genre-id"},
  "intent_terms": {"reviewed-literal-phrase": "informational"},
  "cta_roles": {"verified-cta-type": "conversion"}
}
```

Mappings require operator review and belong with the private import if they contain site-specific information. Classification evidence references IDs and mapped fields; body excerpts are not stored. An optional transient text argument cannot establish membership rights and is not persisted.

Initial state: the user confirmed zero existing articles, so existing classified = 0, unclassified = 0. Separate synthetic regression fixtures test known, unknown, conflicting and paid-keyword-only cases. Test drafts A/B/C are handled by A07/A08 and are not existing WordPress articles.
