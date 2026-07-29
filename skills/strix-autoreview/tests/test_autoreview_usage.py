from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from autoreview_usage import (  # noqa: E402
    extract_last_agent_message,
    format_usage_metrics,
    parse_usage_metrics,
)


class AutoreviewUsageTests(unittest.TestCase):
    def test_parses_usage_and_keeps_cached_tokens_separate(self) -> None:
        raw = "\n".join(
            [
                '{"type":"thread.started","thread_id":"thread-1"}',
                '{"type":"turn.completed","usage":{"input_tokens":150,'
                '"cached_input_tokens":100,"cache_write_input_tokens":5,'
                '"output_tokens":20,"reasoning_output_tokens":12}}',
            ]
        )

        metrics = parse_usage_metrics(
            raw,
            elapsed_seconds=1.23456,
            prompt_chars=4321,
            model="review-model",
            reasoning_effort="high",
            process_exit_code=0,
        )

        self.assertTrue(metrics["token_usage_available"])
        self.assertEqual(metrics["input_tokens"], 150)
        self.assertEqual(metrics["cached_input_tokens"], 100)
        self.assertEqual(metrics["cache_write_input_tokens"], 5)
        self.assertEqual(metrics["output_tokens"], 20)
        self.assertEqual(metrics["reasoning_output_tokens"], 12)
        self.assertEqual(metrics["total_tokens"], 170)
        self.assertEqual(metrics["elapsed_seconds"], 1.235)
        self.assertEqual(metrics["prompt_chars"], 4321)
        self.assertEqual(metrics["usage_event_count"], 1)

    def test_aggregates_complete_usage_events(self) -> None:
        raw = "\n".join(
            [
                '{"type":"turn.completed","usage":{"input_tokens":10,'
                '"cached_input_tokens":2,"cache_write_input_tokens":0,'
                '"output_tokens":3,"reasoning_output_tokens":1}}',
                '{"type":"turn.completed","usage":{"input_tokens":20,'
                '"cached_input_tokens":4,"cache_write_input_tokens":1,'
                '"output_tokens":5,"reasoning_output_tokens":2}}',
            ]
        )

        metrics = parse_usage_metrics(
            raw,
            elapsed_seconds=2,
            prompt_chars=100,
            model=None,
            reasoning_effort=None,
            process_exit_code=0,
        )

        self.assertEqual(metrics["input_tokens"], 30)
        self.assertEqual(metrics["cached_input_tokens"], 6)
        self.assertEqual(metrics["output_tokens"], 8)
        self.assertEqual(metrics["reasoning_output_tokens"], 3)
        self.assertEqual(metrics["total_tokens"], 38)
        self.assertEqual(metrics["usage_event_count"], 2)

    def test_missing_usage_is_explicitly_unavailable(self) -> None:
        metrics = parse_usage_metrics(
            '{"type":"turn.started"}',
            elapsed_seconds=0.5,
            prompt_chars=50,
            model="gpt-test",
            reasoning_effort="medium",
            process_exit_code=0,
        )

        self.assertFalse(metrics["token_usage_available"])
        self.assertIsNone(metrics["input_tokens"])
        self.assertIsNone(metrics["total_tokens"])
        self.assertEqual(metrics["elapsed_seconds"], 0.5)
        self.assertEqual(metrics["usage_event_count"], 0)

    def test_zero_filled_fallback_usage_is_unavailable(self) -> None:
        metrics = parse_usage_metrics(
            '{"type":"turn.completed","usage":{"input_tokens":0,'
            '"cached_input_tokens":0,"cache_write_input_tokens":0,'
            '"output_tokens":0,"reasoning_output_tokens":0}}',
            elapsed_seconds=1,
            prompt_chars=50,
            model="gpt-test",
            reasoning_effort="medium",
            process_exit_code=0,
        )

        self.assertFalse(metrics["token_usage_available"])
        self.assertIsNone(metrics["input_tokens"])
        self.assertIsNone(metrics["cached_input_tokens"])
        self.assertIsNone(metrics["output_tokens"])
        self.assertIsNone(metrics["total_tokens"])
        self.assertEqual(metrics["usage_event_count"], 1)

    def test_partial_or_malformed_usage_never_underreports(self) -> None:
        raw = "\n".join(
            [
                "not json",
                '{"type":"turn.completed","usage":{"input_tokens":10,'
                '"cached_input_tokens":2,"output_tokens":3,'
                '"reasoning_output_tokens":1}}',
                '{"type":"turn.completed","usage":{"input_tokens":5,'
                '"cached_input_tokens":1,"cache_write_input_tokens":0,'
                '"output_tokens":"bad","reasoning_output_tokens":0}}',
            ]
        )

        metrics = parse_usage_metrics(
            raw,
            elapsed_seconds=1,
            prompt_chars=25,
            model=None,
            reasoning_effort=None,
            process_exit_code=0,
        )

        self.assertFalse(metrics["token_usage_available"])
        self.assertEqual(metrics["input_tokens"], 15)
        self.assertIsNone(metrics["cache_write_input_tokens"])
        self.assertIsNone(metrics["output_tokens"])
        self.assertIsNone(metrics["total_tokens"])
        self.assertEqual(metrics["malformed_event_count"], 1)

    def test_nonzero_process_is_recorded_without_losing_usage(self) -> None:
        metrics = parse_usage_metrics(
            '{"type":"turn.completed","usage":{"input_tokens":4,'
            '"cached_input_tokens":0,"cache_write_input_tokens":0,'
            '"output_tokens":2,"reasoning_output_tokens":0}}',
            elapsed_seconds=3,
            prompt_chars=10,
            model="gpt-test",
            reasoning_effort="low",
            process_exit_code=17,
        )

        self.assertTrue(metrics["token_usage_available"])
        self.assertEqual(metrics["process_exit_code"], 17)
        self.assertEqual(metrics["total_tokens"], 6)

    def test_extracts_last_agent_message_and_formats_stable_json(self) -> None:
        raw = "\n".join(
            [
                '{"type":"item.completed","item":{"type":"agent_message",'
                '"text":"first"}}',
                "malformed",
                '{"type":"item.completed","item":{"type":"agent_message",'
                '"text":"second"}}',
            ]
        )

        self.assertEqual(extract_last_agent_message(raw), "second")
        self.assertEqual(
            format_usage_metrics({"b": 2, "a": 1}),
            '{"a":1,"b":2}',
        )


if __name__ == "__main__":
    unittest.main()
