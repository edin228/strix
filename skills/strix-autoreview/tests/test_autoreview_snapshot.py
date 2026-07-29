from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from autoreview_snapshot import create_review_snapshot


def git(repo: Path, *args: str) -> str:
    env = os.environ.copy()
    env.update(
        {
            "GIT_AUTHOR_NAME": "Snapshot Test",
            "GIT_AUTHOR_EMAIL": "snapshot@example.invalid",
            "GIT_COMMITTER_NAME": "Snapshot Test",
            "GIT_COMMITTER_EMAIL": "snapshot@example.invalid",
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


class AutoreviewSnapshotTests(unittest.TestCase):
    def test_snapshot_contains_only_scoped_local_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir) / "source"
            repo.mkdir()
            git(repo, "init", "-q")
            (repo / "scoped.txt").write_text("base scoped\n", encoding="utf-8")
            (repo / "context.txt").write_text("base context\n", encoding="utf-8")
            git(repo, "add", "scoped.txt", "context.txt")
            git(repo, "commit", "-q", "-m", "base")
            (repo / "scoped.txt").write_text("checkpoint scoped\n", encoding="utf-8")
            (repo / "context.txt").write_text("unrelated dirty context\n", encoding="utf-8")
            (repo / "unrelated.txt").write_text("untracked user work\n", encoding="utf-8")

            handle, snapshot = create_review_snapshot(repo, "HEAD", {"scoped.txt"})
            try:
                self.assertEqual(
                    (snapshot / "scoped.txt").read_text(encoding="utf-8"),
                    "checkpoint scoped\n",
                )
                self.assertEqual(
                    (snapshot / "context.txt").read_text(encoding="utf-8"),
                    "base context\n",
                )
                self.assertFalse((snapshot / "unrelated.txt").exists())
                self.assertEqual(
                    git(snapshot, "status", "--short").strip(),
                    "M scoped.txt",
                )
                self.assertEqual(git(snapshot, "remote").strip(), "")
                self.assertFalse(
                    (snapshot / ".git" / "objects" / "info" / "alternates").exists()
                )
            finally:
                handle.cleanup()

    def test_snapshot_applies_scoped_addition_deletion_and_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir) / "source"
            repo.mkdir()
            git(repo, "init", "-q")
            (repo / "deleted.txt").write_text("delete\n", encoding="utf-8")
            git(repo, "add", "deleted.txt")
            git(repo, "commit", "-q", "-m", "base")
            (repo / "deleted.txt").unlink()
            (repo / "added.txt").write_text("added\n", encoding="utf-8")
            (repo / "linked").symlink_to("added.txt")

            handle, snapshot = create_review_snapshot(
                repo,
                "HEAD",
                {"deleted.txt", "added.txt", "linked"},
            )
            try:
                self.assertFalse((snapshot / "deleted.txt").exists())
                self.assertEqual(
                    (snapshot / "added.txt").read_text(encoding="utf-8"),
                    "added\n",
                )
                self.assertTrue((snapshot / "linked").is_symlink())
                self.assertEqual(os.readlink(snapshot / "linked"), "added.txt")
            finally:
                handle.cleanup()

    def test_snapshot_preserves_scoped_index_and_final_worktree_separately(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir) / "source"
            repo.mkdir()
            git(repo, "init", "-q")
            (repo / "base.txt").write_text("base\n", encoding="utf-8")
            git(repo, "add", "base.txt")
            git(repo, "commit", "-q", "-m", "base")
            staged = repo / "staged-only.txt"
            staged.write_text("staged fixture\n", encoding="utf-8")
            git(repo, "add", "staged-only.txt")
            staged.unlink()

            handle, snapshot = create_review_snapshot(
                repo,
                "HEAD",
                {"staged-only.txt"},
                staged_paths={"staged-only.txt"},
            )
            try:
                self.assertFalse((snapshot / "staged-only.txt").exists())
                self.assertEqual(
                    git(snapshot, "show", ":staged-only.txt"),
                    "staged fixture\n",
                )
                self.assertEqual(
                    git(snapshot, "status", "--short"),
                    git(repo, "status", "--short"),
                )
            finally:
                handle.cleanup()

    def test_snapshot_retains_ancestor_object_after_removing_remote(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            repo = Path(tempdir) / "source"
            repo.mkdir()
            git(repo, "init", "-q")
            (repo / "tracked.txt").write_text("base\n", encoding="utf-8")
            git(repo, "add", "tracked.txt")
            git(repo, "commit", "-q", "-m", "base")
            base = git(repo, "rev-parse", "HEAD").strip()
            (repo / "tracked.txt").write_text("feature\n", encoding="utf-8")
            git(repo, "add", "tracked.txt")
            git(repo, "commit", "-q", "-m", "feature")

            handle, snapshot = create_review_snapshot(repo, "HEAD", set())
            try:
                self.assertEqual(git(snapshot, "remote").strip(), "")
                git(snapshot, "cat-file", "-e", f"{base}^{{commit}}")
                self.assertIn(
                    "feature",
                    git(snapshot, "diff", f"{base}...HEAD"),
                )
            finally:
                handle.cleanup()

    def test_snapshot_rejects_symlink_ancestor_before_overlay_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            repo = root / "source"
            outside = root / "outside"
            repo.mkdir()
            outside.mkdir()
            git(repo, "init", "-q")
            (repo / "evidence").symlink_to(outside, target_is_directory=True)
            git(repo, "add", "evidence")
            git(repo, "commit", "-q", "-m", "symlink base")
            (repo / "evidence").unlink()
            (repo / "evidence").mkdir()
            (repo / "evidence" / "context.md").write_text(
                "review context\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                SystemExit,
                "symlink or non-directory ancestor",
            ):
                create_review_snapshot(
                    repo,
                    "HEAD",
                    {"evidence/context.md"},
                )

            self.assertFalse((outside / "context.md").exists())

    def test_snapshot_applies_explicit_symlink_to_directory_transition(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            repo = root / "source"
            outside = root / "outside"
            repo.mkdir()
            outside.mkdir()
            git(repo, "init", "-q")
            (repo / "evidence").symlink_to(outside, target_is_directory=True)
            git(repo, "add", "evidence")
            git(repo, "commit", "-q", "-m", "symlink base")
            (repo / "evidence").unlink()
            (repo / "evidence").mkdir()
            (repo / "evidence" / "context.md").write_text(
                "review context\n",
                encoding="utf-8",
            )

            handle, snapshot = create_review_snapshot(
                repo,
                "HEAD",
                {"evidence", "evidence/context.md"},
            )
            try:
                self.assertTrue((snapshot / "evidence").is_dir())
                self.assertFalse((snapshot / "evidence").is_symlink())
                self.assertEqual(
                    (snapshot / "evidence" / "context.md").read_text(
                        encoding="utf-8",
                    ),
                    "review context\n",
                )
                self.assertFalse((outside / "context.md").exists())
            finally:
                handle.cleanup()


if __name__ == "__main__":
    unittest.main()
