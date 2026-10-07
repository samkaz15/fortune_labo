# Editorial Foundation QA Report

本書は公開可能な構造とルールの検査記録である。非公開Sourceや記事本文は含めない。今回のFoundation承認は、記事公開・商品提供・SEO policyの承認ではない。

## 公開範囲の検査

- 11ジャンルの固定IDと短い要約を保持した。
- 非公開Sourceの本文、URL、文書識別子、詳細位置情報、調査数値・順位を公開Foundationから除いた。
- Provenanceは不透明なSource ID、一般名、種類、アクセス範囲、派生ファイルだけを持つ。
- テスト記事と実データの本文は公開対象から除外した。
- Article Production RulesをWriting Source of Truthとして維持し、A08によるBrief変更を禁止した。
- A06、SEO policy承認、WordPress公開権限をFoundation承認から分離した。

再現可能な公開検査は [Public Export Policy](PUBLIC_EXPORT_POLICY.md) を参照する。後続のImporter、分類、A07/A08、QA引き継ぎの結果は実行時レポートで確認する。以前の検査件数を、変更後の新しい実装が合格した証拠には使わない。

## 判定限界

機械検査は構造・整合性・禁止パターンを検査するもので、文章の自然さ、事実の真偽、取得範囲の網羅性、人間本人の承認を保証しない。未取得のPerformance値はnullとし、未接続の値をゼロに置き換えない。総合100点Scoreや重みは作成しない。

本番への受け渡しにはA29 Fact Check、A32 Editorial、A28 QAの各契約と、人間による対象記事への明示的な承認が必要である。
