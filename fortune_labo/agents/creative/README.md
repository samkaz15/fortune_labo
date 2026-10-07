# A11 Creative Agent

A11は、保存済みArticle DraftとBlueprintから画像の役割を考え、検証可能なImage Planと実アセットをA25へ渡す後段工程である。A07/A08のBrief・Draft・runを画像追加のために変更しない。

[Visual Identity](../../../docs/editorial/VISUAL_IDENTITY.md) `visual-style-0.1.0` が表現の基準。featuredは原則1枚、全H2について画像が理解を助けるか検討する。本文・表・既存図で十分な節は、理由を記したNO_IMAGEを選ぶ。画像枚数や装飾を増やすために生成しない。

[inputs](inputs.md)、[rules](rules.md)、[workflow](workflow.md)、[outputs](outputs.md) と [Image Plan prompt](prompts/image_plan.md) を使用する。実行補助は `fortune_labo/editorial/creative.py`。外部モデルや画像生成APIを隠れて呼び出すことはなく、実際の生成は明示した外部ツールまたはnative図制作で行う。

planとasset referenceのschemaは [schemas](schemas)。コードは記事と図の意味的整合・出典の真偽・実画の品質を保証しないため、保存した実画像を人またはモデルが視覚確認し、A29/A32/A28のQAへ結果を渡す。
