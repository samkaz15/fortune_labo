# A07 — Integrations

ローカルJSON/Markdownのみ。外部API、WordPress、SNS、予約配信、ログイン情報は使わない。Intelligenceには安全な派生情報と出典IDを渡し、非公開原文は別のprivate storageで保全する。

`fortune_labo/editorial/strategy.py` は標準ライブラリとリポジトリ内schema検証器を使う。外部モデル呼出は内蔵しない。モデル/人間の判断はprompts/brief.mdに従ってdecisionへ入力し、コードは根拠・制約・型・整合を検証する。

出力はdictであり、自動保存・push・投稿・公開権限を持たない。A08への引継ぎ後も承認情報は生成しない。
