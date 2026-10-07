# A07 → A08 Brief Contract

版: 1.0.0 / 状態: オフライン試作用、通常運用への接続は未承認

A07はContent IndexとContent Intelligenceを使って編集意図を定め、A08へ1記事1JSONのBriefを渡す。[a07_a08_brief.schema.json](schemas/a07_a08_brief.schema.json) が機械契約となる。既存の [A06 content_brief.schema.json](../../fortune_labo/agents/seo/schemas/content_brief.schema.json) は別の入力契約として保持し、変更も暗黙の読み替えもしない。

## 2つの入力状態

`mode=a06_handoff` は、A06既存スキーマで検証したContent Briefと承認済みSEO Opportunityを参照する通常経路。元JSONは参照先に残し、SEO要件を間引かない。通常経路には、人間承認情報を持ち、permitted_scopeが `editorial_production` の登録済みSEO方針が必要。このscope名は将来の契約値で、今回の台帳へそのような方針を登録・承認したものではない。`a06_source` に参照パス・ID・tier・content_path・visit_record_id・検証状態・不足一覧を記録する。保存先はリポジトリ相対パスとし、通常handoffで根拠ファイルを取得できない場合はreadyにしない。

`mode=offline_test` は、今回ユーザーが依頼した3本だけの非公開検証。A06の承認済み出力が存在しないため、`a06_source.status=not_issued`、参照・ID・tier・path・訪問記録はすべてnullとする。`handoff.state=offline_test_only`、`publication_allowed=false`、`human_approval=null`。検索需要・SERP差分・差別化をA06が検証したように装わない。

既存A06の「本人の体験・見解で差別化」「競合がAIだけで同じページを書けるなら提案しない」という要件に対し、今回の汎用相談整理・実践ワーク試作には未解消の差分がある。`strategy_assessment.moat_alignment=conflicting`、`strategy_review_status=pending` で記録し、ユーザーが依頼した編集工程の検証に限定する。正式採用、A06通過、Strategy承認、公開承認のいずれともみなさない。Tier DをA06へ新規提案する例外ではない。

## 必須データ

| フィールド | 用途 |
|---|---|
| `schema_version`, `content_id`, `mode`, `title`, `genre`, `topic` | 同一記事のIndex、根拠、Blueprint、Draftを結ぶ |
| `keyword`, `secondary_keywords`, `search_intent` | 主keyword・副keyword・intent。Indexのprimary_keywordはBriefのkeywordへ対応 |
| `explicit_need`, `latent_need`, `persona`, `reader_stage` | 何に答え、どこまで支援するか。原資料と編集仮説を混同しない |
| `access_type`, `access_rationale`, `core_answer`, `content_depth`, `article_type` | FREE/PREMIUMの根拠、先に返す回答、深さと形式 |
| `h2_h3_intent` | heading_level、heading、purpose、source_requirement、evidence_refs。H2/H3ごとの役割を明示 |
| `evidence_needed` | requirement、claim_kind、source_ref、status。6種類の主張分類と出典の有無 |
| `personal_experience_needed` | required、source_ref、status、handling。不要ならnot_required、必要なのに原資料がない場合はpending |
| `internal_link_candidates` | 未公開URLはnull。target_content_id、anchor_text、rationale、direction、candidate/verifiedを保持 |
| `cta` | type、destination、placement、copy_direction、status。未確認URLはnull、候補文言を実提供中のサービスと断定しない |
| `seo_policy_version` | 記事に適用したGoogle SEO方針の版 |
| `a06_source`, `strategy_assessment` | 元契約と差分・未承認事項の明示 |
| `source_refs`, `source_status` | 調査の出典と、ユーザー調査の構造化かA06検証済み入力かの区別 |
| `handoff`, `human_approval`, `publication_allowed`, `tbd` | 次工程、承認状態、実行範囲、不足事項 |

evidence_neededは最低1項目を記録する。対象となる事実主張がない場合も理由をnot_applicableで残し、必要な根拠を配列ごと削除しない。availableにはsource_refを必須とし、人間の素材が必要な見出しにはevidence_refsを1件以上付ける。

`evidence_needed.claim_kind` は FACT/FORTUNE_INTERPRETATION/TRADITION/PERSONAL_EXPERIENCE/PERSONAL_OPINION/HYPOTHESIS。仮の具体例はHYPOTHESISとし、実在する顧客・筆者体験として書かない。`PERSONAL_EXPERIENCE` は人間の原記録と本人確認なしにavailable/verifiedへ進めない。`source_requirement=practitioner_judgment` は人間の見立てとその根拠、`visit_notes` は実訪問記録が必要。AIが補筆して事実を作る権限はない。

## A06からの明示的な対応

| 既存A06の項目 | 新Brief/Indexの対応 | 欠損時の扱い |
|---|---|---|
| id / opportunity_id | a06_source.brief_id / opportunity_id | 通常入力は必須。今回の試作はnull |
| tier / content_path / visit_record_id | a06_sourceの同名項目 | 推測でA/B/Cへ分類しない。訪問系は原記録がなければ発行不可 |
| keyword / secondary_keywords / search_intent | keyword / secondary_keywords / search_intent | primary_keywordはIndex側の名前。secondary_keywordsの省略既定値は[] |
| target_audience | persona | 必要ならreader_stage等へ拡張するが元の意味を保持 |
| working_title / article_type | title / article_type | A06の8種類を保持し、新形式は無断追加しない |
| outline.heading_level / heading / purpose / source_requirement | h2_h3_intentの同名項目 + evidence_refs | A06スキーマ上source_requirementが省略可能でもプロンプトは必須。欠ければ不足として差し戻す |
| internal_links | internal_link_candidates | 既知のURL・anchor・rationale・directionを保持。URL不明を架空URLで埋めない |
| cta.type / placement / copy_direction | ctaの同名項目 + destination/status | A06にないfree_fortune/member_registration/premiumを既存bookingへ読み替えない。通常運用への採用は再Brief化が必要 |
| compliance_requirements | 元A06 JSONを保持しA29/A28へ引き継ぐ | Disclaimer、主観表示、占術根拠、写真許可の要件を削除しない |
| required_topics / serp_gap / differentiation_basis | 元A06 JSONを保持しBlueprintとQAへ引き継ぐ | 調査なしにSERP gap・独自性を作らない |
| meta_description / structured_data / target_length / publish_by / priority | 元A06 JSONを保持し担当工程へ引き継ぐ | 現Briefから落ちて見えても失効しない。publish_byは予定日で、Indexのpublish_dateへ転記不可 |
| A06にないexplicit_need / latent_need / genre / access_type / core_answer / content_depth等 | Content Intelligence・IndexをもとにA07が追記 | 既存A06にある項目だと偽装しない。出典または編集仮説を示し、不明はTBDとして通常readyを止める |

A06の `moat_alignment` はContent BriefスキーマではなくSEO Opportunityの項目なので、Opportunityも保持・検証する。Opportunityの非nullのtier・keyword・search_intentとContent Briefの同名項目を照合し、A07のmoat評価も一致させる。A06のenum制約を広げるために既存ファイルを編集しない。元要件とA07の追記が衝突したときは、上流の訂正版を受け取るまで通常handoffをblockedとする。

## A08の受入と返却

1. JSON Schema、Indexとの同一性、genre、方針版、上流参照を検証する。
2. 通常経路は承認済みOpportunity、非conflicting、解消済みcompliance flags、A06の全必須要件、visit record、根拠とTBDを確認する。スキーマ適合だけで記事採用を承認しない。
3. A08はBlueprintで回答順・根拠・段落の展開・FREE/PREMIUM差・CTA位置を具体化する。元資料がない体験や人物見解は補わない。
4. DraftとClaim台帳を返し、A29相当の事実確認、A32相当の編集レビュー、A28相当のQAを順に記録する。これは今回の担当工程の実施記録であり、実在する人間が各役割をレビューしたという表示ではない。
5. `Draft → A29 → A32 → A28 → Human Approval → A25 WordPress Draft`。各段階で元要件と残課題を引き継ぐ。A25へのhandoffやWordPress書き込みは今回実行しない。

工程成果物は非公開の実行領域に保存し、公開Repositoryには本文をコピーしない。公開Schemaは構造の契約であり、サンプル本文の保存を要求しない。試作QAを終えても、正式SEO方針・Strategy差分・URL・計測・人間承認が未確定なら公開可にしない。

## 未確定と変更管理

通常運用の承認済みA06 Opportunity/Brief、genre別のA06 tier分類、本人の独自見解・実体験、FREE鑑定/会員/PremiumへのCTA拡張承認、実リンク、料金/商品仕様、担当人間と承認方法はTBD。契約破壊を伴う変更はschema_versionを更新し、A06/A07/A08とA28で再検証する。今回の3件をそのまま通常経路へ変更する自動migrationは作らない。
