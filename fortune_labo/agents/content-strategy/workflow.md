# A07 — Workflow

A06要件確認 → Indexの完全性確認 → Opportunitiesの根拠・重複確認 → Intelligence照合 → 4目的のPerformance確認 → モデル/担当者による制作対象選択 → FREE/PREMIUM判定 → Brief組立・検証 → A08。

選定プロンプトは候補ごとに「誰の何を解決するか」「既存記事を更新すべきか」「今必要な追加価値は何か」を説明し、採用しない理由も残す。件数や総合scoreで自動選定しない。選択した候補に関する条件がfalseならhelperはエラーを返すので、架空の入力で埋めず上流へ差し戻す。

今回は実記事0というユーザーの確認をinventoryの根拠として利用できる。そこから登録する3本は公開記事数へ加算せずtest_draft/fixtureとして区別する。追加生成や自動スケジュールはしない。

Google変更は検知→影響評価→人間承認→policy version更新の手順へ送る。Briefは作成時のseo_policy_versionを保持し、既存Briefを最新versionへ一括書き換えない。
