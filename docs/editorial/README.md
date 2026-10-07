# Editorial Intelligence Foundation

編集基盤の方向性は承認済み。公開Repositoryには要約されたInsight、分類・制作ルール、Schema、Provenanceと、この依頼で認められた実装を保存する。非公開原資料、実記事の本文・入力データ、テスト記事の本文は公開対象にしない。

| Foundation | 内容 |
| --- | --- |
| [Article Production Rules](ARTICLE_PRODUCTION_RULES.md) | Writing Source of Truth、日本語、主張分類、QA工程 |
| [Content Intelligence](CONTENT_INTELLIGENCE.md) / [JSON](content-intelligence.json) | ジャンル別の編集上の要約 |
| [Genre Taxonomy](GENRE_TAXONOMY.md) / [JSON](genre-taxonomy.json) | 固定IDを持つ11ジャンル |
| [FREE / PREMIUM Rules](FREE_PREMIUM_RULES.md) | 根拠のあるアクセス区分の候補決定 |
| [Content Index仕様](CONTENT_INDEX_SPEC.md) / [Schema](schemas/content_index.schema.json) | 既存記事を把握する台帳の契約 |
| [A07 / A08契約](A07_A08_BRIEF_CONTRACT.md) | 戦略から制作への引き継ぎ |
| [Provenance](sources/provenance.json) | 非公開Sourceへの不透明な参照 |
| [Public Export Policy](PUBLIC_EXPORT_POLICY.md) | 公開対象の許可リストと漏えい検査 |
| [Google Search Policy](../seo/GOOGLE_SEARCH_POLICY.md) / [Update Register](../seo/GOOGLE_UPDATE_REGISTER.md) / [Changelog](../seo/SEO_CHANGELOG.md) | 影響評価・人間承認・version管理 |
| [Implementation Notes](IMPLEMENTATION_NOTES.md) / [QA Report](QA_REPORT.md) | 実装範囲、未確定事項、検査記録 |

通常の受け渡し順は `A06 → Content Index → A07 → A08 → A29 → A32 → A28 → Human Approval → A25 WordPress Draft`。A29/A32/A28の本体が未実装ならQA Contractとして扱う。A07は根拠を含むBriefを作成し、A08はBriefを変更せずBlueprint、Draft、Self Reviewを作成する。

記事の非公開テストとFoundation承認は、正式SEO policy、A06の個別採用、商品化、記事公開の承認を兼ねない。WordPress書込・自動公開・SNS投稿・大量生成・自動Scheduling・Performance Scoreは今回の対象外である。
