from __future__ import annotations

from typing import Any


REPORT_KEYS = {
    "findings",
    "overall_correctness",
    "overall_explanation",
    "overall_confidence",
}
FINDING_KEYS = {
    "title",
    "body",
    "priority",
    "confidence",
    "category",
    "code_location",
}


def _confidence(value: object) -> bool:
    return (
        not isinstance(value, bool)
        and isinstance(value, (int, float))
        and 0 <= value <= 1
    )


def report_schema_error(value: object) -> str | None:
    if not isinstance(value, dict) or set(value) != REPORT_KEYS:
        return "review output must contain exactly the report schema keys"
    if value["overall_correctness"] not in {"patch is correct", "patch is incorrect"}:
        return "review output has invalid overall_correctness"
    if not isinstance(value["overall_explanation"], str):
        return "review output overall_explanation must be a string"
    if not _confidence(value["overall_confidence"]):
        return "review output overall_confidence must be a number from 0 to 1"
    if not isinstance(value["findings"], list):
        return "review findings must be an array"
    for index, finding in enumerate(value["findings"], start=1):
        if not isinstance(finding, dict) or set(finding) != FINDING_KEYS:
            return f"finding {index} must contain exactly the finding schema keys"
        if not isinstance(finding["title"], str) or not isinstance(finding["body"], str):
            return f"finding {index} title and body must be strings"
        if finding["priority"] not in {"P0", "P1", "P2", "P3"}:
            return f"finding {index} has invalid priority"
        if not _confidence(finding["confidence"]):
            return f"finding {index} confidence must be a number from 0 to 1"
        if finding["category"] not in {
            "bug",
            "security",
            "regression",
            "test_gap",
            "maintainability",
        }:
            return f"finding {index} has invalid category"
        location = finding["code_location"]
        if not isinstance(location, dict) or set(location) != {"file_path", "line"}:
            return f"finding {index} has invalid code_location"
        if not isinstance(location["file_path"], str):
            return f"finding {index} file_path must be a string"
        if (
            isinstance(location["line"], bool)
            or not isinstance(location["line"], int)
            or location["line"] < 1
        ):
            return f"finding {index} line must be a positive integer"
    return None
