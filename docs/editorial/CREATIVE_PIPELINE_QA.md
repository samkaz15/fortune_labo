# Article + Creative + WordPress Draft QA

対象は既存A07/A08の3Fixture。本文、Brief、Blueprint、Writing Rulesのsnapshotは変更していない。後段Jobのpipeline_versionは`article-creative-1.0.0`、article_versionは`article-1.0.0`、visual_style_versionは`visual-style-0.1.0`。article_versionは後段連携用の初回ラベルで、旧稿への巻き戻しや本文の改稿を意味しない。

## FL-TEST-A

A29相当のモデル確認: FeaturedはAI生成の机上イメージで、実在の職場や取材写真ではないとcaptionに表示。説明図の三分類と例は記事本文の架空の場面から取り、転職結果や勤務条件の実在を主張しない。

A32相当のモデル確認: Featuredは三枚の白紙とノートで最初の条件整理を表す。H2-01だけ、変えたいこと・残したいこと・未確認のことを比較する説明図を付ける。残り2節は本文にある質問とメモ例を優先し、NO_IMAGEの理由を保存した。実画像を目視して文字・ロゴ・過剰な占い表現がないことを確認。SVG由来の短い日本語は描画結果も目視し、欠けや誤字は見られなかった。

A28相当の構造確認: article/blueprint hashとimage planの参照、2assetの実ファイル・寸法・hash、SVG masterのhash、alt/caption、H2位置を検査。Draft Payloadは画像2件の登録待ちプレビューで、WordPress作成済みとは表示しない。

## FL-TEST-B

A29相当のモデル確認: Featuredは伏せたスマートフォンとノートを置いたAI生成の静物で、相談者の写真ではない。説明図は確認済みの用件・日時と未確認の事情・気持ちを分離し、相手の心理を当てる図にしていない。

A32相当のモデル確認: スマートフォンを主役にし過ぎず、自分の予定へ目を向ける本文の目的に合わせた。H2-01のみ分類図を配置。仮の連絡文はコピー可能な本文に残し、同じ雰囲気の画像は追加しない。実画像とPNG化した図を目視し、日本語の欠けや不自然な記号を認めなかった。

A28相当の構造確認: 2assetを同じcontent_id、本文hash、style versionで追跡。診断の実URLは未知のままで、架空のリンクを埋め込んでいない。2件のMedia登録は未実行。

## FL-TEST-C

A29相当のモデル確認: Featuredは白紙のワークブックと用紙のAI生成イメージ。90日での成功や実在する成果を示すグラフは含めない。本文どおり自己記入ワークとして扱う。

A32相当のモデル確認: 紙・自然光・落ち着いた色味をA/Bと統一。4つのH2を全て検討し、既存の3つの記入表と段落説明が用途を果たすためNO_IMAGEとした。表を画像へ焼き込まず、WordPress本文へのHTML変換でも表として保持する。

A28相当の構造確認: Featured 1assetを追跡。PREMIUM区分は編集候補のmetadataで、WordPressの課金・閲覧制限を実装済みとは表示しない。Media登録は未実行。

検証結果: 全129テスト、18件のSchema定義監査、3Jobの再構築と既存3稿のhash検証がPASS。実WordPressへの書込みは0件。

## QAの範囲と停止点

上記の各役割に相当するモデルレビューは、今回のoffline_fixtureに限りPASSと記録する。A29/A32/A28本体の実装や人間の承認を意味しない。各qa.jsonは本文と最終image-planのhashに結び付き、変更後の使い回しを拒否する。元A08のqa.jsonは歴史的なレビューsnapshotとして不変に保つ。

最新のユーザー指定により後段の順序はA11 → A29 → A32 → A28 → A25 draft → Human Approval → PUBLISH。旧Briefのhandoff配列やWriting Rulesを改変せず、新しいJobのroutingでこの追加経路を明示する。A25にはdraft以外のstatusを生成・送信する機能を設けない。publishは人間の別操作となる。

5件のMedia Library登録、post作成、サイトのtaxonomy/REST meta登録は未実行。attachment_id、WordPress post ID、サイトIDはnull。proposed_payload.statusは全件draft、request_payloadはnull、network_readyはfalse。編集・SEO metadataはsidecarへ保持し、登録根拠のないmeta keyをREST payloadに追加しない。

正式SEO方針、A06の本番採用、著者・独自素材、商品仕様、実CTA・内部リンク、公開承認は依然として未確定。画像生成が完了したことを、これらの承認へ読み替えない。

## 生成と再現

Featured 3枚は組込みimage_genを実行した成果物。説明図2枚はコードで作成したSVGのnative text層をSharpでPNGへレンダリングした成果物。生成AIに日本語を描画させていない。生成prompt、配置、NO_IMAGE判断は各image-plan.json、由来と実寸はassets.json、記事からDraftまでの参照はjob.jsonに保存する。生成済みと記録する前に実ファイルを検証する。

```sh
python3 -B scripts/verify_test_fixtures.py
python3 -B scripts/verify_creative_fixtures.py
python3 -B scripts/validate_editorial.py --schemas-only
python3 -B -m unittest discover -s tests -v
```

断続的な失敗は本文を破棄せずarticle_readyを維持し、image_incomplete / image_generation_pending / fact_review_required / editorial_revision_required / qa_failed / draft_sync_failedを段階別に記録する。Mediaの同一hashは同じsite・content単位で照合し、受領済みattachment IDを再利用する。自動Schedulingや大量生成は開始しない。
