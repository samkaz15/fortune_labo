# Content Index

既存の公開・下書き記事と、今回生成したFixtureを区別して把握する。ユーザー確認により既存記事は0件。WordPressへの接続・Importは実行していない。

## 保存構造

| 保存先 | 件数・用途 | 契約 |
| --- | --- | --- |
| [existing-content-index.json](existing-content-index.json) | 既存0件。取得範囲、完全性、確認根拠を保持 | [existing_content_inventory.schema.json](schemas/existing_content_inventory.schema.json) |
| [test-content-index.json](test-content-index.json) | 今回許可されたtest_draft 3件。WordPress ID・URL・公開日はnull | [test_content_index.schema.json](schemas/test_content_index.schema.json) |
| [unified-content-view.json](unified-content-view.json) | 既存0 / Fixture3 / 合計3を区別した参照用metadata | [unified_content_view.schema.json](schemas/unified_content_view.schema.json) |

`inventory_view(existing_inventory, test_index)`で統合viewを再作成できる。実記事が増えた後のIndex・本文・source URL・provider IDは非公開保存に戻す。公開Repositoryへの許可は現時点の空の既存Indexと、今回の3Fixtureだけである。

取得するmetadataは content_id、wordpress_post_id、title、slug、url、status、publish_date、modified_date、category、tags、genre、subgenre、topic_cluster、access_type、primary_keyword、secondary_keywords、search_intent、explicit_need、latent_need、article_type、content_depth、cta_type、cta_destination、internal_links、featured_image、word_count、seo_policy_version。未知の値はnullを保持し、ジャンル候補はunclassifiedも使える。分類候補ができても元の観測値を上書きしない。

WordPress側のIDにsite namespaceを付け、slug・title変更でもcontent_idを維持する。Fixtureには別の固定IDを使う。word_countは日本語をCJK文字、欧文を語tokenとして数えた手法名を併記し、日本語の形態素解析による語数とは混同しない。公開予定日をpublish_dateへ入れない。リンク候補は観測済みの実リンクと別欄にする。

## 取込・分類・機会

[Importer](EXISTING_CONTENT_IMPORT.md)はWXR、REST JSON、GET限定ページングに対応する。公開APIで非公開状態の全件まで取得したとは判断しない。[分類](EXISTING_CLASSIFICATION.md)は根拠とconfidenceを持つ候補を返し、lowはHuman Reviewへ渡す。[Opportunity](CONTENT_OPPORTUNITY_INDEX.md)は明示topicとIndexを比較し、取得範囲や意味上の重複確認を保持する。scoreは作らない。

## Performanceから次の企画へ

`WordPress → Content Index → Search Console / GA4 / WordPress / SNS raw observations → A07`

新しい実測値は [Performance Schema](PERFORMANCE_SCHEMA.md) に保存する。17指標は未計測ならnull。期間・timezone・filter・母集団・定義版・source provenanceを維持し、異なる条件の数字を混ぜない。scroll_depthは新raw契約で0〜100のpercent、CTRとengagement_rateは0〜1のratio。総合scoreやweightはない。

Fixtureのgrouped performanceは全値nullの未計測表現に限定する。旧 [content_index.schema.json](schemas/content_index.schema.json) はv1の履歴契約であり、今後の実測保存には使わない。旧scroll_depthのratioから新percentへの暗黙変換は行わない。

## 検証

```sh
python3 -B scripts/validate_editorial.py --schemas-only
python3 -B scripts/verify_test_fixtures.py
python3 -B -m unittest discover -s tests -v
```

通常の公開はA06採用、正式policy、A29/A32/A28、記事別の人間承認が揃うまでblocked。schemaへの適合は公開承認ではない。
