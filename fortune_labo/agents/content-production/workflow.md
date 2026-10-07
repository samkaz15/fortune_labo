# A08 — Workflow

A07 v2 Brief → schema確認・hash固定 → Blueprint → Writing正本snapshotとprompt → 外部モデル/担当者のDraft → structural findings → 本文根拠つきSelf Review → A29 → A32 → A28 → 人間承認 → 別途許可されたA25工程。

prepare_runは新規ディレクトリだけを作る。accept_draftは未完了runへ一度だけDraftを保存する。verify_runは入力・出力のhashとSEO版を照合する。DraftができただけでQA合格へ進めず、A29/A32/A28の実装・実施状態をhandoff側で別途表す。

今回の3本はユーザーが依頼した比較検証で終了する。privateからGitHub Draft/Fixtureへ保存する場合は、この3本への明示的許可と原資料非公開の制約を両方確認する。WordPressやSNSへ送らない。

Google変更を知った場合はpolicyの影響評価へ報告し、作業中のBriefやWritingルールを勝手に修正しない。適用方針が変わるなら承認済みversionを持つ新しいA07 Briefから開始する。
