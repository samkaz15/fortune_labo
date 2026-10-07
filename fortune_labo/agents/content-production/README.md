# A08 Content Production Agent

後段への追加経路は [Article + Creative Pipeline](../../../docs/editorial/ARTICLE_CREATIVE_PIPELINE.md) を参照。A08の本文・Briefは変更せずA11へ渡し、新しいJobが画像・QA・A25 draftを管理する。旧runのhandoff snapshotは履歴として保持する。

A08はA07 Briefを変更せず、Article Blueprint → Draft → Self Reviewを作る。[ARTICLE_PRODUCTION_RULES](../../../docs/editorial/ARTICLE_PRODUCTION_RULES.md) がWritingの正本。現行policyの適用範囲と未確定事項を保持し、公開許可を生成しない。

[inputs](inputs.md)、[rules](rules.md)、[workflow](workflow.md)、[outputs](outputs.md) と [draft prompt](prompts/draft.md) を使用する。schemaはBlueprint/Self Review/run manifest、実行補助は `fortune_labo/editorial/production.py`。文章の生成は外部のモデルまたは担当者が行い、コードはテンプレート文を実記事として偽装しない。

private runを作り、Brief・Blueprint・Writing正本snapshot・prompt・Draft・Self Reviewのhashで工程を追跡する。今回許可されたFixtureのGit保存は別の検査付きexport工程であり、A08がpublic出力先を直接書く権限ではない。
