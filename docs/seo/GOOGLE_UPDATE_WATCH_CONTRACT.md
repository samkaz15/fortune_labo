# Google Update Watch Contract

参照正本は [Google Search Policy](GOOGLE_SEARCH_POLICY.md)、[Google Update Register](GOOGLE_UPDATE_REGISTER.md)、[SEO Changelog](SEO_CHANGELOG.md)、[機械可読台帳](SEO_POLICY_REGISTER.json)。本契約は監視やSchedulingを開始しない。

`Google Update → Impact Assessment → Human Approval → SEO Policy Version → A06 / A07 / A08`

1. 公式一次情報の検出を更新候補として記録する。検出時点ではpolicyとWriting Ruleに書き込まない。
2. A06の外側のintegration adapterでsource ID、変更点、影響rule、対象記事、A06制約との衝突、移行・検証・復帰方法を整理する。既存A06の22ファイルは変更しない。
3. 人間は具体的な差分と適用範囲を承認する。Foundationの方向性承認やGoogle記事の検出をこの承認に置き換えない。
4. 承認記録を確認してから新versionとchangelogを登録する。旧versionを削除しない。自動昇格処理は提供しない。
5. A07はBriefに版とpolicy registerのhashを固定する。A08は同じ版とBrief hashをBlueprint、Draft manifest、Self Reviewへ運び、後段のA11画像plan・asset、QA、A25のjob・draft payloadも記事の版を引き継ぐ。過去記事の版は一括更新しない。

現在は `current_approved_policy=null`、`seo-policy-0.1.0-draft` のWordPress未公開のテスト範囲のみ。通常運用へのhandoffでは正式policy、上流A06、本文と画像のQAを確認する。追加指示により、WordPressはQA後にA25がdraftを作成し、その後で人間が公開を承認・操作する。Agentはdraft以外のpost statusを書き込まない。policy更新自体に必要な人間承認は引き続き維持し、記事の公開承認と分ける。
