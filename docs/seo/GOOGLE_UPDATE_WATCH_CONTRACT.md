# Google Update Watch Contract

参照正本は [Google Search Policy](GOOGLE_SEARCH_POLICY.md)、[Google Update Register](GOOGLE_UPDATE_REGISTER.md)、[SEO Changelog](SEO_CHANGELOG.md)、[機械可読台帳](SEO_POLICY_REGISTER.json)。本契約は監視やSchedulingを開始しない。

`Google Update → Impact Assessment → Human Approval → SEO Policy Version → A06 / A07 / A08`

1. 公式一次情報の検出を更新候補として記録する。検出時点ではpolicyとWriting Ruleに書き込まない。
2. A06の外側のintegration adapterでsource ID、変更点、影響rule、対象記事、A06制約との衝突、移行・検証・復帰方法を整理する。既存A06の22ファイルは変更しない。
3. 人間は具体的な差分と適用範囲を承認する。Foundationの方向性承認やGoogle記事の検出をこの承認に置き換えない。
4. 承認記録を確認してから新versionとchangelogを登録する。旧versionを削除しない。自動昇格処理は提供しない。
5. A07はBriefに版とpolicy registerのhashを固定する。A08は同じ版とBrief hashをBlueprint、Draft manifest、Self Review、QAへ運ぶ。過去記事の版は一括更新しない。

現在は `current_approved_policy=null`、`seo-policy-0.1.0-draft` のWordPress未公開のテスト範囲のみ。通常運用へのhandoffは正式policy、上流A06、記事別QA、人間承認をそれぞれ確認してから行う。
