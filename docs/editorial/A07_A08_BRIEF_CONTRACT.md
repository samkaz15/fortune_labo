# A07 → A08 Brief Contract

現行のAgent仕様は [A07](../../fortune_labo/agents/content-strategy/README.md) と [A08](../../fortune_labo/agents/content-production/README.md)。機械契約はA07の [Brief v2](../../fortune_labo/agents/content-strategy/schemas/brief.schema.json) とA08配下のschemas。旧 [v1](schemas/a07_a08_brief.schema.json) は履歴用として保存し、今回のv2へ読み替えない。既存A06を変更しない。

A07はA06、統合Content Index、Content Intelligence、raw Performance、Content Opportunityを読み、モデルまたは担当者が次の制作対象と理由を決める。Python helperは判断を検証し、Briefへ組み立てる。keyword需要、事業方針、未知の値をコードで捏造しない。ジャンル、topic、keyword、search intent、explicit/latent need、persona、FREE/PREMIUM、depth、core answer、evidence/personal experience requirement、link候補、CTA、policy versionを必須化する。

FREE/PREMIUMはContent IntelligenceとFREE_PREMIUM_RULESを根拠にし、acquisition / engagement / conversion / retention / premium valueを保存する。基本回答の欠落を拒否し、PREMIUMには具体的追加価値、value dimension、参照可能な出典を要求する。FREEのpremium valueはnull。文字数だけの有料判定は不可。

今回の3本はユーザーが選定したoffline_testで、A06の採用済みOpportunity/Briefは発行されていない。元A06の独自性・本人素材・予約導線との差分はpendingで残す。通常のA06 → A07運用は、上流の各schema、採用、全要件の対応と正式policyを別途確認する必要がある。実行helperはその承認を作らず、今回のoffline範囲に限定する。

A08はBriefを変更せず、Blueprint、Writing Source of Truthのsnapshot、Draft、Self Reviewを作る。Brief・Blueprint・rule・prompt・Draft・reviewのSHA-256を保持し、変更や再上書きを拒否する。文章はモデル／担当者が作成し、helperが外部に記事を自動生成・公開するものではない。

今回の [3Fixture](test-content-index.json) は明示許可を受けてGitHubへ保存する。実行の作業領域はprivateを既定とし、公開へ出すのはmanifestで選んだ今回の生成物だけ。原文、旧Draft、私的なURLはコピーしない。

次段階は [QA Contract](QA_HANDOFF_CONTRACT.md) のA29 → A32 → A28 → Human Approval → A25 WordPress Draft。相当するモデルレビューと機械検査を記録しても、本体実装・人間承認・WordPress操作の実行済みとは表示しない。公開可能フラグはfalseのままとする。

[Google Update Watch Contract](../seo/GOOGLE_UPDATE_WATCH_CONTRACT.md)に従い、更新検知だけでWriting Ruleや既存Briefを変えない。policy版とinput hashを各工程へ引き継ぐ。
