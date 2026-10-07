# A25 WordPress Draft Agent

A25は同じ`content_id`のA08記事・A11画像・QAを、WordPress下書き用のpayloadとmedia手順にまとめる。現在はdry-runのみ。WordPress接続、画像upload、記事作成、公開、Schedulingは実行しない。

Flow: A08 → A11 → A29 → A32 → A28 → **A25 Draft** → Human Approval → Publish。下書き準備にはQA全PASSが必要。公開のHuman Approvalを下書き前の条件へ流用しない。公開処理自体は未実装。

[inputs](inputs.md)・[outputs](outputs.md)・[rules](rules.md)・[workflow](workflow.md)と[prompt](prompts/draft_preparation.md)を参照。実装は`fortune_labo/editorial/wordpress_draft.py`、契約は[Draft Payload Schema](schemas/draft_payload.schema.json)と[Media Receipt Schema](schemas/media_receipt.schema.json)。

画像未生成・実attachment ID未取得・QA未完了の状態でもreview用`proposed_payload`を返す。`request_payload`はnull、`payload_ready`はfalseに保ち、架空のattachment IDやWordPress記事URLを作らない。
