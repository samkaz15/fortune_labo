# Existing Content Import

Version: 1.0.0. The user confirmed that the site has **zero existing articles**. [existing-content-index.json](existing-content-index.json) records this initial state as `source_type: user_confirmation`, `source_ref: user_attestation:2026-10-07-existing-articles-zero`, `completeness: complete`, and zero items. No live import was executed. The three editorial test drafts are separate fixtures; they do not increase the existing WordPress article count.

`fortune_labo/editorial/importer.py` imports existing article metadata without changing WordPress. It accepts a local REST JSON export, WXR XML export, or an explicitly supplied public HTTPS site. The HTTP adapter issues only GET requests and follows every returned page. It checks `X-WP-Total`, `X-WP-TotalPages`, duplicate IDs, and changing totals. A failed request aborts instead of storing a successful but incomplete run. See the official [posts reference](https://developer.wordpress.org/rest-api/reference/posts/) and [pagination reference](https://developer.wordpress.org/rest-api/using-the-rest-api/pagination/).

```sh
python3 -B -m fortune_labo.editorial.importer --wxr /private/path/export.xml --site-id fortune_labo
python3 -B -m fortune_labo.editorial.importer --rest-json /private/path/posts.json --site-id fortune_labo
```

Output defaults to ignored `.private/editorial/existing-content-index.json`. Output inside tracked repository directories is rejected. File mode is 0600. A real import is private even when its inputs include publicly accessible pages: metadata may contain draft titles, links, or subscriber details. WXR files, REST exports, bodies, credentials, classification sidecars, and real analytics are not committed. The public repository contains schemas, code, the confirmed empty state, and synthetic or explicitly approved editorial fixtures.

| Index fields | Import behavior |
| --- | --- |
| content_id, wordpress_post_id | Stable namespace hash of operator-assigned site ID plus positive WordPress post ID; repeat imports deduplicate. Reuse the site ID after migrations. |
| title, slug, url, status | Explicit WordPress metadata. Decode HTML title entities and remove markup. Do not interpret `publish` as FREE. |
| publish_date, modified_date | Prefer GMT with `Z`; otherwise preserve local time and record `date_basis: site_timezone_unknown`. WordPress zero dates become null. |
| category, tags | Arrays of `{id, name, slug}`. REST embedded terms resolve names; absent names remain null. WXR channel term definitions resolve IDs where provided. |
| genre, subgenre, topic_cluster | Null unless an explicit metadata mapping supplies a value; candidates remain in separate classification artifacts. |
| access_type | FREE / PREMIUM only through an explicit metadata map; no inference from visibility, title, paywall-like text or status. |
| primary_keyword, secondary_keywords, search_intent, explicit_need, latent_need | Null unless explicit mapped editorial metadata exists. No inferred search demand. |
| article_type, content_depth, cta_type, cta_destination, seo_policy_version | Null unless explicit mapped metadata exists. Never stamp an old article with the current SEO version merely because it was imported today. |
| internal_links | Same-host HTTP(S) links extracted transiently from accessible HTML; fragments removed and duplicates collapsed. Null when the body or origin is unknown; an empty array means inspected and none found. |
| featured_image | `{wordpress_media_id, url, alt_text}` if present. REST embedding and WXR attachment records resolve known fields. Unknown fields stay null. |
| word_count | `cjk_character_plus_latin_number_token_v1`: each Japanese/CJK character plus each Latin/number token counts as one unit; markup/script/style excluded. This is a transparent size proxy, not a Japanese morphological word count. Unavailable or protected content is null. |

`--field-map` accepts a private JSON object such as `{"access_type":"meta.access_type","primary_keyword":"meta.primary_keyword"}`. Only listed editorial fields are copied; other WordPress metadata, authors, users and comments are discarded. Plugin-specific access and SEO keys must be verified before mapping. Fields are not filled from a model's guess.

A public REST run covers only published posts accessible to that endpoint. Its `coverage_complete` can be true for that scope while overall `completeness` stays `partial`, because private, draft, scheduled and custom-type articles remain unverified. For a local full export, `--complete-export` is an explicit operator attestation that the export includes all article statuses and the site's article post types. The WXR default includes `post` and `page`; set `--post-types` for relevant custom types. WordPress exports can be filtered, so merely receiving XML is not proof of completeness. See [WordPress export documentation](https://wordpress.org/documentation/article/tools-export-screen/).

Keep the attested export scope with the private import record. Conflicting duplicates or a count mismatch downgrade completeness. The importer does not deduce deletion from a missing row; reconcile removals only against a later confirmed complete snapshot.

After human-approved publication: WordPress → private Content Index → Search Console / GA4 raw observations → A07 strategy input. No scheduling, analytics connection, write endpoint, or publishing action is implemented here.

`inventory_view(existing_inventory, test_index)` provides a unified metadata query without changing either source. Each record carries `record_type: existing_wordpress | test_fixture`, its source index, all required nullable metadata fields, and candidate links separately from observed links. Counts expose `existing`, `test_fixtures`, and `total_records`; registering three tests therefore yields 0 / 3 / 3. A test fixture never receives a fabricated WordPress post ID. The [unified view schema](schemas/unified_content_view.schema.json) is independent of A07/A08 brief schema versions.
