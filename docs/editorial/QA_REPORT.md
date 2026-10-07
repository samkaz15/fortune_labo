# Editorial Foundation QA Report

更新: 2026-10-07。公開範囲は承認済みFoundation、実装・Schema、空の既存Indexと今回生成した3Fixture。原資料の原文・URL・個人情報・文書IDは保存しない。

## 検証結果

Python標準ライブラリの自動検証76件がPASS。Schema定義監査13件、既存0／Fixture3の統合Index、3本のBrief・Draft・review hashとSEO版の整合もPASS。これらは機械契約の検査であり、人間の公開承認や文章・主張の正しさの保証ではない。

| 必須確認 | 結果・参照 |
| --- | --- |
| Existing Article classification | 合成のWordPress metadataから根拠付き候補を生成。元記事・本文を変更しない |
| Unknown classification | 根拠不足・曖昧な入力はunclassified / low、Human Review |
| FREE decision | 基本回答を隠す設定を拒否。FREEのpremium valueはnull |
| PREMIUM decision | 具体的追加価値、value dimension、Intelligence出典が必要。長さだけの判定を拒否 |
| Opportunity generation | 初期11件から、登録済み3Fixtureと重なる2件を明示レビューで抑制。残り9件。scoreなし |
| A07 Brief generation | 選択根拠、5役割、必須要件、入力hashを保持。矛盾・出典欠損を拒否 |
| A08 Blueprint | 不変BriefのhashとWriting Source of Truthを保持 |
| A08 Draft | H1・見出し・順序・必須Self Reviewを検査。完了runの上書きを拒否 |
| AI-likeness check | 断片化した合成文を検出。実3稿は構造警告0件。判定器の結果を自然さの証明にしない |
| Fact claim extraction | 数字のない文も候補へ抽出。未検証候補をFACT承認へ昇格しない |
| QA handoff | A29 → A32 → A28を契約として渡す。人間承認とWordPress handoffはfalse/null |
| Google policy version trace | Brief / Blueprint / run / review / QAにdraft版を固定。検知による自動変更なし |

本文は別のモデルが全文通読し、指定9観点で旧稿と比較した。[詳細な比較](TEST_ARTICLE_COMPARISON.md)は新しい本文のSHA-256に結び付く。旧稿・原資料は転記していない。3本は検証用Draftとして確認済みで、顧客向け公開・販売はblocked。

## 件数の定義

- 既存WordPress記事: 0件（ユーザー確認。Importを実行した結果ではない）。
- 既存記事のclassified / unclassified: 0 / 0。分類機能の合成テストを実件数へ加えない。
- 生成Fixture: 3件。A/BはFREE、CはPREMIUM候補。genreはcareer / love / career。未知subgenreはnull。
- Content Opportunity: 9件、重複抑制2件。検索需要未検証のkeywordはnull、優先ラベルはreview。
- Performance: 17 raw metrics未接続。値はnull、集計Scoreは作らない。

## 公開と未確定事項

原資料はopaque provenanceのみ。許可リストと禁止pattern検査、非公開原資料の長い原文との照合を送信前に実施する。A06の22ファイルは元ファイルと一致する。

正式SEO policy、A06の個別採用と独自素材、商品・診断の実体、実URL、著者・監修者、Performanceのイベント定義・接続、人間による記事別承認は未確定。A29/A32/A28本体は未実装で、今回の役割相当のモデルQAをAgent本体や人間の承認と呼ばない。WordPress・SNS・Scheduling・main mergeは実行しない。
