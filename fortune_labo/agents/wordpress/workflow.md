# Workflow

1. A08 source article、A11 validated image plan、同版QAを読み、hash/ID/版を照合する。
2. QA全PASSと根拠参照を確認する。公開用Human Approvalは後段で扱う。
3. sourceを変えずHTMLを組み立て、featured/inline mediaの位置・alt/captionを準備する。
4. 生成済みassetをsite/content/hashでまとめ、既存upload receiptを照合する。未uploadは計画を残す。
5. 接続後の将来手順は media upload → 実attachment ID response保存 → draft request準備 → 実draft post ID response保存 → media `post` association。現実装は各payloadを組み立てるのみ。
6. WordPress Draftを人間が確認し、別工程で公開承認する。A25にPublish/Scheduleの実行口はない。

`association_plan(envelope, post_receipt)`はhash固定済みpackageと同site/content IDのdraft responseから`/wp/v2/media/{id}`への`{"post": received_post_id}`を組み立てる。送信しない。`execute_draft`は常に未接続エラーを返すため、previewを渡してもnetwork writeは発生しない。
