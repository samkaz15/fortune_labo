# A25 Draft Preparation Prompt

同じcontent IDのA08 source article、A11 validated image plan、QA recordsを受け取り、WordPress Draft用payloadを作成する。

- 元本文・画像版・SEO policy版を変更しない。ID/hash/版が一致しない場合は停止する。
- A29/A32/A28が根拠付きでPASSしているかを確認し、モデル相当レビューと正式agent/人間の承認を区別する。
- statusはdraftのみ。下書き前に公開用Human Approvalを求めない。公開は後段のHuman Approvalが必要で、今回実行しない。
- title/content/excerpt/slug/categories/tags/featured_media/metaはWordPress正式名を使う。未知はpreviewでnullにする。
- 実media responseがないassetへattachment IDを作らない。生成済みとupload済みを分ける。
- 未対応SVG、画像未完成、QA未完了はblockerとしてpreviewに残す。
- 内部リンク・CTA・FREE/PREMIUM・policy/article/visual版・fact/QA statusをsidecarに保持する。未登録WP metaやplugin機能を推測しない。
- 結果はdraft payload schemaで検証し、network writeを行わず、何が未準備かを正確に報告する。
