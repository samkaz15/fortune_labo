# Implementation Notes

対象: `samkaz15/fortune_labo`。作業日: 2026-10-07。Editorial Intelligence Foundationの方向性と専用branchでのDraft PR作成はユーザー承認済み。mainへのmergeは行わない。

公開Foundationは短い要約、11ジャンルのTaxonomy、FREE/PREMIUMと制作ルール、Schema、Source Referenceで構成する。非公開資料の本文・URL・文書ID・取得時のrevision・個人情報・調査上の数値や順位はコピーしない。公開ProvenanceはSource ID、種類、一般名、privateというアクセス範囲、派生成果物だけを持つ。

既存A06の仕様・スコア式・Tier・独自性・実体験要件は維持する。Foundationの方向性の承認を、既存A06の変更承認、正式SEO policyの承認、個別記事の本番採用に読み替えない。

今回、既存記事は0件とユーザーが確認したため、実サイトへのImporter実行は不要とする。0件の状態はユーザー確認によるもので、WordPress全件取得の成功として記録しない。今後の既存記事の台帳は提供された実データまたはread-only取得結果から作成する。全件取得を確認できない場合は、取得件数と未取得範囲を区別する。原文を書き換えず、分類候補を実データの値から分離する。追加指示でGitHub Draft/Fixture保存を許可された今回のA07/A08生成3本を、既存記事の実件数に含めない。

## 未確定事項

| 項目 | 必要な確認 |
| --- | --- |
| 正式SEO policy | 影響評価への人間承認、承認者、日時、version |
| A06の採用判断 | 検索意図、Tier、独自素材、鑑定者への導線 |
| 将来のImport範囲 | 現時点はユーザー確認で0件。記事が増えた後に対象サイト・投稿種別・権限・全件数を照合 |
| subgenre / topic_cluster | 正式分類と分類根拠 |
| 商品・CTA | 実際の提供範囲、遷移先、利用条件 |
| 著者・事実・実体験 | 本人からの素材、出典、利用許可 |
| Performance | データ接続、期間、母数、イベント定義、帰属 |

QA完了後は上記を人間が確認する。今回の実装からWordPressやSNSへの書込・公開・自動実行には進まない。Googleの更新は検出後に影響評価と人間承認を必要とし、制作ルールを自動で変更しない。
