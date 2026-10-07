# FREE / PREMIUM Rules

Version: 0.2.0。編集判断の方向性は承認済み。商品化・公開・A06戦略変更は別途判断する。

FREEは読者の基本的な問いを本文内で解決する。PREMIUM候補は、個人条件を扱う深さ、選択肢の比較、具体的な行動計画、繰り返し使える記録と見直しに追加価値を持つ。文字数だけで有料にせず、答えの途中を隠して購入へ誘導しない。この編集ルールは [Content Intelligence](content-intelligence.json) と `GR001` の公開用要約に基づく。Source IDの参照先は [Provenance](sources/provenance.json) に限定する。

| 判定項目 | FREE候補 | PREMIUM候補 |
| --- | --- | --- |
| `acquisition_role` | 読者の疑問への入口 | 該当する場合だけ記録 |
| `engagement_role` | 説明を自分の状況に当てはめる | 個人条件を継続して検討する |
| `conversion_role` | 本文で解決後に残る課題への任意導線 | 具体的な提供範囲が明示された価値 |
| `retention_role` | 保存や実行後の見直し | 反復利用の用途がある計画や記録 |
| `premium_value` | 原則null | 無料の回答を超える具体的成果物と用途 |

A07は上記の五つをすべて判定理由として保持する。該当しない役割や根拠のない役割はnullにし、判定そのものにconfidenceと `evidence_refs` を付ける。`CONTENT_INTELLIGENCE` の該当ジャンルと本ルールの両方を参照できない場合、AIの直感で確定せずHuman Reviewに回す。

判定手順は、読者の問いと `core_answer` を決め、無料で完結すべき範囲を確認し、追加価値の実体を確認する順とする。一般的な説明・最初の一歩はFREE候補。個人条件、比較フレーム、実践計画などがBriefで明示され、ジャンルのpremium roleとも一致する場合だけPREMIUM候補にする。長文、専門用語、表の数は根拠にならない。

既存記事の `access_type` は実データで確認した値を保存する。分類の `free_premium_candidate` は編集上の提案であり、実際の閲覧制限や販売状況を上書きしない。根拠不足・対立・未対応ジャンルはnullまたは `unclassified` とし、low confidenceには人間の確認を必須にする。

PREMIUM候補が自己記入ワークの場合は、その範囲を明示する。本人の入力、占術の根拠、鑑定者の見立てがないものを個別鑑定済みと扱わない。成果保証、不安をあおる販売、医療・金融・法律の結果保証、依存を促す継続導線は使用しない。

CTAの実在・条件・URLが未確認ならnullを保持し、公開可能と判定しない。人間によるFoundationの承認は個別記事・商品・SEO policy・WordPress操作の承認を兼ねない。
