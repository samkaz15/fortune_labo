# A08 — Outputs

| ファイル | 内容 |
|---|---|
| brief.json | 不変の入力Brief v2 |
| blueprint.json | 回答、節意図、根拠、CTA、リンク、アクセス区分と入力hash |
| writing-rules.md / draft-prompt.md | Writing正本snapshotと呼出用prompt |
| article.md | 外部モデル/担当者が書いたDraft |
| self-review.json | 本文箇所に基づく17基準のreview、未確定事項、Brief/Draft hash |
| writing-findings.json | 短文・一文一改行等の構造的な警告。品質判定や人間承認ではない |
| run.json | 工程状態、全hash、適用SEO版、次のhandoff、公開不可 |

`accept_draft(run_dir, draft_text, self_review, *, private_root)` はBrief/Blueprint不変、H1・H2/H3整合、Self Reviewの必要項目を確認して保存する。戻り値のrelease_gateは常にblocked。`verify_run` で保存時のhashと関連artifactを照合する。修正版は新しいrunにする。

hashは変更検知と再現性のための証跡であり、署名や第三者の承認を保証しない。保存者が全artifactを改変できる環境では別途権限管理が必要である。本文の意味の正しさや文章品質をコードだけで保証しない。
