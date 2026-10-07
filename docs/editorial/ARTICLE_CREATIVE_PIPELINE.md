# Article Creative Pipeline

Version: 1.0.0 / 2026-10-07。今回の追加指示に基づく記事・画像・WordPress下書きの契約。A06の既存仕様と、生成済みA07/A08 FixtureのBrief・本文・hashは変更しない。記事の生成、画像の生成、WordPress下書き、顧客向け公開は別の状態として記録する。

```text
A06 → Content Index → A07 → A08 → A11
                                  ↓
                  A29 Fact Check → A32 Editorial → A28 QA
                                                        ↓
                                                  A25 WordPress draft
                                                        ↓
                                                   Human Approval
                                                        ↓
                                                   Human publish
```

人間の公開承認はWordPress下書きの後に置く。以前の「下書き作成前にも記事の人間承認が必須」という順序は、この追加指示の対象範囲では上記へ更新する。ただし、QA未完了、source不足、policy不整合、権限・接続先の未設定を通過扱いにしてよいわけではない。A25は検証済みのjobを `status=draft` としてのみ扱い、`publish / future / pending / private` などへの書込み、予約公開、公開済み記事の更新は行わない。publish操作は人間が行う。

## Jobと変更境界

Jobは一つの `content_id` に対し、A07 Brief、A08 Draft、Article Production Rules、適用 `seo_policy_version`、A11 planとasset、QA結果、WordPress payloadを追跡する。各成果物の参照とhashで対応を固定し、別記事の素材を混ぜない。本文またはBriefを直す必要があればA07/A08の新しいrunへ戻り、A11やA25が黙って本文を改変しない。

| 段階 | 入力 | 成果物と止まる条件 |
| --- | --- | --- |
| A07 | A06、Index、Intelligence、Performance、Opportunity | 変更禁止のContent Brief。根拠不足は明示 |
| A08 | Brief、Writing Source of Truth | Blueprint、Draft、Self Review。Briefを変更しない |
| A11 | 該当記事のDraftとBrief | image plan、生成prompt、asset provenance、画像QA。生成失敗はpending/failedで残す |
| A29 | 本文・主張台帳・画像内の主張・出典 | 事実、解釈、仮例、実体験を確認。未検証は残す |
| A32 | 本文・画像・配置案・CTA・alt | 日本語、検索意図、段落、読みやすさ、画像との一致を確認 |
| A28 | 全artifactの対応、hash、policy、QA | 下書き引き継ぎ可否。未解決blockerを隠さない |
| A25 | 検証済みjob、media plan、draft payload | 認証済みの指定サイトに下書きだけ作成。dry-runと実行結果を区別 |
| Human | WordPress上の具体的な下書きとQA | 最終確認後に公開を判断し、公開操作を行う |

通常のA08 private出力制約は維持する。追加指示で許可されたA/B/Cの生成Fixtureとその画像だけを、公開許可リストへ個別に追加できる。原資料、旧Draft、実記事の私的な入力、認証情報は公開しない。

## A11の画像契約

画像は記事の説明を補うために作る。記事のtopic、検索意図、主張、該当する節から構図を決め、`source_article_ref / source_article_sha256` をimage planとassetに結び付ける。話題と無関係な装飾画像を、本文に根拠がある図解と表示しない。

Featured imageと必要なsection imageは、用途、掲載位置、構図、比率、生成prompt、alt、文字overlayの有無を記録する。日本語の見出しやラベルは内容と表記を確認し、読めない文字を完成扱いにしない。既存の人物・神社・訪問現場を記録した実写真のように見せず、説明用の生成画像であることをprovenanceに保持する。架空の顧客、実績、口コミ、鑑定結果、統計、資格を画像に追加しない。

Assetには生成由来、生成手段、記事との対応、ファイルhash、media type、寸法、altと画像QA結果を残す。参照画像が必要な場合は使用権限と公開可能性を別途確認する。非公開調査資料や個人情報を生成promptや画像文字へ転記しない。生成ツールが未接続、失敗、出力不足の場合はその事実を保存し、placeholderを生成成功と偽らない。

画像QAは本文との意味の一致、文字の正確さ、視認性、トリミング、実写との誤認、private sourceの混入を確認する。生成直後のassetは自動でQA済みにならない。未確認のaltや図中の断定もA29/A32へ渡す。

## A25の下書き契約

WordPressへの書込みには、明示された対象サイトと必要な認証、検証済みpayload、media upload planを用いる。planを保存しただけではuploadやdraft作成が成功したと記録しない。外部応答のpost IDとmedia IDは成功後に保存し、再実行時は同じjobの既存結果を確認して重複を避ける。失敗した途中状態を保持し、本文とmediaの対応を再確認できるようにする。

本文は生成Draftからの変換として追跡し、PREMIUMのアクセス設定やプラグイン機能を推測で適用しない。URL、カテゴリー、タグ、featured media、CTAの未確認値をもっともらしい値で補完しない。接続先やプラグイン仕様が未確定なら、ローカルのpayloadとplanをreviewableな状態で保存して止める。

追加指示によって下書き前の人間公開承認は不要になったが、公開権限はAgentへ移らない。Agentが受け付けるpost statusはdraftだけとし、人間承認が存在してもAgentからpublishへ昇格するコードは設けない。SNS投稿・大量生成・自動Schedulingは開始しない。

## Google PolicyとQA

Google updateは検出だけで制作ルールに反映しない。`Google Update → Impact Assessment → Human Approval → SEO Policy Version → A06 / A07 / A08` を保ち、そのversionをA11、QA、A25のjobにも引き継ぐ。これはGoogle policyを承認する人間工程であり、WordPress上の記事を公開する人間工程とは別である。

A29/A32/A28本体が未実装で `contract_pending` の場合、従来のQA helperは引き続き下書き引き継ぎ不可を返す。モデルのself reviewを人間承認や未実装Agentの完了に置き換えない。現在の未承認SEO policyとA06の未解決事項も、生成やdry-runができたことによって解消したとは扱わない。

参照: [QA Handoff Contract](QA_HANDOFF_CONTRACT.md)、[Public Export Policy](PUBLIC_EXPORT_POLICY.md)、[Google Update Watch Contract](../seo/GOOGLE_UPDATE_WATCH_CONTRACT.md)。
