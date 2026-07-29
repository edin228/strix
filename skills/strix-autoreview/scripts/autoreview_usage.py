from __future__ import annotations

import json
from typing import Any


TOKEN_FIELDS = (
    "input_tokens",
    "cached_input_tokens",
    "cache_write_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
)


def _nonnegative_int(value: object) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def _jsonl_events(raw: str) -> tuple[list[dict[str, Any]], int]:
    events: list[dict[str, Any]] = []
    malformed = 0
    for line in raw.splitlines():
        text = line.strip()
        if not text:
            continue
        try:
            value = json.loads(text)
        except json.JSONDecodeError:
            malformed += 1
            continue
        if not isinstance(value, dict):
            malformed += 1
            continue
        events.append(value)
    return events, malformed


def parse_usage_metrics(
    raw: str,
    *,
    elapsed_seconds: float,
    prompt_chars: int,
    model: str | None,
    reasoning_effort: str | None,
    process_exit_code: int,
) -> dict[str, Any]:
    events, malformed = _jsonl_events(raw)
    usage_events = [
        event["usage"]
        for event in events
        if event.get("type") == "turn.completed"
        and isinstance(event.get("usage"), dict)
    ]

    token_values: dict[str, int | None] = {}
    for field in TOKEN_FIELDS:
        values = [_nonnegative_int(usage.get(field)) for usage in usage_events]
        token_values[field] = (
            sum(value for value in values if value is not None)
            if values and all(value is not None for value in values)
            else None
        )

    input_tokens = token_values["input_tokens"]
    output_tokens = token_values["output_tokens"]
    if input_tokens == 0 and output_tokens == 0:
        token_values = {field: None for field in TOKEN_FIELDS}
        input_tokens = None
        output_tokens = None
    token_usage_available = (
        input_tokens is not None
        and input_tokens > 0
        and output_tokens is not None
        and output_tokens > 0
    )
    total_tokens = (
        input_tokens + output_tokens if token_usage_available else None
    )

    return {
        "schema_version": 1,
        "token_usage_available": token_usage_available,
        **token_values,
        "total_tokens": total_tokens,
        "elapsed_seconds": round(max(0.0, elapsed_seconds), 3),
        "prompt_chars": max(0, prompt_chars),
        "model": model,
        "reasoning_effort": reasoning_effort,
        "usage_event_count": len(usage_events),
        "malformed_event_count": malformed,
        "process_exit_code": process_exit_code,
    }


def extract_last_agent_message(raw: str) -> str:
    events, _malformed = _jsonl_events(raw)
    messages = [
        item["text"]
        for event in events
        if event.get("type") == "item.completed"
        and isinstance(event.get("item"), dict)
        and (item := event["item"]).get("type") == "agent_message"
        and isinstance(item.get("text"), str)
    ]
    return messages[-1] if messages else ""


def format_usage_metrics(metrics: dict[str, Any]) -> str:
    return json.dumps(metrics, sort_keys=True, separators=(",", ":"))
