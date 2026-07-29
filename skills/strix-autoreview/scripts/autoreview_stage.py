from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path
from typing import Any

from autoreview_lenses import available_lenses
from autoreview_schema import report_schema_error


TOKEN_FIELDS = ("input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens",
                "reasoning_output_tokens", "total_tokens")
USAGE_PREFIX = "autoreview usage: "
PROGRESS_PREFIX = "autoreview-stage progress: "
PROGRESS_SECONDS = 60
MAX_REVIEWERS = 3


def _run(cmd: list[str], repo: Path, *, text: bool = True) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(cmd, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=text)

def repo_root() -> Path:
    result = _run(["git", "rev-parse", "--show-toplevel"], Path.cwd())
    if result.returncode != 0:
        raise SystemExit("autoreview-stage must run inside a git repository")
    return Path(result.stdout.strip()).resolve()

def _append_shared_options(cmd: list[str], args: argparse.Namespace) -> None:
    for option, values in (
        ("--prompt", args.prompt),
        ("--prompt-file", args.prompt_file),
        ("--dataset", args.dataset),
        ("--scope-path", args.scope_path),
    ):
        for value in values or []:
            cmd.extend([option, value])

def inspect_input(repo: Path, args: argparse.Namespace, autoreview: Path) -> tuple[str, str | None, str]:
    cmd = [str(autoreview), "--dry-run", "--mode", args.mode]
    if args.base:
        cmd.extend(["--base", args.base])
    if args.commit:
        cmd.extend(["--commit", args.commit])
    _append_shared_options(cmd, args)
    result = _run(cmd, repo)
    if result.returncode != 0:
        raise SystemExit(result.stderr or result.stdout)
    values: dict[str, str] = {}
    for line in result.stdout.splitlines():
        key, separator, value = line.partition(": ")
        if separator and key in {
            "autoreview target",
            "ref",
            "base_input_fingerprint",
        }:
            values[key] = value
    target = values.get("autoreview target")
    if target not in {"local", "branch", "commit"}:
        raise SystemExit("unable to resolve autoreview target")
    fingerprint = values.get("base_input_fingerprint")
    if not fingerprint:
        raise SystemExit("unable to fingerprint autoreview base input")
    return target, values.get("ref"), fingerprint

def _usage_from_stdout(stdout: str) -> dict[str, Any] | None:
    for line in reversed(stdout.splitlines()):
        if line.startswith(USAGE_PREFIX):
            try:
                value = json.loads(line[len(USAGE_PREFIX) :])
            except json.JSONDecodeError:
                return None
            return value if isinstance(value, dict) else None
    return None

def _valid_report(value: object) -> bool:
    return report_schema_error(value) is None

def validate_lenses(lenses: list[str]) -> None:
    if len(lenses) > MAX_REVIEWERS:
        raise SystemExit(f"autoreview-stage supports at most {MAX_REVIEWERS} lenses")
    if len(set(lenses)) != len(lenses):
        raise SystemExit("autoreview-stage lens names must be unique")
    unknown = [lens for lens in lenses if lens not in {"generalist", *available_lenses()}]
    if unknown:
        raise SystemExit(f"unknown autoreview stage lens: {', '.join(unknown)}")

def _child_command(autoreview: Path, args: argparse.Namespace, target: str, target_ref: str | None,
                   lens: str, output: Path, fingerprint: str) -> list[str]:
    cmd = [
        str(autoreview),
        "--mode",
        target,
        "--json-output",
        str(output),
        "--expected-base-fingerprint",
        fingerprint,
    ]
    if target == "branch":
        assert target_ref
        cmd.extend(["--base", target_ref])
    elif target == "commit":
        cmd.extend(["--commit", args.commit])
    if lens != "generalist":
        cmd.extend(["--lens", lens])
    for option, value in (
        ("--model", args.model),
        ("--thinking", args.thinking),
        ("--codex-bin", args.codex_bin),
    ):
        if value:
            cmd.extend([option, value])
    if args.web_search:
        cmd.append("--web-search")
    _append_shared_options(cmd, args)
    return cmd

def _terminate_processes(processes: set[subprocess.Popen[str]], process_lock: threading.Lock) -> None:
    with process_lock:
        active = [process for process in processes if process.poll() is None]
    for process in active:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            continue
    for process in active:
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass


def _emit_progress(
    lenses: list[str],
    results: list[dict[str, Any]],
    started: float,
) -> bool:
    statuses = {item["lens"]: item["status"] for item in results}
    payload = {
        "schema_version": 1,
        "completed_lenses": [
            lens for lens in lenses if statuses.get(lens) == "completed"
        ],
        "incomplete_lenses": [
            lens for lens in lenses if statuses.get(lens) == "incomplete"
        ],
        "pending_lenses": [lens for lens in lenses if lens not in statuses],
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    line = PROGRESS_PREFIX + json.dumps(payload, separators=(",", ":")) + "\n"
    try:
        try:
            descriptor = sys.stderr.fileno()
        except (AttributeError, OSError, ValueError):
            sys.stderr.write(line)
            sys.stderr.flush()
        else:
            encoded = line.encode("utf-8")
            while encoded:
                written = os.write(descriptor, encoded)
                if written <= 0:
                    raise OSError("progress descriptor accepted no bytes")
                encoded = encoded[written:]
    except (OSError, ValueError):
        return False
    return True


def run_stage(repo: Path, args: argparse.Namespace, *, autoreview: Path) -> tuple[dict[str, Any], int]:
    started = time.monotonic()
    try:
        target, target_ref, before = inspect_input(repo, args, autoreview)
    except BaseException as exc:
        empty_usage = {field: None for field in TOKEN_FIELDS}
        target_ref = args.base if args.mode == "branch" else (
            args.commit if args.mode == "commit" else None
        )
        return {
            "schema_version": 1, "complete": False,
            "target": {"mode": args.mode, "ref": target_ref,
                       "fingerprint": None, "stable": False},
            "results": [], "findings": [], "duplicate_groups": [],
            "usage": {
                "token_usage_available": False, "available_lens_count": 0,
                "unavailable_lenses": args.lens,
                "unavailable_metric_lenses": {field: args.lens for field in TOKEN_FIELDS},
                **empty_usage,
                "reviewer_elapsed_seconds": 0, "prompt_chars": 0,
                "usage_event_count": 0, "malformed_event_count": 0,
                "stage_elapsed_seconds": round(time.monotonic() - started, 3),
            },
            "failure": f"preflight input inspection failed: {exc}",
        }, 2
    temp_root = Path(tempfile.mkdtemp(prefix="strix-autoreview-stage-"))
    processes: set[subprocess.Popen[str]] = set()
    process_lock = threading.Lock()
    cancel_event = threading.Event()

    def run_one(lens: str) -> dict[str, Any]:
        output = temp_root / f"{lens}.json"
        cmd = _child_command(autoreview, args, target, target_ref, lens, output, before)
        proc = subprocess.Popen(cmd, cwd=repo, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True,
                                start_new_session=True)
        with process_lock:
            processes.add(proc)
        if cancel_event.is_set():
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        try:
            stdout, stderr = proc.communicate()
        finally:
            with process_lock:
                processes.discard(proc)
        report: object = None
        if output.is_file():
            try:
                report = json.loads(output.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                report = None
        completed = proc.returncode in {0, 1} and _valid_report(report)
        return {
            "lens": lens,
            "status": "completed" if completed else "incomplete",
            "exit_code": proc.returncode,
            "report": report if completed else None,
            "usage": _usage_from_stdout(stdout) if completed else None,
            "error": None if completed else (stderr or stdout)[-4000:],
        }

    results: list[dict[str, Any]] = []
    cleanup_error: str | None = None
    stage_failure: str | None = None
    executor = ThreadPoolExecutor(max_workers=min(MAX_REVIEWERS, len(args.lens)))
    futures = {executor.submit(run_one, lens): lens for lens in args.lens}
    try:
        pending = set(futures)
        progress_enabled = _emit_progress(args.lens, results, started)
        while pending:
            done, pending = wait(
                pending,
                timeout=PROGRESS_SECONDS,
                return_when=FIRST_COMPLETED,
            )
            if not done:
                if progress_enabled:
                    progress_enabled = _emit_progress(args.lens, results, started)
                continue
            for future in done:
                results.append(future.result())
            if progress_enabled:
                progress_enabled = _emit_progress(args.lens, results, started)
    except BaseException as exc:
        stage_failure = f"stage interrupted: {type(exc).__name__}"
        cancel_event.set()
        _terminate_processes(processes, process_lock)
        for future in futures:
            future.cancel()
    finally:
        executor.shutdown(wait=True, cancel_futures=True)
        completed_lenses = {item["lens"] for item in results}
        for future, lens in futures.items():
            if lens in completed_lenses:
                continue
            try:
                results.append(future.result())
            except BaseException as exc:
                results.append({
                    "lens": lens, "status": "incomplete", "exit_code": None,
                    "report": None, "usage": None,
                    "error": f"{type(exc).__name__}: {exc}",
                })
        try:
            shutil.rmtree(temp_root)
        except OSError as exc:
            cleanup_error = str(exc)

    results.sort(key=lambda item: args.lens.index(item["lens"]))
    post_failure: str | None = None
    try:
        after_target, after_ref, after = inspect_input(repo, args, autoreview)
        stable = before == after and target == after_target and target_ref == after_ref
    except BaseException as exc:
        stable = False
        post_failure = f"post-review fingerprint failed: {exc}"
    complete = (all(item["status"] == "completed" for item in results)
                and stable and not cleanup_error and not stage_failure)
    unavailable = [item["lens"] for item in results if not item["usage"]
                   or not item["usage"].get("token_usage_available")]
    available_usage = [item["usage"] for item in results if item["usage"]
                       and item["usage"].get("token_usage_available")]
    unavailable_metrics = {
        field: [item["lens"] for item in results if not item["usage"]
                or not item["usage"].get("token_usage_available")
                or not isinstance(item["usage"].get(field), int)]
        for field in TOKEN_FIELDS
    }
    totals = {
        field: (None if unavailable_metrics[field]
                else sum(int(usage[field]) for usage in available_usage))
        for field in TOKEN_FIELDS
    }
    findings = [{"lens": item["lens"], "finding": finding}
                for item in results if item["report"]
                for finding in item["report"]["findings"]]
    groups: dict[str, list[str]] = {}
    for item in findings:
        key = json.dumps(item["finding"], sort_keys=True, separators=(",", ":"))
        groups.setdefault(key, []).append(item["lens"])
    duplicate_groups = [{"lenses": lenses, "finding": json.loads(key)}
                        for key, lenses in groups.items() if len(lenses) > 1]
    blockers = any(item["exit_code"] == 1 for item in results) or any(
        finding["finding"].get("priority") in {"P0", "P1", "P2"}
        for finding in findings
    )
    packet = {
        "schema_version": 1, "complete": complete,
        "target": {
            "mode": target, "ref": target_ref if target != "commit" else args.commit,
            "fingerprint": before, "stable": stable,
        },
        "results": results, "findings": findings,
        "duplicate_groups": duplicate_groups,
        "usage": {
            "token_usage_available": not unavailable and bool(results),
            "available_lens_count": len(available_usage), "unavailable_lenses": unavailable,
            "unavailable_metric_lenses": unavailable_metrics,
            **totals,
            "reviewer_elapsed_seconds": round(sum(float(item["usage"].get("elapsed_seconds", 0))
                                                  for item in results if item["usage"]), 3),
            "prompt_chars": sum(int(item["usage"].get("prompt_chars", 0))
                                for item in results if item["usage"]),
            "usage_event_count": sum(int(item["usage"].get("usage_event_count", 0))
                                     for item in results if item["usage"]),
            "malformed_event_count": sum(int(item["usage"].get("malformed_event_count", 0))
                                         for item in results if item["usage"]),
            "stage_elapsed_seconds": round(time.monotonic() - started, 3),
        },
        "failure": (stage_failure or post_failure
                    or ("review input changed during stage" if not stable else None)
                    or (f"temporary cleanup failed: {cleanup_error}" if cleanup_error else None)
                    or ("one or more reviewers incomplete" if not complete else None)),
    }
    return packet, 2 if not complete else 1 if blockers else 0
