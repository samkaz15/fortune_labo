# A11 — Workflow

Draft + Blueprint → hash/H2確認 → Visual Identity確認 → featuredと全H2の画像判断 → plan検証 → 外部画像生成またはnative図制作 → 実ファイル検証・asset登録 → 実画QA → A25 Draft payload。

画像生成ツールのpromptは記事用に具体化し、生成自体はツール実行で行う。helperが画像を作ったと偽装しない。失敗時はrecord_generation_failureを使って失敗を残す。成功したファイルだけadd_assetへ渡す。

`add_asset(plan, image_id, asset_path, *, asset_root, provenance)` は入力planを変更せず、新しいplanを返す。asset_root配下の実ファイルだけを受け付け、勝手な置換を拒否する。修正版は意図的なplan改訂として別途扱う。

`validate_image_plan(plan, article_path, blueprint_path, *, asset_root)` は実際の元記事・Blueprintと全assetを再検証する。A25はこのplanとQAに結び付くhashを使い、WordPress用の派生payloadを作る。upload・draft creation・publishの実行許可はそれぞれ別で、A11は実施しない。

今回の対象は指定済み3記事。記事数や画像目的を無断で拡張せず、WordPress公開、SNS投稿、Schedulingに進まない。
