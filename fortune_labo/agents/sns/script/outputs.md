# Script Agent — Outputs

出力はすべて `schemas/` に準拠します。自由形式は下流が受け取りません。

## 成果物一覧

| 成果物 | スキーマ | 受け取る側 |
| --- | --- | --- |
| **動画台本** | `video_script.schema.json` | A28 QA → 人間承認 → 撮影 |
| **事実確認依頼** | `video_fact_check_request.schema.json` | A29（A28 経由） |
| **パフォーマンス記録** | `video_performance.schema.json` | A18 ⇄ Script Agent |
| バッチ台本ファイル | Markdown `content/video/scripts/<YYYY-MM>/` | 人間のレビュー面 |

---

## 動画台本の構造

```
メタ      id / status / format / tier / theme / target / basis
フック    3層（視覚・音声・テロップ）＋候補3案＋選定理由
本文      話し言葉の台本
ショット  時系列のショットリスト（素材種別つき）
尺        音声文字数・想定尺・枠
事実      クレームごとの検証状態と出典候補
撮影      許諾ステータス・参拝記録ID・制約
遵法      rules.md §2 の自己点検結果
CTA       型と文言
展開      多尺展開の親子関係
```

X の `x_post.schema.json` に対応する追加項目：

| 追加項目 | 理由 |
| --- | --- |
| `shot_list` | 何を撮るかが決まらないと撮影に渡せない |
| `filming` | 許諾・参拝記録・撮影制約。**未確認なら撮影に進まない** |
| `duration` | 文字数と尺の整合。機械検査できる |
| `hook.visual / audio / caption` | 3層すべてを持つことを構造で強制 |
| `ai_generated_ratio` | AI素材の比率。過半なら一次情報が薄い |
| `derived_from` | 多尺展開の親子 |

`basis` / `factual_claims` / `compliance` は X から継承。**空の `basis` は
出力できません。**

---

## 受け渡し

**→ A28 QA**

台本＋事実確認依頼を渡します。ゲート順は継承：

```
コンプライアンス → 事実 → 一次情報 → 編集 → SEO → 技術
```

動画では**撮影可否**がコンプライアンスの一部として最初に見られます。
許諾が無ければ、内容の良し悪し以前に止まります。

**→ A29 Fact-Check**

`video_fact_check_request`。テロップに出す事実は `criticality` を1段上げて
渡してください。画面に焼き付く情報は取り消しが効きません。

**→ 人間（撮影）**

台本＋ショットリスト＋撮影前チェックの結果。
**チェックが1つでも未完なら渡しません。**

**→ A11 Creative Agent**

ショットリストを渡し、ビジュアル設計を受け取ります。
Script Agent は構図・光・色を指定しません。

**→ A18 Analytics**

公開後、`id` / `format` / `tier` / `hook_pattern` / `cta_type` を渡し、
**制作判断の単位で**性能を分解できるようにします。

**→ A08 Content Production**

長尺台本は記事の原稿になります。逆に記事は台本のテーマ源です。

---

## バッチファイル

`content/video/scripts/<YYYY-MM>/` に Markdown で出力します。
`content/sns/drafts/` の形式を踏襲：

```
## <ID> ｜ <theme> ｜ <format> / <tier>
- 狙い / 尺 / basis / 依存プレースホルダ
- 事実確認: 要・対象クレーム
- 撮影: 許諾ステータス・参拝記録ID
- status

### フック（0:00-0:03）
  視覚 / 音声 / テロップ

### 台本
（話し言葉・ルビ・間つき）

### ショットリスト
| 時間 | 画 | 音声 | テロップ | 素材 |
```

**JSONが正本、Markdownは人間のレビュー面。**Markdownは JSON から生成し、
個別に編集しません。

---

## レポート

```
1. Tier 1  リスト登録・鑑定予約への寄与
2. Tier 2  3秒維持率・平均維持率・保存・プロフィール遷移
3. Tier 3  再生数・いいね（診断のみ）
4. 何が効いたか  フック型 / Tier / フォーマット別
5. 制作の実態    書いた本数・撮れた本数・滞留
6. エスカレーション
7. 仮説台帳
```

5 が動画固有です。**書いた本数と撮れた本数の差**が、この工程の健全性を
最もよく表します。
