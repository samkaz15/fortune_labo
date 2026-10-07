# A08 — Integrations

標準ライブラリのローカルファイル操作だけを行う。外部API、WordPress、SNS、スケジューラ、モデルSDK、認証情報は使わない。LLM本文生成は呼出側の会話または人間の作業として明示し、コードに隠さない。

private_rootを明示し、public repositoryの内部・親ディレクトリをprivate保存先として指定することを拒否する。symlink解決後も範囲を確認する。A08からGitへ自動export、commit、pushしない。

schemaはschemas/のBlueprint、Self Review、run manifestを使い、A07のv2 schemaも検証する。記事・調査の非公開原文はログへ出力しない。公開テストでは合成データだけを使用する。
