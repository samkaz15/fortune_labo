# Content Index仕様

版: 1.0.0 / 状態: Editorial基盤の提案 / 更新: 2026-10-07

記事の目的・制作状態・根拠・実績を、1記事1レコードで管理する。実レコードの保存先は非公開の実行領域。公開する機械仕様は [content_index.schema.json](schemas/content_index.schema.json)。既存のWordPress記事台帳を取得できていないため、実記事の件数を未取得として扱い、「既存公開記事は存在しない」とは判断しない。

## 保存形式と識別

ルートは `schema_version`、`updated_at`、`items`。`schema_version` は現在 `1.0.0`、`updated_at` は台帳更新日。`items` の全項目と下記のキーは省略不可。不明な値は許可された `null` と `tbd` の理由で表し、未測定をゼロへ変換しない。`[]` は「確認した結果、要素がない」または「候補未登録」であり、その違いは `tbd` に残す。

`content_id` は不変の `FL-*` IDで、タイトル・slugが変わっても再採番しない。試作IDと既存WordPressのIDは別管理とし、試作を既存記事の件数に加えない。同じ記事の無料版・有料版を別ページとして制作するなら別IDにする。公開済みURLは公開側の記録で確認し、公開前は `url` と `publish_date` を `null` にする。予定日を実公開日に流用しない。`slug` は候補として保存できるが、URLや公開予約の確定を意味しない。

## 必須フィールド

| 項目 | 型・値 | 運用上の意味 |
|---|---|---|
| `content_id`, `title`, `slug`, `url`, `status`, `publish_date` | ID、文字列、nullable slug/URL/date、状態 | `status` は下表。dateは `YYYY-MM-DD` |
| `genre`, `subgenre`, `topic_cluster` | taxonomyのID、nullable文字列 | genreは [genre-taxonomy.json](genre-taxonomy.json) を参照。subgenre未定はnull |
| `primary_keyword`, `secondary_keywords`, `search_intent` | nullable文字列、配列、nullable enum | intent: informational/navigational/commercial/transactional/local。根拠のない検索需要は測定済みにしない |
| `explicit_need`, `latent_need`, `persona` | nullable文字列 | 原資料の事実とA07の編集上の仮説をBriefで区別 |
| `reader_stage` | discovery/understanding/consideration/action/continuation/null | 読者の現在地。未調査はnull |
| `access_type` | FREE/PREMIUM | BOTHはジャンルの推奨値であり1記事の権限には使わない |
| `content_depth` | short/standard/deep | 長さではなく回答範囲・判断材料・実践支援の深さ |
| `article_type` | A06の8種類 | shrine_visit_report/annual_outlook/forecast_review/method_explainer/situation_guide/practitioner_profile/service_page/hub_page |
| `cta_type`, `cta_destination` | enum、nullable絶対URL | booking/list_signup/related_content/free_fortune/member_registration/premium/none。未確認の鑑定ページ等はURLを作らずnull |
| `internal_links` | 候補オブジェクト配列 | target_content_id、target_url、anchor_text、rationale、direction、status。未公開対象はURLをnullにしcandidateにする |
| `featured_image_type` | none/original_photo/illustration/diagram/text_graphic/TBD | original_photoでも利用権確認済みとは限らない |
| `fact_check_status` | pending/in_progress/reviewed/reviewed_with_gaps/blocked | `reviewed`は現実世界の全主張を保証する意味ではない。根拠と保留箇所はClaim台帳へ |
| `editorial_status` | pending/in_progress/reviewed/changes_requested | 編集自己レビューを実施しても人間承認は別 |
| `qa_status` | pending/in_progress/passed/passed_with_blockers/blocked | 今回は試作QAの完了と公開ブロックを併記できる |
| `seo_policy_version` | seo-policy-X.Y.Z または末尾-draft | 適用した版を固定。後日方針が変わっても過去の記事値を自動置換しない |
| `performance` | 下記の4群 + measurement | Raw metricの保管のみ。合算や重み付けなし |
| `source_refs` | 根拠のパス・URL・出典IDの配列 | 少なくとも1件。Briefの出典箇所へ遡れるようにする |
| `artifacts` | 6つのnullableパス | brief/blueprint/draft/fact_claims/editorial_review/qa_report。試作完了時には全6件を実ファイルで埋める |
| `human_approval` | nullまたは承認記録 | 実際の人間の判断が来るまではnull。approved_by/approved_at/decision/scope/evidence_refが必須 |
| `release_gate`, `tbd` | blocked/awaiting_human_approval/approved、未確定配列 | QA通過から自動でapprovedへ変えない |

## 状態と承認

`planned → briefed → drafting → qa_pending → human_review → approved → published` が将来の通常経路。`test_draft` は今回のオフライン試作状態、`archived` は記録保全用。状態変更は担当者が証跡を確認して行い、スキーマ適合だけで次状態へ遷移させない。plannedは工程成果物をnullで登録できる。briefedはBrief、draftingはBriefとBlueprint、qa_pendingはさらにDraftが必要。test_draft（今回の試作完了）、human_review、approved、publishedは全6成果物を必須とし、存在する参照先を常に確認する。

`test_draft` では `url=null`、`publish_date=null`、`human_approval=null`、`release_gate=blocked` を必須とする。`approved` と `published` は人間承認記録、事実確認・編集レビューの完了、QA通過、通常経路のready Briefを必要とする。公開済みには実URL・実公開日も必要。`archived` の過去の公開情報は消さず保持できる。スキーマは承認記録の形を検証するが、承認した人物や記録の真実性を認証する仕組みではない。A28と人間が証跡を照合する。

非公開の試作は `test_draft` のまま終了する。次工程の `A25 WordPress Draft` への移行も今回の実行範囲外である。

## Performance: 目的別に分離する

| 群 | 必須メトリクス | 単位・定義 |
|---|---|---|
| `seo` | impressions, clicks, ctr, average_position | impressions/clicksは非負整数、ctrは0–1、average_positionは1以上。GSCで取得した同じ期間・条件を保存 |
| `engagement` | users, sessions, engaged_sessions, engagement_rate, average_engagement_time, scroll_depth | 件数は非負整数。rateとscroll_depthは0–1。timeは秒。timeの分母とscroll_depthの集計方法は定義確定までnull |
| `conversion` | fortune_cta_clicks, fortune_start, fortune_complete, member_registration, premium_conversion | 非負整数。イベント発火の成立条件、重複排除、記事への帰属は未確定。無料鑑定の完了と予約完了を同一視しない |
| `retention` | returning_users, repeat_article_views | 非負整数。再訪の識別期間、同一記事の再閲覧定義、重複排除は未確定 |

全メトリクスは `null` を許可し、未公開・未計測・イベント未実装をそのまま表す。`0` は計測対象として観測した結果がゼロのときだけ使う。例えば `ctr=0.05` は5%であり、`5`を入れない。重み・総合スコア・PVだけの勝敗判定を保存するキーは設けず、未知のプロパティは拒否する。

`performance.measurement` は `window_start`、`window_end`、`collected_at`、群別 `source`、`definition_version`、`notes` を持つ。期間は両端を含む日付、時刻はタイムゾーン付きRFC 3339。実数が1つでもある群はソースを必須とし、期間・収集日時・承認された定義版を伴わせる。集計対象・タイムゾーン・フィルタ・計測不能理由はnotesへ。異なる期間や母集団の値を同じレコードに混在させない。複数期間の履歴保存が必要になる段階で、別の計測テーブルを設計する。

既存A06にはkeyword優先順位の重み・スコアがある。これは取得済み指標を評価する本台帳のperformanceとは別仕様であり、今回変更しない。既存A06の予約中心KGI、一次体験・権威指標も維持する。本台帳の無料鑑定・会員・Premium指標を予約KGIの代替として扱わず、A18/A26/Strategyがイベント・帰属・評価目的を整理するまで仮説として運用する。

## 検証と未確定事項

リポジトリルートで以下を実行する。外部接続や公開処理は行わない。

```sh
python3 -B scripts/validate_editorial.py --schemas-only
```

JSON SchemaはDraft 2020-12。付属スクリプトは使用中のキーワードだけを実装した標準ライブラリ検証器で、汎用の完全実装ではない。未知のスキーマキーワードは無視せず拒否する。型・必須項目・enum・範囲・日付・ローカル参照・条件分岐に加え、ID重複、genre、Index/Brief整合、工程成果物の存在、SEO版、試作の未公開・未計測状態を検証する。文章の正しさ、出典の信頼性、実体験、人間承認は別途QAする。

既存公開記事一覧、本番slug規則、公開先ドメイン、鑑定・登録・Premiumの実在ページ、画像権利、計測イベントと分母、機械的な履歴保持方法、正式に承認されたSEO版はTBD。記事生成のために補完して事実化しない。
