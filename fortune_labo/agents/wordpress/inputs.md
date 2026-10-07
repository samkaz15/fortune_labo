# Inputs

`build_draft_payload(article, image_plan, qa, media_receipts=[], site_config={}, requested_status='draft', fixture_mode=False)`を使用する。

`article`は`content_id`, `title`, `content`（A08 Markdown全文）, `draft_sha256`, `article_version`, `seo_policy_version`, `access_type`を持つ。`content_format`は`markdown`のみ。`excerpt`, `slug`, `categories`, `tags`, `internal_links`, `cta`, `seo_meta`は不明ならnull。分類は実WordPress term IDが確定したときだけ整数配列で渡す。

`image_plan`はA11の正式出力。`generated_asset_reference`のstate/hash/pathと生成状態を使用する。assetの実ファイル・寸法・権利・画像内容はA11の検証とA29/A32/A28で確認したものを渡す。A25は画像生成や権利の推測を行わない。

`qa`は同content IDの`draft_sha256`, `image_plan_sha256`（canonical JSON hash）, `scope: offline_fixture | draft_preparation`, `blockers`, `gates`を持つ。gatesはA29/A32/A28を一度ずつ登録し、それぞれ`status: passed`, `evidence_ref`, `reviewer_kind: model_review | human_review`が必要。現在のFixtureのモデル相当QAと正式agent稼働を区別する。

`media_receipts`はupload/取得結果の記録であり、計画段階では空配列。`asset_id`, `content_id`, `site_id`, `image_sha256`, `attachment_id`, `source_url`, `response_reference`, `receipt_type`, `state`を保持する。テスト用IDは`receipt_type: test_fixture`かつ`fixture_mode=True`でのみ受け付ける。通常runtimeへ混ぜない。
