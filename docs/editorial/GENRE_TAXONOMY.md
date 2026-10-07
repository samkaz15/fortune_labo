# Genre Taxonomy

Version: 0.2.0。分類基盤の方向性は承認済み。公開メニューや商品展開の確定を意味しない。

[機械可読版](genre-taxonomy.json) は次の11識別子を保持する。各分類の編集上の要約は [Content Intelligence](CONTENT_INTELLIGENCE.md)、根拠は [Provenance](sources/provenance.json) の `GR001` に結び付ける。

| genre_id | 表示名 |
| --- | --- |
| general_fortune | 総合運・月運 |
| love | 恋愛 |
| marriage | 結婚 |
| career | 仕事・キャリア |
| money | 金運 |
| health_lifestyle | 健康・生活習慣 |
| self_understanding | 自己理解・才能 |
| shrine_visits | 神社・参拝 |
| direction_travel_moving | 方位・旅行・引越し |
| compatibility | 相性 |
| spiritual_consultation | 霊視・個別相談 |

記事の中心的な問いに対応する主分類を一つ選ぶ。複数の課題が含まれる場合は、分類候補と確信度を保持し、同じ記事を複数の独立記事として数えない。`genre_id` は表示名の変更から独立した固定IDである。

正式な `subgenre` と `topic_cluster` は未確定。根拠のない値はnullまたは `unclassified` にする。分類候補に `high / medium / low` のconfidenceを付け、lowはHuman Reviewへ回す。候補生成だけで既存本文・公開カテゴリ・アクセス制限を変更しない。

ジャンルごとの `BOTH` はFREEとPREMIUMの両方を検討できるという意味で、記事単位の決定ではない。既存記事の実際のアクセス区分と、ルールに基づく候補を別フィールドに保存する。恋愛・結婚・相性、神社・方位を便宜的に統合しない。

分類として保持した題材でも、通常制作は既存A06のTier、独自性、実体験要件を満たす必要がある。一般運勢や無料占いを自動で採用する許可にはならない。
