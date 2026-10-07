# Outputs

出力は`proposed_payload`, `request_payload`, `media_upload_plan`, `inline_media`, `editorial_metadata`, `seo_metadata`, `qa_reference`, source/rendered/package hashes、readiness/blockersを含む。実WordPress IDは作成前にはnull。`network_ready`と`publication_allowed`は常にfalse。

| WordPress field | 内容 |
| --- | --- |
| status | draftのみ |
| title / content | H1の正式titleと、A08 Markdownから決定的に整形したHTML |
| excerpt / slug | 確定値、未知はpreviewでnull |
| categories / tags | 実term ID配列。`category`等の独自aliasを直接送らない |
| featured_media | upload/取得responseのattachment ID。未取得はnull |
| meta | 登録確認済みキーへの明示mappingのみ。初期状態は空object |

`request_payload`はQAとmedia準備が全て揃うまでnull。揃った場合はpreviewのnull fieldsを省略し、意図しないWordPress defaultを既知のmetadataとして記録しない。

inline画像のalt/captionはmedia metadataとHTML figureに保持する。未uploadのinline画像はpreview内のpending commentだけで位置を示し、公開可能な画像と装わない。内部リンク・CTAは本文内の既存記述を保ち、構造化候補もsidecarへ残す。候補URLを本文へ自動追記しない。

editorial sidecarはcontent ID、FREE/PREMIUM、SEO policy版、article版、visual style版、fact/QA status、source hashを保持する。SEO pluginやmembership pluginの互換性は仮定しない。
