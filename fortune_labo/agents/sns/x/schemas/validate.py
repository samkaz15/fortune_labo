#!/usr/bin/env python3
"""Validate X Content Agent artifacts against the schemas in this directory.

A schema nobody runs is documentation, not a gate. This makes the rules in
agents/sns/x/rules.md actually enforceable before a post reaches QA.

Usage:
    python3 validate.py                    # validate ../examples/*.json
    python3 validate.py path/to/post.json  # validate specific files

Artifact type is taken from the "id" prefix: X- / XPLAN- / XFC- / XPERF-.
Exit status is 0 when everything validates, 1 otherwise.

Requires: jsonschema (pip install jsonschema)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    sys.exit("jsonschema is required: pip install jsonschema")

SCHEMA_DIR = Path(__file__).resolve().parent

# Longest prefix first — "XPLAN-" must be tested before "X-".
SCHEMA_BY_PREFIX = [
    ("XPLAN-", "x_content_plan.schema.json"),
    ("XPERF-", "x_performance_record.schema.json"),
    ("XFC-", "x_fact_check_request.schema.json"),
    ("X-", "x_post.schema.json"),
]


def schema_for(artifact: dict) -> tuple[str, dict]:
    artifact_id = artifact.get("id", "")
    for prefix, filename in SCHEMA_BY_PREFIX:
        if artifact_id.startswith(prefix):
            return filename, json.loads((SCHEMA_DIR / filename).read_text())
    raise ValueError(f"unknown artifact id {artifact_id!r} (expected X- / XPLAN- / XFC- / XPERF- prefix)")


def validate_file(path: Path) -> list[str]:
    artifact = json.loads(path.read_text())
    filename, schema = schema_for(artifact)
    validator = Draft202012Validator(schema)
    problems = []
    for error in sorted(validator.iter_errors(artifact), key=lambda e: list(e.path)):
        location = ".".join(str(p) for p in error.path) or "(root)"
        problems.append(f"{location}: {error.message}")
    return problems


def main(argv: list[str]) -> int:
    for name in (f for _, f in SCHEMA_BY_PREFIX):
        Draft202012Validator.check_schema(json.loads((SCHEMA_DIR / name).read_text()))

    targets = [Path(a) for a in argv[1:]] or sorted((SCHEMA_DIR.parent / "examples").glob("*.json"))
    if not targets:
        print("nothing to validate")
        return 0

    failed = 0
    for path in targets:
        problems = validate_file(path)
        if problems:
            failed += 1
            print(f"FAIL  {path.name}")
            for problem in problems:
                print(f"      {problem}")
        else:
            print(f"ok    {path.name}")

    print(f"\n{len(targets) - failed}/{len(targets)} valid")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
