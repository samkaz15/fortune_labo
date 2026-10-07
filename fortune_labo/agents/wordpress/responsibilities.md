# Responsibilities

- 記事・画像計画・QAのcontent ID、本文hash、article version、visual style versionを照合する。
- A29/A32/A28のPASS、reviewer kind、根拠参照、blockerを確認する。モデル相当レビューを稼働中の独立QA agentやHuman Approvalと偽らない。
- WordPressの正式field名で下書きpreviewを作り、未知の分類・slug・excerpt等はnullに保つ。
- 画像をasset ID・image hash・site ID・content IDで追跡し、受信済みmedia receiptに基づいて関連付ける。
- 未登録plugin meta、未実装の機能、未取得URLを作らない。原資料・個人情報をpayloadへコピーしない。
