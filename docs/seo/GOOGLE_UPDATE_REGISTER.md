# Google Update Register

この台帳は2026-10-07に行った限定的な一次資料確認の記録である。5件は互いに独立したGoogle更新の件数ではなく、起点の記事、後続の説明、現行ドキュメントを含む。未調査の更新を「確認済み」と扱わない。日付は資料に示されたもののみを記録する。

## 確認した資料

| ID | 一次資料 | 種類 | 公開日 | 資料内で確認した更新日 | 取得・確認日 | 今回読んだ範囲 |
| --- | --- | --- | --- | --- | --- | --- |
| GS-001 | [2022 helpful content update](https://developers.google.com/search/blog/2022/08/helpful-content-update?hl=ja) | ユーザー指定の起点・過去の発表 | 2022-08-18 | null | 2026-10-07 | ユーザー第一という考え方と当時の更新説明 |
| GS-002 | [March 2024 core update and spam policies](https://developers.google.com/search/blog/2024/03/core-update-spam-policies?hl=ja) | 過去の変更説明 | 2024-03-05 | 2024-06-04（記事末尾に記載された追記日） | 2026-10-07 | 複数のコアシステムと大量生成の不正使用に関する説明。追記箇所は今回の運用根拠に使わない。 |
| GS-003 | [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content?hl=ja) | 現行ドキュメントの参照 | null | null（今回の日付記録は未確認） | 2026-10-07 | 自己評価、著者・制作過程・目的、E-E-A-T、文字数と更新日 |
| GS-004 | [Spam policies](https://developers.google.com/search/docs/essentials/spam-policies?hl=ja) | 現行ドキュメントの参照 | null | null（今回の日付記録は未確認） | 2026-10-07 | キーワードの乱用、大量生成されたコンテンツの不正使用 |
| GS-005 | [Ranking systems guide](https://developers.google.com/search/docs/appearance/ranking-systems-guide?hl=ja) | 現行ドキュメントの参照 | null | 2025-12-18（ページ表示、UTC） | 2026-10-07 | 廃止されたシステム内の helpful content の扱い |

`null` は日付が存在しないという断定ではなく、この台帳で確認・記録できていないことを意味する。GS-002 の追記日と GS-005 のページ更新日は、2024年3月の変更が発生した日として使用しない。

## IA-001 — 初期案の影響評価

| 項目 | 記録 |
| --- | --- |
| 評価日 / 評価者 | 2026-10-07 / AIによる基盤構築レビュー |
| 参照資料 | GS-001〜GS-005 |
| 変更前 | このEditorial基盤にversion登録はない。A06の既存仕様は存在する。 |
| 評価結果 | `change_required` — 制作ルールとpolicy登録・承認手順を追加する案 |
| 提案version | `seo-policy-0.1.0-draft` |
| 対象rule | SEO-P01〜SEO-P06 |
| 対象artifact | 記事制作ルール、Content Index、A07→A08 Brief、テスト記事3本、QA |
| 人間の判断 | `pending_human_approval` |
| 承認者 / 承認日時 / 承認記録 | null / null / null |

起点の2022年記事を保持しつつ、独立した helpful content システムの説明を現在の運用前提として引き継がない。GS-005が示すコアへの統合を注記し、文書参照先を現行資料へつなぐ。社内で必要な変更は、読者の問い、主張の根拠、制作責任、低価値の大量生成と不自然な反復の検査を、追跡できる工程にすることである。

今回の評価で順位・売上・コンバージョンへの効果は測定していない。Googleの要件を、Fortune Laboのジャンル別需要やFREE/PREMIUM分類の根拠に流用しない。既存A06の事業方針、Tier D、訪問素材の条件、キーワード優先度式は変更しない。調査とA06が衝突する場合は別の戦略判断を要する。

検証は、テスト記事3本のpolicy参照、五つのSEO入力、六つのclaim分類、段落の自然さ、FREE/PREMIUMの差、CTA・内部リンク、未確認事項の扱いを確認する。テスト品質と公開条件は分けてQA報告する。未承認のため運用への移行は実施せず、戻し方はこの追加案を採用しないことになる。元のA06に復旧作業は発生しない。

## 次回以降の登録形式

新しい一次資料を確認したら、source ID、URL、資料名、種類、公開日、表示更新日、取得日、確認した節、事実として確認できた変更、未確認事項を追加する。履歴を追跡できない場合、過去版との差分が確認できたように書かない。その資料を元に別の `assessment_id` を作り、対象記事、変更案、テスト、承認状態を記録する。

登録だけでpolicyは昇格しない。承認対象の具体的なdiffと実際の人間の承認記録がそろった後に、[SEO_CHANGELOG](SEO_CHANGELOG.md) と [registry](SEO_POLICY_REGISTER.json) を更新する。定期監視や自動スケジュールは今回作成していない。
