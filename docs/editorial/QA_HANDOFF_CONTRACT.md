# A29 / A32 / A28 QA Contract

A29、A32、A28のAgent本体は今回実装しない。この契約と検査用helperは、各担当へ不足を含めて渡すためのもので、担当Agentや人間が承認済みだと表示するものではない。

`A06 → Content Index → A07 → A08 → A29 Fact Check → A32 Editorial → A28 QA → Human Approval → A25 WordPress Draft`

## 共通Envelope

`qa_handoff.schema.json`に従い、content_id、変更禁止BriefのSHA-256、DraftのSHA-256、seo_policy_version、非公開artifactの不透明なID、各段階のstatusとfinding、未解決blockerを渡す。A08のSelf ReviewはA32の承認を兼ねない。実体験の原記録や取得記事本文は非公開ストレージで扱う。

| 担当 | 入力 | 確認と返却 |
| --- | --- | --- |
| A29 | Brief、Draft、主張抽出候補、evidence_needed | FACT / FORTUNE_INTERPRETATION / TRADITION / PERSONAL_EXPERIENCE / PERSONAL_OPINION / HYPOTHESISを区別。出典の支持範囲・日付・原記録を確認。不明な主張は未検証として返す |
| A32 | A29結果、Brief、Draft、Writing Source of Truth | Search Intent、日本語の自然さ、段落展開、断片化、具体性、アクセス区分差、CTA、リンクを確認。Brief変更が必要ならA07へ返却 |
| A28 | A29 / A32結果、immutable hash、policy register | 必須artifact、上流採用、参照先、承認範囲を照合。pending / unresolvedがあればblockerを返す |
| Human Approval | 具体的な最終本文・差分・QA findings | 対象hash、判断、担当人間、日時、承認記録を固定。AIが承認欄を作って埋めない |
| A25 | 承認後の一式 | 別途指定されたWordPress Draftの書込み範囲のみ。公開は別の明示承認を要する |

`contract_pending`、`candidate_review_only`、`changes_requested`、`verified`を区別する。今回の実行では最初の二状態までを記録できる。未実装のAgentを実行済みと偽らない。検査用helperは常に `wordpress_handoff_allowed=false`、`publication_allowed=false` を返す。Human Approval前のrelease判定やWordPress操作は提供しない。

主張抽出とAIらしさの検査は候補検出であり、網羅性・真偽・自然さの証明ではない。数値や強い断定の単純検査で拾えない主張もA29の全文確認対象となる。小さなQAスコアを合計して100点評価にする処理は作らない。
