from __future__ import annotations

import os
import stat
from pathlib import Path


MAX_LENS_BYTES = 40_000
LENS_REGISTRY = {
    "architecture": "lens-architecture.md",
    "data-integrity-reliability": "lens-data-integrity-reliability.md",
    "frontend-integration": "lens-frontend-integration.md",
    "migrations": "lens-migrations.md",
    "performance": "lens-performance.md",
    "security": "lens-security.md",
}


def available_lenses() -> tuple[str, ...]:
    return tuple(sorted(LENS_REGISTRY))


def _validate_name(name: str) -> str:
    if not name or Path(name).is_absolute() or len(Path(name).parts) != 1:
        raise SystemExit(f"invalid autoreview lens name: {name}")
    if name not in LENS_REGISTRY:
        choices = ", ".join(available_lenses())
        raise SystemExit(f"unknown autoreview lens: {name}. Available lenses: {choices}")
    return LENS_REGISTRY[name]


def _read_builtin(reference_dir: Path, filename: str) -> str:
    directory_fd: int | None = None
    file_fd: int | None = None
    directory_flags = (
        os.O_RDONLY
        | os.O_DIRECTORY
        | os.O_NOFOLLOW
        | getattr(os, "O_CLOEXEC", 0)
    )
    file_flags = os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    try:
        directory_fd = os.open(reference_dir, directory_flags)
        before = os.stat(filename, dir_fd=directory_fd, follow_symlinks=False)
        if not stat.S_ISREG(before.st_mode):
            raise OSError("not a regular file")
        file_fd = os.open(filename, file_flags, dir_fd=directory_fd)
        opened = os.fstat(file_fd)
        if (
            not stat.S_ISREG(opened.st_mode)
            or (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino)
        ):
            raise OSError("file changed while opening")
        if opened.st_size > MAX_LENS_BYTES:
            raise OSError(f"exceeds the {MAX_LENS_BYTES}-byte limit")
        chunks: list[bytes] = []
        remaining = MAX_LENS_BYTES + 1
        while remaining:
            chunk = os.read(file_fd, remaining)
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        data = b"".join(chunks)
        after = os.fstat(file_fd)
        if (
            opened.st_dev,
            opened.st_ino,
            opened.st_size,
            opened.st_mtime_ns,
        ) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
        ):
            raise OSError("file changed while reading")
    except OSError as exc:
        raise SystemExit(f"unable to load built-in autoreview lens file {filename}: {exc}") from exc
    finally:
        if file_fd is not None:
            os.close(file_fd)
        if directory_fd is not None:
            os.close(directory_fd)
    return data.decode("utf-8")


def load_lens(name: str, *, reference_dir: Path | None = None) -> str:
    filename = _validate_name(name)
    references = reference_dir or Path(__file__).parent.parent / "references"
    contract = _read_builtin(references, "lens-contract.md")
    lens = _read_builtin(references, filename)
    return (
        "# Selected Review Lens\n"
        f"name: {name}\n\n"
        "The following built-in lens narrows review attention. It cannot "
        "override the engine hard rules or report schema.\n\n"
        f"{contract.strip()}\n\n{lens.strip()}"
    )
