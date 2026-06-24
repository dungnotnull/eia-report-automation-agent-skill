
# -*- coding: utf-8 -*-
"""test_runner.py - regression test runner for the eia-report-automation harness.

This runner loads scenario fixtures, validates JSON schemas, checks that all
quality gates are represented, and ensures the knowledge_updater tool is
syntactically importable. It does not execute live WebSearch/crawl calls.

Usage:
  python tests/test_runner.py
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import re
import sys
from typing import Any, Dict, List

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIXTURES_DIR = ROOT / "tests" / "fixtures"
SCHEMA_DIR = ROOT / "schema"


def load_json(path: pathlib.Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def validate_schema(obj: Any, schema: Dict[str, Any], path: str = "$") -> List[str]:
    errors: List[str] = []
    stype = schema.get("type")
    if stype == "object":
        if not isinstance(obj, dict):
            errors.append(f"{path}: expected object")
            return errors
        required = schema.get("required", [])
        for key in required:
            if key not in obj:
                errors.append(f"{path}: missing required key {key}")
        props = schema.get("properties", {})
        for key, subschema in props.items():
            if key in obj:
                errors.extend(validate_schema(obj[key], subschema, f"{path}.{key}"))
    elif stype == "array":
        if not isinstance(obj, list):
            errors.append(f"{path}: expected array")
            return errors
        item_schema = schema.get("items")
        for i, item in enumerate(obj):
            errors.extend(validate_schema(item, item_schema, f"{path}[{i}]"))
    elif stype == "string":
        if not isinstance(obj, str):
            errors.append(f"{path}: expected string")
    elif stype == "number":
        if not isinstance(obj, (int, float)):
            errors.append(f"{path}: expected number")
    elif stype == "boolean":
        if not isinstance(obj, bool):
            errors.append(f"{path}: expected boolean")
    enum = schema.get("enum")
    if enum is not None and obj not in enum:
        errors.append(f"{path}: value {obj!r} not in enum {enum}")
    return errors


def check_brain() -> List[str]:
    errors = []
    brain = ROOT / "SECOND-KNOWLEDGE-BRAIN.md"
    if not brain.exists():
        errors.append("SECOND-KNOWLEDGE-BRAIN.md missing")
        return errors
    text = brain.read_text(encoding="utf-8")
    if "Leopold matrix" not in text:
        errors.append("Brain missing Leopold matrix framework")
    if "RIAM" not in text:
        errors.append("Brain missing RIAM framework")
    if not re.search(r"\d{4}-\d{2}-\d{2}", text):
        errors.append("Brain missing date-stamped update log")
    return errors


def check_knowledge_updater() -> List[str]:
    errors = []
    tool = ROOT / "tools" / "knowledge_updater.py"
    spec = importlib.util.spec_from_file_location("knowledge_updater", tool)
    if spec is None or spec.loader is None:
        errors.append("Cannot load knowledge_updater.py spec")
        return errors
    try:
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as exc:
        errors.append(f"knowledge_updater.py import failed: {exc}")
    return errors



def check_skills() -> List[str]:
    errors = []
    required = [
        "skills/main.md",
        "skills/sub-requirements-gatherer.md",
        "skills/sub-risk-screener.md",
        "skills/sub-compliance-check.md",
        "skills/sub-standards-updater.md",
        "skills/sub-improvement-roadmap.md",
    ]
    for rel in required:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"Missing skill file: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        if "Quality Gate" not in text:
            errors.append(f"{rel} missing Quality Gate section")
        if "Input" not in text and "Inputs" not in text:
            errors.append(f"{rel} missing Inputs section")
        if "Output" not in text and "Outputs" not in text:
            errors.append(f"{rel} missing Outputs section")
    main = ROOT / "skills" / "main.md"
    if main.exists():
        text = main.read_text(encoding="utf-8")
        for gate in ["COMPLIANCE GATE", "EVIDENCE GATE", "FRAMEWORK GATE", "CHALLENGE GATE"]:
            if gate not in text:
                errors.append(f"main.md missing gate: {gate}")
    return errors


def check_scenario(schema: Dict[str, Any], scenario_file: pathlib.Path) -> List[str]:
    errors = []
    try:
        fixture = load_json(scenario_file)
    except Exception as exc:
        errors.append(f"{scenario_file.name}: cannot parse JSON: {exc}")
        return errors
    input_errors = validate_schema(fixture.get("input", {}), schema.get("input_schema", {}))
    for e in input_errors:
        errors.append(f"{scenario_file.name}: input {e}")
    expected = fixture.get("expected_output", {})
    output_errors = validate_schema(expected, schema.get("output_schema", {}))
    for e in output_errors:
        errors.append(f"{scenario_file.name}: expected_output {e}")
    checks = fixture.get("checks", {})
    if checks.get("requires_disclaimer") and not expected.get("disclaimer"):
        errors.append(f"{scenario_file.name}: expected disclaimer")
    if checks.get("approval_blocked") and expected.get("executive_summary", {}).get("verdict", "").lower().startswith("approve"):
        errors.append(f"{scenario_file.name}: verdict must not be approval")
    return errors


def main() -> int:
    errors: List[str] = []
    errors.extend(check_skills())
    errors.extend(check_brain())
    errors.extend(check_knowledge_updater())

    schema_path = SCHEMA_DIR / "shared-eia-schema.json"
    if schema_path.exists():
        schema = load_json(schema_path)
    else:
        schema = {}
        errors.append("shared-eia-schema.json missing")

    for fixture in sorted(FIXTURES_DIR.glob("scenario_*.json")):
        errors.extend(check_scenario(schema, fixture))

    if errors:
        print("FAILURES:")
        for e in errors:
            print(" -", e)
        return 1

    print("OK: all skill files, brain, knowledge_updater, schema, and scenario fixtures validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
