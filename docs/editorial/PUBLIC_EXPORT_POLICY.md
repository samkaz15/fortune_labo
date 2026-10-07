# Public Export Policy

公開対象はユーザーが承認したFoundationと今回の実装に限定する。原資料、取得した記事の実データ、旧テストDraft本文、個人情報を含む成果物は公開しない。追加指示で明示的に許可された今回のA07→A08生成3本は、GitHubのDraft/Fixtureとして保存できる。

初期Foundationの許可リストは [public-export-manifest.json](public-export-manifest.json) に固定パスで保存する。STEP 2以降の実装はレビュー後に別manifestまたは同manifestへの明示的追加を必要とする。ディレクトリ全体を自動で追加しない。

```sh
python3 -B scripts/check_public_export.py --manifest docs/editorial/public-export-manifest.json
```

検査は許可リスト外の選択ファイル、Source本文・識別子・URL、詳細位置情報、非公開データのパス、調査数値の引用を拒否する。`--private-reference` にローカルの非公開Source JSONを指定すると、長い原文の一致も検査する。検査結果には一致本文や個人情報を出力しない。

Provenanceの各レコードに許可するキーは `source_id / source_type / source_title / access_scope / derived_artifacts` のみ。`access_scope` は `private`、`source_title` は一般的な別名とする。Sourceの私的なURLや保存先へのリンクを公開しない。

検査は人間のレビューを代替しない。短い言い換えに非公開の戦略詳細が残っていないことも確認する。GitHubへ送信する直前に選択したファイルのバイト列を再検査する。既存A06は変更せず、mainへmergeしない。

## 今回の生成Fixtureの例外

許可するのは `docs/editorial/test-articles/FL-TEST-A/`、`FL-TEST-B/`、`FL-TEST-C/` のみ。Brief、Blueprint、生成Prompt、生成Draft、Self Review、Claims、QA、比較結果、run記録とexport manifestを対象にし、各ファイルを公開許可リストに列挙する。元Draft本文、原資料本文、実記事データは含めない。比較には編集上の差分とQA結果を記録し、旧Draft全文を再掲しない。

各フォルダの `manifest.json` に `export_scope=explicitly_authorized_a07_a08_fixture`、一致する `content_id`、`contains_private_source=false`、`contains_legacy_draft=false`、`publication_allowed=false` を必須とする。これは公開対象を限定する記録で、WordPress公開や商品化の承認ではない。本文の原資料照合と人間による内容確認も引き続き必要である。

A08の通常出力はprivate領域で生成し、今回の3本だけを確認後にexportする。private領域の出力制約は緩めず、生成と公開Fixtureの保存を分ける。

既存記事0件の `existing-content-index.json` はユーザー確認を出典として保存できる。実データ取得の成功とは表示しない。`test-content-index.json` には今回の生成Fixture3件だけを登録し、WordPress ID・公開URL・公開日はnull、statusはtest_draftとする。実記事の件数には加算しない。
