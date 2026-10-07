# Integrations

入力: A08 article/blueprint、A11 image plan/verified assets、A29/A32/A28 QA。出力: WordPress Draft payload/media計画、Content Indexへの将来のpost/media ID返却記録。公開後のWordPress → Index → raw Performance → A07 feedbackは別の既存契約に従う。

正式field名は[WordPress Posts REST reference](https://developer.wordpress.org/rest-api/reference/posts/)に従う。mediaの`alt_text`, `caption`, `post`と返却される`id`/`source_url`は[Media REST reference](https://developer.wordpress.org/rest-api/reference/media/)を確認した。個別metaのREST公開/書込みはサイト側登録が必要なので、[REST metadata拡張の公式説明](https://developer.wordpress.org/rest-api/extending-the-rest-api/modifying-responses/)を根拠に明示設定を要求する。確認日: 2026-10-07。

論理metadataから実keyへのmapping例は、接続先で登録を確認した後だけ使用する:

```json
{
  "site_id": "operator-assigned-site-id",
  "meta_mapping": {"content_id": "verified_registered_key"},
  "registered_meta": {
    "verified_registered_key": {
      "type": "string",
      "rest_writable": true,
      "registration_reference": "private-site-capability-record"
    }
  }
}
```

上記は設定shapeの説明であり、実サイトにこのkeyが登録済みという意味ではない。接続先URL、credentials、Application Password、認証処理、write transportは今回含めない。
