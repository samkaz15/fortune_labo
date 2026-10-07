# A07 — Inputs

| 入力 | 扱い |
|---|---|
| A06 Content Brief / SEO Opportunity | 元契約を保持。未発行はnull。A06要件を黙って広げない |
| Content Index | ID、記事状態、genre、検索意図、アクセス区分、既存記事と候補リンク |
| Content Intelligence | 安全に構造化されたgenreと出典ID。原文転載や非公開URLは不要 |
| Performance | 4目的のraw metricを分離。nullは未測定、0は観測ゼロ。出所未検証の入力はsupplied_not_independently_verified |
| Content Opportunities | opportunity_id、根拠、候補区分、既存記事とのoverlap、inventory completeness |
| FREE_PREMIUM_RULES | アクセス区分の正本。参照とSHA-256をaccess_basisへ保存 |
| SEO_POLICY_REGISTER | 記事に適用できるscopeとversion。変更検知から承認なしでversion更新しない |
| decision | モデルまたは担当者が作る編集判断。具体的な回答・outline・access判定・選定理由 |

機会候補を与えた場合はdecision.selection.opportunity_idを必須とし、そのID・genre・topic・keyword・intent・access候補を照合する。根拠のない候補、重複未解決、存在しないIDを拒否する。今回のユーザー指定再生成のように候補一覧を使わない場合だけ、offline_selection_reasonを明記し、gapを検証した扱いにしない。

全入力は呼出側のオブジェクトを変更せず、hashで追跡する。Performanceと機会は省略可能だが、省略を測定ゼロや機会不存在へ変換しない。

実測を渡す場合はperformance={observations:[...], selection:{period_start,period_end,timezone,filters,dimensions}}を使う。adapterは期間・timezone・filter・dimension・definition版の混在と、同一metricの複数供給を拒否する。raw_observationsにsource、unit、定義、集計方法、採取時刻を保持し、A07へ単位のない値だけを渡さない。scroll_depthは新Raw観測契約のpercent（0–100）、ctrとengagement_rateはratio（0–1）。旧grouped形式は全nullの未測定値のみ許可する。
