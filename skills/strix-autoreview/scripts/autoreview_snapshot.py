from __future__ import annotations

import os
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path


def _run(cmd: list[str], cwd: Path, env: dict[str, str]) -> str:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise SystemExit(
            f"unable to create scoped review snapshot ({result.returncode}): "
            f"{result.stderr or result.stdout}"
        )
    return result.stdout


def _run_bytes(
    cmd: list[str],
    cwd: Path,
    env: dict[str, str],
    *,
    input_data: bytes | None = None,
) -> bytes:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace")
        stdout = result.stdout.decode("utf-8", errors="replace")
        raise SystemExit(
            f"unable to create scoped review snapshot ({result.returncode}): "
            f"{stderr or stdout}"
        )
    return result.stdout


def _apply_scoped_index(
    source: Path,
    snapshot: Path,
    changed_paths: set[str],
    env: dict[str, str],
) -> None:
    if not changed_paths:
        return
    pathspecs = ["--", *(f":(literal){path}" for path in sorted(changed_paths))]
    patch = _run_bytes(
        [
            "git",
            "diff",
            "--cached",
            "--binary",
            "--full-index",
            "--no-ext-diff",
            "--no-textconv",
            *pathspecs,
        ],
        source,
        env,
    )
    if patch:
        _run_bytes(
            [
                "git",
                "apply",
                "--cached",
                "--binary",
                "--whitespace=nowarn",
                "-",
            ],
            snapshot,
            env,
            input_data=patch,
        )


def _replace_with_worktree_path(source: Path, destination: Path) -> None:
    try:
        mode = os.lstat(source).st_mode
    except FileNotFoundError:
        if os.path.lexists(destination):
            destination.unlink()
        return
    if stat.S_ISDIR(mode):
        if os.path.lexists(destination):
            if destination.is_dir() and not destination.is_symlink():
                return
            destination.unlink()
        destination.mkdir()
        return
    if os.path.lexists(destination):
        if destination.is_dir() and not destination.is_symlink():
            raise SystemExit(f"scoped review path unexpectedly resolves to a directory: {source}")
        destination.unlink()
    if stat.S_ISLNK(mode):
        destination.symlink_to(os.readlink(source))
    elif stat.S_ISREG(mode):
        shutil.copy2(source, destination, follow_symlinks=False)
    else:
        raise SystemExit(f"scoped review path is not a regular file or symlink: {source}")


def _prepare_snapshot_destination(snapshot: Path, relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise SystemExit(f"unsafe scoped review snapshot path: {relative}")
    parent = snapshot
    for part in path.parts[:-1]:
        parent /= part
        try:
            mode = os.lstat(parent).st_mode
        except FileNotFoundError:
            parent.mkdir()
            continue
        if not stat.S_ISDIR(mode):
            raise SystemExit(
                "scoped review snapshot path has a symlink or non-directory "
                f"ancestor: {relative}"
            )
    return snapshot / path


def create_review_snapshot(
    repo: Path,
    ref: str,
    changed_paths: set[str],
    *,
    staged_paths: set[str] | None = None,
) -> tuple[tempfile.TemporaryDirectory[str], Path]:
    temporary = tempfile.TemporaryDirectory(prefix="strix-autoreview-snapshot-")
    snapshot = Path(temporary.name) / "repo"
    env = os.environ.copy()
    env["GIT_LFS_SKIP_SMUDGE"] = "1"
    try:
        _run(
            [
                "git",
                "-c",
                "core.hooksPath=/dev/null",
                "clone",
                "--quiet",
                "--no-checkout",
                "--no-hardlinks",
                str(repo),
                str(snapshot),
            ],
            repo,
            env,
        )
        resolved_ref = _run(["git", "rev-parse", f"{ref}^{{commit}}"], repo, env).strip()
        _run(
            [
                "git",
                "-c",
                "core.hooksPath=/dev/null",
                "checkout",
                "--quiet",
                "--detach",
                resolved_ref,
            ],
            snapshot,
            env,
        )
        _run(["git", "remote", "remove", "origin"], snapshot, env)
        if staged_paths:
            _apply_scoped_index(repo, snapshot, staged_paths, env)
        for relative in sorted(changed_paths):
            destination = _prepare_snapshot_destination(snapshot, relative)
            _replace_with_worktree_path(repo / relative, destination)
    except BaseException:
        temporary.cleanup()
        raise
    return temporary, snapshot
