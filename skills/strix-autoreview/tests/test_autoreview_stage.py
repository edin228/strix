from __future__ import annotations

import argparse
import io
import json
import os
import runpy
import stat
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import autoreview_stage


FAKE_AUTOREVIEW = """\
#!/usr/bin/env python3
import hashlib
import json
import pathlib
import sys
import time

args = sys.argv[1:]
def fingerprint():
    digest = hashlib.sha256(pathlib.Path("tracked.txt").read_bytes())
    for option in ("--prompt", "--prompt-file", "--dataset", "--scope-path"):
        for index, value in enumerate(args):
            if value != option:
                continue
            supplied = args[index + 1]
            digest.update(option.encode() + supplied.encode())
            if option not in {"--prompt", "--scope-path"}:
                digest.update(pathlib.Path(supplied).read_bytes())
    return digest.hexdigest()

if "--dry-run" in args:
    if "--prompt" in args and "preflight-fail" in args:
        print("preflight fixture", file=sys.stderr)
        raise SystemExit(1)
    mode = args[args.index("--mode") + 1]
    target = "local" if mode in {"auto", "local", "uncommitted"} else mode
    print(f"autoreview target: {target}")
    if target == "branch":
        ref = args[args.index("--base") + 1] if "--base" in args else "main"
        print(f"ref: {ref}")
    print("base_input_fingerprint: " + fingerprint())
    raise SystemExit(0)

lens = args[args.index("--lens") + 1] if "--lens" in args else "generalist"
if "--expected-base-fingerprint" in args:
    expected = args[args.index("--expected-base-fingerprint") + 1]
    if expected != fingerprint():
        print("input changed", file=sys.stderr)
        raise SystemExit(1)
prompts = [args[index + 1] for index, value in enumerate(args) if value == "--prompt"]
control = " ".join(prompts)
time.sleep(0.2)
if "mutate" in control:
    pathlib.Path("tracked.txt").write_text(f"mutated by {lens}\\n")
if "delete-target" in control:
    pathlib.Path("tracked.txt").unlink(missing_ok=True)
if f"malformed-{lens}" in control:
    print("engine failed", file=sys.stderr)
    raise SystemExit(1)
priority = "P2" if "blockers" in control else "P3"
finding = {
    "title": "shared finding" if "duplicates" in control else f"{lens} finding",
    "body": "concrete fixture",
    "priority": priority,
    "confidence": 0.9,
    "category": "bug",
    "code_location": {"file_path": "tracked.txt", "line": 1},
}
report = {
    "findings": [finding] if ("findings" in control or "duplicates" in control or "blockers" in control) else [],
    "overall_correctness": "patch is incorrect" if priority == "P2" or "verdict-only" in control else "patch is correct",
    "overall_explanation": "fixture",
    "overall_confidence": 0.9,
}
pathlib.Path(args[args.index("--json-output") + 1]).write_text(json.dumps(report))
usage = {
    "token_usage_available": "no-usage" not in control,
    "input_tokens": 100,
    "cached_input_tokens": 50,
    "cache_write_input_tokens": 0,
    "output_tokens": 20,
    "reasoning_output_tokens": 10,
    "total_tokens": 120,
    "elapsed_seconds": 0.2,
}
print("autoreview usage: " + json.dumps(usage))
raise SystemExit(1 if priority == "P2" or "verdict-only" in control else 0)
"""


def git(repo: Path, *args: str) -> str:
    env = os.environ.copy()
    env.update(
        {
            "GIT_AUTHOR_NAME": "Stage Test",
            "GIT_AUTHOR_EMAIL": "stage@example.invalid",
            "GIT_COMMITTER_NAME": "Stage Test",
            "GIT_COMMITTER_EMAIL": "stage@example.invalid",
        }
    )
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        env=env,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def fixture(root: Path) -> tuple[Path, Path]:
    repo = root / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    (repo / "tracked.txt").write_text("base\n", encoding="utf-8")
    git(repo, "add", "tracked.txt")
    git(repo, "commit", "-q", "-m", "base")
    fake = root / "fake-autoreview"
    fake.write_text(textwrap.dedent(FAKE_AUTOREVIEW), encoding="utf-8")
    fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
    return repo, fake


def args(**overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "lens": ["generalist"],
        "mode": "local",
        "base": None,
        "commit": "HEAD",
        "model": "gpt-test",
        "thinking": "medium",
        "codex_bin": None,
        "web_search": False,
        "prompt": [],
        "prompt_file": None,
        "dataset": None,
        "scope_path": None,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


class AutoreviewStageTests(unittest.TestCase):
    def test_one_lens_preserves_direct_report_and_usage(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            repo, fake = fixture(Path(tempdir))
            packet, exit_code = autoreview_stage.run_stage(repo, args(), autoreview=fake)

        self.assertEqual(exit_code, 0)
        self.assertTrue(packet["complete"])
        self.assertEqual(packet["results"][0]["lens"], "generalist")
        self.assertEqual(packet["results"][0]["report"]["findings"], [])
        self.assertEqual(packet["usage"]["total_tokens"], 120)

    def test_two_and_three_lenses_run_concurrently_and_sum_usage(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            repo, fake = fixture(Path(tempdir))
            started = time.monotonic()
            packet, exit_code = autoreview_stage.run_stage(
                repo,
                args(lens=["generalist", "architecture"]),
                autoreview=fake,
            )
            elapsed = time.monotonic() - started

            packet_three, exit_three = autoreview_stage.run_stage(
                repo,
                args(lens=["generalist", "architecture", "security"]),
                autoreview=fake,
            )

        self.assertEqual(exit_code, 0)
        self.assertLess(elapsed, 0.36)
        self.assertEqual(packet["usage"]["total_tokens"], 240)
        self.assertEqual(exit_three, 0)
        self.assertEqual(len(packet_three["results"]), 3)

    def test_progress_reports_start_heartbeat_and_lens_transitions(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            repo, fake = fixture(Path(tempdir))
            stderr = io.StringIO()
            with mock.patch.object(
                autoreview_stage,
                "PROGRESS_SECONDS",
                0.05,
            ), redirect_stderr(stderr):
                packet, exit_code = autoreview_stage.run_stage(
                    repo,
                    args(lens=["generalist", "architecture"]),
                    autoreview=fake,
                )

        self.assertEqual(exit_code, 0)
        self.assertTrue(packet["complete"])
        progress = [
            json.loads(line[len(autoreview_stage.PROGRESS_PREFIX) :])
            for line in stderr.getvalue().splitlines()
            if line.startswith(autoreview_stage.PROGRESS_PREFIX)
        ]
        self.assertGreaterEqual(len(progress), 3)
        self.assertEqual(
            progress[0]["pending_lenses"],
            ["generalist", "architecture"],
        )
        self.assertTrue(
            any(
                item["pending_lenses"]
                and item["elapsed_seconds"] >= 0.04
                for item in progress[1:-1]
            )
        )
        self.assertEqual(
            progress[-1]["completed_lenses"],
            ["generalist", "architecture"],
        )
        self.assertEqual(progress[-1]["pending_lenses"], [])

    def test_progress_sink_failure_does_not_cancel_reviewers(self) -> None:
        class BrokenProgressSink:
            def write(self, _value: str) -> int:
                raise BrokenPipeError("consumer closed")

            def flush(self) -> None:
                pass

        with tempfile.TemporaryDirectory() as tempdir:
            repo, fake = fixture(Path(tempdir))
            with mock.patch.object(
                autoreview_stage.sys,
                "stderr",
                BrokenProgressSink(),
            ):
                packet, exit_code = autoreview_stage.run_stage(
                    repo,
                    args(lens=["generalist", "architecture"]),
                    autoreview=fake,
                )

        self.assertEqual(exit_code, 0)
        self.assertTrue(packet["complete"])
        self.assertEqual(
            [item["status"] for item in packet["results"]],
            ["completed", "completed"],
        )

    def test_real_closed_progress_pipe_does_not_change_process_exit(self) -> None:
        code = textwrap.dedent(
            f"""
            import sys
            import time
            sys.path.insert(0, {str(SCRIPT_DIR)!r})
            import autoreview_stage
            time.sleep(0.1)
            autoreview_stage._emit_progress(["generalist"], [], time.monotonic())
            """
        )
        process = subprocess.Popen(
            [sys.executable, "-c", code],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        assert process.stderr is not None
        process.stderr.close()

        self.assertEqual(process.wait(timeout=5), 0)

    def test_valid_blocking_exit_one_is_completed(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            repo, fake = fixture(Path(tempdir))
            packet, exit_code = autoreview_stage.run_stage(
                repo,
                args(prompt=["blockers"]),
                autoreview=fake,
            )

        self.assertEqual(exit_code, 1)
        self.assertTrue(packet["complete"])
        self.assertEqual(packet["results"][0]["status"], "completed")
        self.assertEqual(packet["findings"][0]["finding"]["priority"], "P2")

        with tempfile.TemporaryDirectory() as tempdir:
            repo, fake = fixture(Path(tempdir))
            packet, exit_code = autoreview_stage.run_stage(
                repo,
                args(prompt=["verdict-only"]),
                autoreview=fake,
            )
        self.assertEqual(exit_code, 1)
        self.assertTrue(packet["complete"])
        self.assertEqual(packet["findings"], [])

    def test_failed_or_malformed_lens_makes_stage_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            repo, fake = fixture(Path(tempdir))
            packet, exit_code = autoreview_stage.run_stage(
                repo,
                args(
                    lens=["generalist", "architecture"],
                    prompt=["malformed-architecture"],
                ),
                autoreview=fake,
            )

        self.assertEqual(exit_code, 2)
        self.assertFalse(packet["complete"])
        self.assertEqual(packet["results"][1]["status"], "incomplete")
        self.assertIsNone(packet["results"][1]["report"])

        with tempfile.TemporaryDirectory() as tempdir:
            repo, fake = fixture(Path(tempdir))
            packet, exit_code = autoreview_stage.run_stage(
                repo,
                args(prompt=["preflight-fail"]),
                autoreview=fake,
            )
        self.assertEqual(exit_code, 2)
        self.assertFalse(packet["complete"])
        self.assertEqual(packet["results"], [])
        self.assertIn("preflight input inspection failed", packet["failure"])

    def test_findings_remain_per_lens_and_exact_duplicates_are_grouped(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            repo, fake = fixture(Path(tempdir))
            packet, _ = autoreview_stage.run_stage(
                repo,
                args(
                    lens=["generalist", "architecture"],
                    prompt=["duplicates"],
                ),
                autoreview=fake,
            )

        self.assertEqual([item["lens"] for item in packet["findings"]], ["generalist", "architecture"])
        self.assertEqual(packet["duplicate_groups"][0]["lenses"], ["generalist", "architecture"])
        self.assertEqual(len(packet["results"][0]["report"]["findings"]), 1)
        self.assertEqual(len(packet["results"][1]["report"]["findings"]), 1)

    def test_target_change_and_cleanup_failure_make_stage_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            repo, fake = fixture(Path(tempdir))
            packet, exit_code = autoreview_stage.run_stage(
                repo,
                args(prompt=["mutate"]),
                autoreview=fake,
            )
            self.assertEqual(exit_code, 2)
            self.assertFalse(packet["target"]["stable"])

        with tempfile.TemporaryDirectory() as tempdir:
            repo, fake = fixture(Path(tempdir))
            packet, exit_code = autoreview_stage.run_stage(
                repo,
                args(prompt=["delete-target"]),
                autoreview=fake,
            )
            self.assertEqual(exit_code, 2)
            self.assertIn("post-review fingerprint failed", packet["failure"])

        with tempfile.TemporaryDirectory() as tempdir:
            repo, fake = fixture(Path(tempdir))
            real_rmtree = autoreview_stage.shutil.rmtree

            def remove_then_fail(path: Path) -> None:
                real_rmtree(path)
                raise OSError("cleanup fixture")

            with mock.patch.object(
                autoreview_stage.shutil,
                "rmtree",
                side_effect=remove_then_fail,
            ):
                packet, exit_code = autoreview_stage.run_stage(repo, args(), autoreview=fake)

        self.assertEqual(exit_code, 2)
        self.assertIn("temporary cleanup failed", packet["failure"])

    def test_interrupt_returns_incomplete_and_stops_children(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            repo, fake = fixture(Path(tempdir))
            with mock.patch.object(
                autoreview_stage,
                "wait",
                side_effect=KeyboardInterrupt,
            ):
                packet, exit_code = autoreview_stage.run_stage(
                    repo,
                    args(lens=["generalist", "architecture"]),
                    autoreview=fake,
                )

        self.assertEqual(exit_code, 2)
        self.assertFalse(packet["complete"])
        self.assertIn("KeyboardInterrupt", packet["failure"])

    def test_cli_installs_and_restores_sigterm_handler(self) -> None:
        entry = runpy.run_path(
            str(SCRIPT_DIR / "autoreview-stage"),
            run_name="autoreview_stage_entry_test",
        )
        main = entry["main"]
        installed: list[tuple[object, object]] = []
        previous = object()
        packet = {"complete": True}
        with mock.patch.dict(
            main.__globals__,
            {
                "parse_args": lambda: args(),
                "validate_lenses": lambda _lenses: None,
                "repo_root": lambda: Path("/repo"),
                "run_stage": lambda *_args, **_kwargs: (packet, 0),
            },
        ), mock.patch.object(
            entry["signal"],
            "getsignal",
            return_value=previous,
        ), mock.patch.object(
            entry["signal"],
            "signal",
            side_effect=lambda signum, handler: installed.append((signum, handler)),
        ), mock.patch("builtins.print"):
            self.assertEqual(main(), 0)

        self.assertEqual(installed[0][0], entry["signal"].SIGTERM)
        self.assertTrue(callable(installed[0][1]))
        self.assertEqual(installed[-1], (entry["signal"].SIGTERM, previous))

    def test_unavailable_usage_is_visible_without_invalidating_report(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            repo, fake = fixture(Path(tempdir))
            packet, exit_code = autoreview_stage.run_stage(
                repo,
                args(prompt=["no-usage"]),
                autoreview=fake,
            )

        self.assertEqual(exit_code, 0)
        self.assertTrue(packet["complete"])
        self.assertFalse(packet["usage"]["token_usage_available"])
        self.assertEqual(packet["usage"]["unavailable_lenses"], ["generalist"])
        self.assertEqual(packet["usage"]["reviewer_elapsed_seconds"], 0.2)

    def test_optional_usage_counter_unavailability_does_not_abort_packet(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            repo, fake = fixture(Path(tempdir))
            fake.write_text(
                fake.read_text().replace(
                    '"cache_write_input_tokens": 0',
                    '"cache_write_input_tokens": None',
                )
            )
            packet, exit_code = autoreview_stage.run_stage(repo, args(), autoreview=fake)

        self.assertEqual(exit_code, 0)
        self.assertTrue(packet["complete"])
        self.assertIsNone(packet["usage"]["cache_write_input_tokens"])
        self.assertEqual(
            packet["usage"]["unavailable_metric_lenses"]["cache_write_input_tokens"],
            ["generalist"],
        )

    def test_cli_rejects_more_than_three_duplicate_or_unknown_lenses(self) -> None:
        invalid = (
            ["generalist", "architecture", "security", "performance"],
            ["generalist", "generalist"],
            ["not-built"],
        )
        for value in invalid:
            with self.subTest(lenses=value), self.assertRaises(SystemExit):
                autoreview_stage.validate_lenses(value)


if __name__ == "__main__":
    unittest.main()
