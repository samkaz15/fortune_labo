# A11 — Inputs

必須入力は不変のArticle Draft、Blueprint、content_id、article_version、Visual Identity、画像判断の一覧。非公開調査原文や元Docs URLは画像計画へコピーしない。必要な根拠は安全な出典IDで参照する。

`article_sections(article_path, blueprint_path)` は実際のH2を確認してh2-01等のsection_idを返す。Blueprintと見出しが異なる場合は中断する。

`image_template(content_id, image_id, *, section_id, section_heading=None, image_role='section', visual_type='NO_IMAGE', no_image_reason=None)` は必要項目を持つテンプレートを返す。TBDを含む描画予定は完成planとして受け付けず、A11担当が具体化する。

`create_image_plan(article_path, blueprint_path, *, content_id, article_version, images, visual_style_version='visual-style-0.1.0', featured_exception_reason=None)` がplanを検証して返す。source参照はpublic repository内の相対pathか非公開sourceを示す識別子に留める。入力ファイルを書き換えない。
