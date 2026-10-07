# A07 Content Strategy Agent

A07は「何を、誰のどの疑問に答えるために書くか」を決める。A06、Content Index、Content Intelligence、目的別Performance、Content Opportunitiesを照合し、根拠と未確定事項を保持したA08用Briefを作る。

[mission](mission.md) → [inputs](inputs.md) → [rules](rules.md) → [workflow](workflow.md) → [outputs](outputs.md) の順に読む。[プロンプト](prompts/brief.md) はモデル・担当者の判断手順、[v2 schema](schemas/brief.schema.json) は引継ぎ形式、`fortune_labo/editorial/strategy.py` は決定済みの内容を検証・組み立てる実行補助である。コードがモデルの代わりに戦略や文章を創作するものではない。

実行補助は今回許可されたoffline_testのみを扱う。新方針への方向性承認は、既存A06の制約解除・安定版SEO policy承認・顧客向け公開承認を意味しない。既存A06と旧v1 Brief契約は変更しない。v2は役割別根拠、FREE/PREMIUM判定、機会選定、入力hashを追加する別契約である。

本文、個人情報、非公開調査原文、元資料の非公開URLはpublic Gitへ入れない。今回ユーザーが明示的に許可した3本のDraft/Fixtureだけは、根拠を安全なIDへ置換し、公開前検査を通したうえで保存できる。顧客向け公開とは別である。
