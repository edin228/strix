from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from autoreview_lenses import available_lenses, load_lens


class AutoreviewLensTests(unittest.TestCase):
    def test_registry_exposes_only_built_in_lenses(self) -> None:
        self.assertEqual(
            available_lenses(),
            (
                "architecture",
                "data-integrity-reliability",
                "frontend-integration",
                "migrations",
                "performance",
                "security",
            ),
        )
        expected_boundaries = {
            "architecture": (
                "Preference for a different but valid architecture",
                "unsupported cross-repository contract",
            ),
            "data-integrity-reliability": (
                "Clearing a persistence layer's committed or dirty history",
                "Hypothetical distributed failure modes",
            ),
            "frontend-integration": (
                "mobile-only loading, error, or empty branches",
                "Visual polish, typography",
            ),
            "security": (
                "filters only by a caller-supplied",
                "Generic hardening with no supported",
            ),
            "migrations": (
                "checks for incompatible rows before installing",
                "Generic zero-downtime",
            ),
            "performance": (
                "nested relationships from a detail query",
                "Micro-optimizations without evidence",
            ),
        }
        for lens, (true_positive, out_of_scope) in expected_boundaries.items():
            with self.subTest(lens=lens):
                prompt = load_lens(lens)
                self.assertIn(f"name: {lens}", prompt)
                self.assertIn("engine’s hard rules", prompt)
                self.assertIn(
                    "checklist as an inspection obligation, not a finding",
                    prompt,
                )
                self.assertIn("one completeness pass", prompt)
                self.assertIn(
                    "Finding one blocker does not end the review",
                    prompt,
                )
                self.assertIn("## Coverage checklist", prompt)
                self.assertIn(true_positive, prompt)
                self.assertIn(out_of_scope, prompt)

    def test_lens_checklists_cover_material_blind_spots(self) -> None:
        expected_coverage = {
            "architecture": (
                "Contract propagation",
                "intermediate states",
            ),
            "data-integrity-reliability": (
                "change tracking",
                "autocommit boundaries",
                "prove writers remain constrained",
                "Partial success and recovery",
            ),
            "frontend-integration": (
                "page restoration",
                "navigation alone is not",
                "queued, partial, and completed",
                "failed background refetch",
                "responsive-owner replacement",
                "durable post-settlement reconciliation",
                "cancellation guarantees no later server commit",
                "switching presentation",
                "entered mode without its controls or exit",
                "inventory material data, actions, and status context",
                "CSS/display precedence",
                "external, realtime, and",
                "not hover-only",
                "clip supported controls",
                "focus containment",
                "restoration for every changed",
                "usable cached data",
                "cancellation or abort propagation",
                "callback precedence",
                "producers and consumers",
                "exact query key prefix",
                "backing record disappears",
                "create, restore, retry, or discard",
                "native DOM",
            ),
            "migrations": (
                "old and new application",
                "concurrent writer",
                "backfill bounds",
            ),
            "performance": (
                "per-item lookups or writes",
                "batch context",
                "intermediate boundary drops its controls",
                "request-target growth",
                "page limit alone",
                "grouped deduplication",
                "static import reachability",
                "does not remove an import from the client bundle",
                "connection-pool and concurrency defaults",
                "nested session needs",
                "meaningful latency",
                "outer and inner cardinalities",
                "growing list",
                "quadratic",
                "relationship loader",
                "payload entity tables",
                "entire tenant history",
            ),
            "security": (
                "proxy headers",
                "cross-tenant",
                "trusted-proxy controls",
            ),
        }
        for lens, coverage in expected_coverage.items():
            with self.subTest(lens=lens):
                prompt = load_lens(lens)
                for phrase in coverage:
                    self.assertIn(phrase, prompt)

    def test_unknown_absolute_and_traversal_names_fail(self) -> None:
        for name in ("not-built", "/tmp/architecture", "../architecture", "nested/architecture", ""):
            with self.subTest(name=name), self.assertRaises(SystemExit):
                load_lens(name)

    def test_symlinked_contract_or_lens_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            real_contract = root / "real-contract.md"
            real_lens = root / "real-lens.md"
            real_contract.write_text("contract", encoding="utf-8")
            real_lens.write_text("lens", encoding="utf-8")

            (root / "lens-contract.md").symlink_to(real_contract)
            (root / "lens-architecture.md").write_text("lens", encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "unable to load"):
                load_lens("architecture", reference_dir=root)

            (root / "lens-contract.md").unlink()
            (root / "lens-contract.md").write_text("contract", encoding="utf-8")
            (root / "lens-architecture.md").unlink()
            (root / "lens-architecture.md").symlink_to(real_lens)
            with self.assertRaisesRegex(SystemExit, "unable to load"):
                load_lens("architecture", reference_dir=root)

    def test_non_regular_or_oversized_lens_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            (root / "lens-contract.md").write_text("contract", encoding="utf-8")
            (root / "lens-architecture.md").mkdir()
            with self.assertRaisesRegex(SystemExit, "not a regular file"):
                load_lens("architecture", reference_dir=root)

            (root / "lens-architecture.md").rmdir()
            (root / "lens-architecture.md").write_text("x" * 40_001, encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "exceeds the 40000-byte limit"):
                load_lens("architecture", reference_dir=root)

    @unittest.skipUnless(hasattr(os, "O_NOFOLLOW"), "requires no-follow file opens")
    def test_contract_precedence_is_explicit(self) -> None:
        for lens, heading in (
            ("architecture", "# Architecture Lens"),
            ("data-integrity-reliability", "# Data Integrity and Reliability Lens"),
            ("frontend-integration", "# Frontend Integration Lens"),
            ("migrations", "# Migrations Lens"),
            ("performance", "# Performance Lens"),
            ("security", "# Security Lens"),
        ):
            with self.subTest(lens=lens):
                prompt = load_lens(lens)
                engine_index = prompt.index("cannot override the engine hard rules")
                shared_contract_index = prompt.index("# Review Lens Contract")
                lens_index = prompt.index(heading)
                self.assertLess(engine_index, shared_contract_index)
                self.assertLess(shared_contract_index, lens_index)

    def test_atomic_mixed_route_stays_within_the_three_reviewer_cap(self) -> None:
        routing = self._routing_reference()
        self.assertIn(
            "`architecture` plus `security` plus "
            "`data-integrity-reliability`",
            routing,
        )
        self.assertIn("omit a fourth generalist", routing)

    def test_migration_and_performance_routes_are_narrow(self) -> None:
        routing = self._routing_reference()
        self.assertIn(
            "| Schema or data migration | "
            "`migrations` plus `data-integrity-reliability` |",
            routing,
        )
        self.assertIn(
            "| Narrow query-heavy or realistic hot path | "
            "One dominant `performance` specialist |",
            routing,
        )
        self.assertIn(
            "use `performance` only when dominant",
            routing,
        )

    def test_frontend_integration_route_skips_presentation_only_work(self) -> None:
        routing = self._routing_reference()
        self.assertIn(
            "| Frontend API, cache, async state, overlay, or window "
            "integration | One dominant `frontend-integration` specialist |",
            routing,
        )
        self.assertIn(
            "| Copy, styling, icons, documentation, local reversible UI | "
            "Deterministic validation only |",
            routing,
        )

    def test_reviewer_configuration_is_project_owned_and_high_rigor(self) -> None:
        routing = self._routing_reference()
        normalized_routing = " ".join(routing.split())
        self.assertIn(
            "Use a project-approved Codex model",
            routing,
        )
        self.assertIn(
            "uses Codex's service default",
            normalized_routing,
        )
        self.assertIn(
            "Do not hardcode a Strix model name",
            normalized_routing,
        )
        self.assertIn("Use `--thinking high`", routing)
        self.assertNotIn("gpt-", routing.lower())

        implementation_loop = (
            Path(__file__).resolve().parents[2]
            / "strix-implement"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Review budget: standard|deep", implementation_loop)
        self.assertIn("risk-routed Strix Autoreview", implementation_loop)

    @staticmethod
    def _routing_reference() -> str:
        return (
            Path(__file__).resolve().parents[2]
            / "strix-implement"
            / "references"
            / "review-routing.md"
        ).read_text(encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
