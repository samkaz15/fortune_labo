#!/usr/bin/env python3
"""A10-SC Script Agent の成果物を検証する。

JSON Schema だけでは見られない「項目をまたいだ整合」をここで見る。動画で最も
多い失敗は、台本単体では正しく見えるのに撮影に渡すと破綻しているもの —
枠に収まらない尺、飛んでいるショット、許諾と合わないショットリスト。

使い方:
    python3 validate.py                      # ../examples/*.json を検証
    python3 validate.py path/to/script.json  # 指定したファイルを検証

id の接頭辞で種別を判定する: VS- / VFC- / VPERF-
すべて妥当なら終了コード 0、そうでなければ 1。

必要: jsonschema (pip install jsonschema)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    sys.exit("jsonschema が必要です: pip install jsonschema")

SCHEMA_DIR = Path(__file__).resolve().parent

SCHEMA_BY_PREFIX = [
    ("VPERF-", "video_performance.schema.json"),
    ("VFC-", "video_fact_check_request.schema.json"),
    ("VS-", "video_script.schema.json"),
]

# 日本語ナレーションの読み上げ速度。writing.md §8 と formats.md の根拠。
CHARS_PER_MINUTE = 325
DURATION_TOLERANCE = 0.15  # ±15%（kpi.md の duration_accuracy）

FORMAT_LIMIT_SEC = {
    "tiktok": 60,
    "reels": 90,
    "shorts": 60,
    "youtube_long": 720,
}

LOCATION_SOURCE = "現地撮影"
AI_SOURCES = {"図解", "イメージ"}


def schema_for(artifact: dict) -> tuple[str, dict]:
    artifact_id = artifact.get("id", "")
    for prefix, filename in SCHEMA_BY_PREFIX:
        if artifact_id.startswith(prefix):
            return filename, json.loads((SCHEMA_DIR / filename).read_text())
    raise ValueError(f"id の接頭辞が不明です: {artifact_id!r} (VS- / VFC- / VPERF-)")


def check_script(s: dict) -> list[str]:
    """video_script のみに適用する項目間の整合検査。"""
    problems: list[str] = []
    shots = s.get("shot_list") or []
    duration = s.get("duration") or {}
    filming = s.get("filming") or {}

    # --- 尺 ---------------------------------------------------------------
    chars = duration.get("narration_chars")
    estimated = duration.get("estimated_sec")
    limit = duration.get("format_limit_sec")
    fmt = s.get("format")

    if chars is not None and estimated is not None:
        derived = chars / CHARS_PER_MINUTE * 60
        if derived > 0 and abs(estimated - derived) / derived > 0.10:
            problems.append(
                f"estimated_sec {estimated} が narration_chars {chars} と合いません "
                f"({CHARS_PER_MINUTE}字/分なら {derived:.1f}秒)"
            )

    if fmt in FORMAT_LIMIT_SEC and limit is not None and limit != FORMAT_LIMIT_SEC[fmt]:
        problems.append(f"format_limit_sec {limit} が {fmt} の上限 {FORMAT_LIMIT_SEC[fmt]}秒 と違います")

    if estimated is not None and limit is not None and estimated > limit:
        problems.append(
            f"想定尺 {estimated:.1f}秒 が枠 {limit}秒 を超えています。"
            "早口にするのではなく内容を削ること（writing.md §8）"
        )

    actual = duration.get("actual_sec")
    if actual is not None and estimated:
        gap = abs(actual - estimated) / estimated
        if gap > DURATION_TOLERANCE:
            problems.append(
                f"実尺 {actual}秒 と想定 {estimated:.1f}秒 の乖離が {gap:.0%} です。"
                "文字数係数の見直しが必要（kpi.md duration_accuracy）"
            )

    # --- ショットリスト ---------------------------------------------------
    prev_to = None
    for i, shot in enumerate(shots):
        a, b = shot.get("from_sec"), shot.get("to_sec")
        if a is not None and b is not None and b <= a:
            problems.append(f"shot_list[{i}]: to_sec {b} が from_sec {a} 以下です")
        if prev_to is not None and a is not None and abs(a - prev_to) > 0.01:
            problems.append(
                f"shot_list[{i}]: {prev_to}秒 の次が {a}秒 から始まっています（間が飛ぶか重なっています）"
            )
        prev_to = b

    if shots and estimated is not None and prev_to is not None:
        if abs(prev_to - estimated) / max(estimated, 1) > 0.20:
            problems.append(
                f"ショットリストの総尺 {prev_to}秒 と想定尺 {estimated:.1f}秒 が20%以上ずれています"
            )

    # --- 撮影許諾とショットリストの一致 -----------------------------------
    has_location = any(shot.get("source") == LOCATION_SOURCE for shot in shots)
    declared = filming.get("requires_location_shoot")

    if has_location and declared is False:
        problems.append(
            "shot_list に 現地撮影 があるのに filming.requires_location_shoot が false です"
        )
    if declared is True and not has_location:
        problems.append(
            "filming.requires_location_shoot が true ですが shot_list に 現地撮影 がありません"
        )

    if has_location and s.get("status") != "blocked":
        if filming.get("permission_status") != "confirmed_video_commercial":
            problems.append(
                f"現地撮影があるのに撮影許諾が {filming.get('permission_status')!r} です。"
                "写真の許諾は動画の許諾ではありません（rules.md §4.1）"
            )
        if not filming.get("visit_record_id"):
            problems.append("現地撮影があるのに visit_record_id がありません（rules.md §4.1）")

    # --- AI素材の比率 ------------------------------------------------------
    total = sum(
        (shot.get("to_sec", 0) - shot.get("from_sec", 0))
        for shot in shots
        if shot.get("to_sec") is not None and shot.get("from_sec") is not None
    )
    ai_sec = sum(
        (shot.get("to_sec", 0) - shot.get("from_sec", 0))
        for shot in shots
        if shot.get("source") in AI_SOURCES
    )
    if total > 0:
        derived_ratio = ai_sec / total
        declared_ratio = s.get("ai_generated_ratio")
        if declared_ratio is not None and abs(declared_ratio - derived_ratio) > 0.02:
            problems.append(
                f"ai_generated_ratio {declared_ratio} がショットリストの実測 {derived_ratio:.2f} と違います"
            )
        if derived_ratio > 0.5:
            problems.append(
                f"AI生成素材が {derived_ratio:.0%} を占めています。"
                "一次情報が薄く、一行テストに落ちる可能性があります（positioning.md §8）"
            )

    # --- フック -----------------------------------------------------------
    hook = s.get("hook") or {}
    if hook.get("silent_viable") is False:
        problems.append(
            "hook.silent_viable が false です。無音で意味が通らないフックは"
            "実質半分しか届きません（writing.md §3）"
        )

    return problems


def validate_file(path: Path) -> list[str]:
    artifact = json.loads(path.read_text())
    _, schema = schema_for(artifact)
    problems = [
        f"{'.'.join(str(p) for p in e.path) or '(root)'}: {e.message}"
        for e in sorted(Draft202012Validator(schema).iter_errors(artifact), key=lambda e: list(e.path))
    ]
    if artifact.get("id", "").startswith("VS-"):
        problems += check_script(artifact)
    return problems


def main(argv: list[str]) -> int:
    for _, name in SCHEMA_BY_PREFIX:
        Draft202012Validator.check_schema(json.loads((SCHEMA_DIR / name).read_text()))

    targets = [Path(a) for a in argv[1:]] or sorted((SCHEMA_DIR.parent / "examples").glob("*.json"))
    if not targets:
        print("検証対象がありません")
        return 0

    failed = 0
    for path in targets:
        problems = validate_file(path)
        if problems:
            failed += 1
            print(f"NG  {path.name}")
            for p in problems:
                print(f"    {p}")
        else:
            print(f"ok  {path.name}")

    print(f"\n{len(targets) - failed}/{len(targets)} 件が妥当")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
