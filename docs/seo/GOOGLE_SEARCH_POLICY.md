# Google Search Policy — Fortune Labo

| 項目 | 現在値 |
| --- | --- |
| 提案 policy version | `seo-policy-0.1.0-draft` |
| 状態 | `pending_human_approval` |
| 承認済み現行 version | `null` |
| 承認者 / 承認日 / 承認記録 | すべて `null` |
| 確認日 | 2026-10-07 |
| 今回使用できる範囲 | 依頼済みの非公開テスト3本とQA |

機械可読な正本は [SEO_POLICY_REGISTER.json](SEO_POLICY_REGISTER.json)。本書を追加したこと、テストが成功したこと、Draft PR が作成されたことは、運用 policy の人間承認を意味しない。

## 根拠と読み方

ユーザー指定の起点は [2022年8月18日のヘルプフル コンテンツ アップデートの記事](https://developers.google.com/search/blog/2022/08/helpful-content-update?hl=ja) である。これはユーザーの問いに応える内容を重視する方針の出発点として保存する。2022年当時の独立したシステムや展開条件を現在の仕組みとして適用しない。

[2024年3月5日の公式説明](https://developers.google.com/search/blog/2024/03/core-update-spam-policies?hl=ja) と [現在のランキングシステムガイド](https://developers.google.com/search/docs/appearance/ranking-systems-guide?hl=ja) で、helpful content が2024年3月からコアランキングシステムに組み込まれたことを限定確認した。現在の編集上の参照先は [people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content?hl=ja) と [spam policies](https://developers.google.com/search/docs/essentials/spam-policies?hl=ja) とする。確認範囲はこの5資料に限り、Googleの更新史を網羅したものではない。

Google の記載内容と Fortune Labo の運用判断は [更新台帳](GOOGLE_UPDATE_REGISTER.md) で分ける。公開日、ページの表示上の更新日、実際に内容を確認した日、サイト内部で適用を承認した日を混同しない。不明な日付は `null` とする。取得日はページの更新日を意味しない。

## 制作に適用する案

| Rule ID | Fortune Labo の運用案 | 根拠・位置付け |
| --- | --- | --- |
| SEO-P01 | Briefで読者・問い・core answerを定め、読み終えたときに基本的な目的を達成できるかQAする。 | GS-001 / GS-003を記事制作に適用する内部ルール |
| SEO-P02 | 独自素材の出典、判断主体、実体験の由来を残す。架空の著者・経歴・体験を作らない。 | GS-003と既存A06を接続する内部ルール |
| SEO-P03 | AIの利用有無だけで品質を判定せず、内容の価値・正確性・制作責任を確認する。ランキング操作を目的とする低価値の大量生成をしない。 | GS-004の該当範囲。今回の大量生成禁止はユーザー指示でもある。 |
| SEO-P04 | キーワードの不自然な反復をしない。文字数の達成を品質基準にせず、実質的な変更のない日付更新をしない。 | GS-003 / GS-004 |
| SEO-P05 | 著者、根拠、編集・AI利用の役割を確認できるようにし、読者の判断に必要な説明を載せる。 | GS-003。すべてのページに特定のAI表示文を義務付けるとの解釈はしない。 |
| SEO-P06 | Googleの変更を確認しても記事群・A06・承認済みpolicyを自動で書き換えない。対象と差分を評価する。 | Fortune Laboの承認・バージョン管理ルール |

E-E-A-Tを単一のランキング点数として扱わない。Googleの説明は品質確認の根拠であり、社内QAの合格から順位上昇や検索流入を保証するものではない。[Google の説明](https://developers.google.com/search/docs/fundamentals/creating-helpful-content?hl=ja)

本文の具体的な確認方法は [記事制作ルール](../editorial/ARTICLE_PRODUCTION_RULES.md) を使う。A06 のキーワード階層、事業上の優先度、参拝記録の要件は維持する。新しい Content Index に weight / 総合 score を設けないという今回の要件を、A06 の既存キーワード優先度式への変更と解釈しない。

## 変更の流れ

```text
Google Update / documentation change
  → source verification and update register
  → impact assessment
  → human approval of the concrete policy diff
  → SEO policy version update
  → A06 → Content Index → A07 → A08
  → A29 → A32 → A28 → separate human approval → A25 WordPress Draft
```

1. A06 / Research は一次情報のURL、対象範囲、公開・更新・確認日を台帳へ登録する。記事のPVや順位の変動だけでGoogle変更との因果を断定しない。
2. A06 が変更前後の解釈、影響するルール、記事・Brief・ジャンル・FREE/PREMIUM区分、既存A06との衝突、変更不要な部分、検証方法、戻し方を整理する。検索効果は測定していなければ仮説とする。
3. A07 / A08 / A29 / A32 / A28 が制作・検証への影響を確認し、承認対象となる文書と差分を固定する。承認待ちは `pending_human_approval` とし、既存の承認済みversionがあれば運用はそちらを維持する。
4. 人間が具体的な差分と適用範囲を確認した後に限り、承認者、承認日時、元の承認記録を保存する。AIの自己評価、CI成功、承認欄の仮入力を人間承認の代わりにしない。承認内容が変わる修正には再承認が必要である。
5. Codex が承認された差分を新しいversionとして登録し、旧versionを保持する。`current_approved_policy`、対象versionの状態、承認情報、SEO_CHANGELOGを同一変更で整合させる。初回安定版の候補は `seo-policy-0.1.0` だが、現時点では未登録・未承認である。
6. A06 / A07 / A08 は承認された適用範囲でのみ新しいversionを使う。既存記事は従来の `seo_policy_version` を保持し、再評価・改稿・QAを経て更新する。Googleの変更検知だけで全記事のversionを一括書き換えない。

## 影響評価に残す情報

変更ごとに `assessment_id`、source IDs、評価日、評価者の種別、変更前後、影響するrule IDs、対象artifact IDs、リスク・不確実性、テスト方法、承認対象の差分参照、移行と戻し方を記録する。結論は `change_required / no_change / insufficient_evidence` のいずれかとし、人間による決定は別欄に残す。

`no_change` の記録にも理由が必要だが、policy versionを増やす必要はない。`insufficient_evidence` のまま検索施策を実行しない。外部公開・WordPress書き込み・事業方針変更の承認はpolicy承認とそれぞれ区別する。

## バージョンと復帰

`seo-policy-MAJOR.MINOR.PATCH` を用い、承認前には `-draft` を付ける。MAJOR は既存契約を破る変更、MINOR は後方互換な制作要件の追加、PATCH は判断を変えない訂正を想定する。番号の大きさより、何が変わり誰が何を承認したかを優先する。

旧versionへ戻す場合も影響評価と人間承認を記録し、過去の履歴を消さず、新しい変更記録として扱う。すでに外部へ書き込まれた内容を戻す操作は、別途その対象と操作への承認を必要とする。今回の初期状態では承認済みversionがないため、復帰対象もない。
