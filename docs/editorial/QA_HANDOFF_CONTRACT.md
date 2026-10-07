# A29 / A32 / A28 QA Contract

A29、A32、A28のAgent本体は今回実装しない。この契約と検査用helperは、各担当へ不足を含めて渡すためのもので、担当Agentや人間が承認済みだと表示するものではない。

追加指示を反映した受け渡し順は `A06 → Content Index → A07 → A08 → A11 → A29 Fact Check → A32 Editorial → A28 QA → A25 WordPress draft → Human Approval → Human publish`。記事の人間公開承認は下書き作成後に置く。QA完了前の下書き作成やAgentによるpublishを許す変更ではない。詳細は [Article Creative Pipeline](ARTICLE_CREATIVE_PIPELINE.md) を参照する。

## 共通Envelope

`qa_handoff.schema.json`に従い、content_id、変更禁止BriefのSHA-256、DraftのSHA-256、seo_policy_version、不透明なartifact ID、各段階のstatusとfinding、未解決blockerを渡す。A11以降のjobではimage plan、asset provenance、画像hash、alt、配置、画像QAの結果も記事hashへ結び付ける。A08のSelf ReviewはA32の承認を兼ねない。実体験の原記録や実記事入力は非公開ストレージで扱う。

| 担当 | 入力 | 確認と返却 |
| --- | --- | --- |
| A29 | Brief、Draft、主張抽出候補、evidence_needed、画像内の主張とprovenance | FACT / FORTUNE_INTERPRETATION / TRADITION / PERSONAL_EXPERIENCE / PERSONAL_OPINION / HYPOTHESISを区別。画像の架空例と実写を混同せず、出典の支持範囲・日付・原記録を確認。不明な主張は未検証として返す |
| A32 | A29結果、Brief、Draft、Writing Source of Truth、画像と配置・alt | Search Intent、日本語の自然さ、段落、断片化、具体性、FREE/PREMIUM差、CTA、リンク、画像との整合を確認。Brief変更が必要ならA07へ返却 |
| A28 | A29 / A32結果、A11画像QA、immutable hash、policy register、job | 必須artifact、上流採用、参照先、policy、画像状態、draft専用payloadを照合。pending / unresolvedがあればblockerを返す |
| A25 | QAを満たす一式、指定先、認証 | draftだけを作成する。payload生成と実upload・draft作成の成功を区別する |
| Human Approval | WordPress上の具体的な最終下書き・画像・差分・QA findings | 対象、判断、担当人間、日時、承認記録を固定。AIが承認者を創作しない |
| Human publish | 承認した具体的な下書き | 人間が公開を操作する。Agentにはpublish操作を設けない |

`contract_pending`、`candidate_review_only`、`changes_requested`、`verified`を区別する。担当役相当のモデルレビューを、未実装Agentの実行完了やhuman passとして記録しない。既存の `qa_contract.py` helperは未実装・未解決の契約を作るため、引き続き `wordpress_handoff_allowed=false`、`publication_allowed=false` を返す。このhelperのfalseを、後段を追加しただけでtrueへ書き換えない。

新しいWordPress adapterで、QAを実際に満たしたjobをdraftにする場合、人間公開承認は前提にしない。一方、Agentには承認の有無にかかわらずpublishを許さない。policy更新の人間承認と記事公開の人間承認を混同しない。

主張抽出とAIらしさの検査は候補検出であり、網羅性・真偽・自然さの証明ではない。数値や強い断定の単純検査で拾えない主張も全文確認対象となる。画像生成の成功は画像QAの完了ではない。小さなQAスコアを合計して100点評価にする処理は作らない。
