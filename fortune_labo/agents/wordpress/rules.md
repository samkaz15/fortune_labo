# Rules

`publish`, `future`, `private`, `pending`は受け付けない。statusを省略して公開設定に依存することもない。下書き後に人間が公開承認する流れを維持し、A25がその承認を作らない。

本文・画像計画・QAのhashやcontent IDが異なる場合は停止する。画像や本文を変更した場合はQAを再実施する。source H1は投稿titleに対応付け、重複H1を避けるためHTML bodyからは省く。本文は見出し、段落、表、list、明示リンクの整形と承認済み画像位置のfigure追加だけを行い、文章を書き換えない。原Markdownファイルを変更しない。

PNG/JPEG/WebPはupload計画の対象。SVGは通常WordPressへのuploadを仮定せず`requires_conversion`として停止する。変換やHTML layerの採用は別の確認対象。生成失敗・未生成・未取得attachment・未QAを成功扱いにしない。

画像のretryはsite/content/hashを含む同じdedup keyで記録する。受信済みIDがある画像はreuseし、uploadを再計画しない。異なるsiteのpost/media receiptを混ぜない。タイムアウト等でupload結果が不明な場合は、将来の接続側が照合してreceiptを確定するまで再送しない。WordPress自体にこのdedup keyが実装済みとは主張しない。

メタフィールドは`site_config.meta_mapping`と`registered_meta`で明示されたものだけを使用する。登録根拠、REST write対応、型の一致が必須。既知のplugin名から勝手に内部keyを推測しない。未設定metaはsidecarに保持する。
