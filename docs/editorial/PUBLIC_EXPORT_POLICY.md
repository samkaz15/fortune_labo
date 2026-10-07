# Public Export Policy

公開対象はユーザーが承認したFoundationと今回の実装に限定する。原資料、取得した記事の実データ、非公開テスト記事、個人情報を含む成果物は公開しない。

初期Foundationの許可リストは [public-export-manifest.json](public-export-manifest.json) に固定パスで保存する。STEP 2以降の実装はレビュー後に別manifestまたは同manifestへの明示的追加を必要とする。ディレクトリ全体を自動で追加しない。

```sh
python3 -B scripts/check_public_export.py --manifest docs/editorial/public-export-manifest.json
```

検査は許可リスト外の選択ファイル、Source本文・識別子・URL、詳細位置情報、非公開データのパス、調査数値の引用を拒否する。`--private-reference` にローカルの非公開Source JSONを指定すると、長い原文の一致も検査する。検査結果には一致本文や個人情報を出力しない。

Provenanceの各レコードに許可するキーは `source_id / source_type / source_title / access_scope / derived_artifacts` のみ。`access_scope` は `private`、`source_title` は一般的な別名とする。Sourceの私的なURLや保存先へのリンクを公開しない。

検査は人間のレビューを代替しない。短い言い換えに非公開の戦略詳細が残っていないことも確認する。GitHubへ送信する直前に選択したファイルのバイト列を再検査する。既存A06は変更せず、mainへmergeしない。
