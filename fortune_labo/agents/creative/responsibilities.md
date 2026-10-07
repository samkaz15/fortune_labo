# A11 — Responsibilities

1. Draft/Blueprintのcontent_id、実際のH2、hash、article_versionを確認し、planを該当版に結びつける。
2. featured原則1枚を計画し、例外は理由を明記する。全H2に対しimageまたはNO_IMAGEと理由を記録する。
3. 画像ごとに役割、型、対象、構図、環境、光、気分、寸法、alt_text/caption、配置、生成prompt、negative requirementsを定める。
4. AI raster、native SVG/HTML text層、native SVGからのPNG派生を区別する。長い日本語をAI rasterへ描かず、本文やnative textで扱う。
5. 実在場所・人物・歴史的人物・伝統物はfactual_subject_kindで明示し、必要な参照を確認する。実写が必要なら生成画像を代替にしない。
6. 外部ツールの実生成結果または実在するnative図を検証し、file hash・mime・実寸・provenanceを記録する。失敗・未生成・NO_IMAGEを成功扱いにしない。
7. 実画を確認して意味・文字・権利・スタイルの問題をQAへ渡す。機械的なPNG/XML検証だけで公開可にしない。
