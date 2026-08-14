from __future__ import annotations

import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "product-performance-engineering"
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCE_NAMES = {
    "performance-engineering-foundations.md",
    "web-performance.md",
    "android-performance.md",
    "apple-performance.md",
    "cross-platform-mobile.md",
    "performance-testing-and-budgets.md",
    "field-observability.md",
    "experience-and-integrity-boundaries.md",
}


class ProductPerformanceEngineeringContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assertTrue(
            SKILL_MD.is_file(),
            "fail-first: product-performance-engineering has not been implemented",
        )
        self.skill = SKILL_MD.read_text(encoding="utf-8")

    def test_ppe_001_identity_and_interface_metadata(self) -> None:
        frontmatter = yaml.safe_load(self.skill.split("---", 2)[1])
        self.assertEqual(
            {"name", "description"},
            set(frontmatter),
        )
        self.assertEqual("product-performance-engineering", frontmatter["name"])
        description = frontmatter["description"].casefold()
        for token in (
            "diagnos",
            "profil",
            "optimiz",
            "verif",
            "web",
            "android",
            "ios",
            "cross-platform",
            "loading",
            "responsiveness",
            "rendering",
            "startup",
            "network",
            "memory",
            "storage",
            "energy",
            "jank",
            "hang",
            "anr",
            "core web vitals",
            "budget",
            "regression",
            "ui/ux",
            "game performance",
            "postgresql",
            "speculative",
            "release",
            "ci",
            "observability",
        ):
            self.assertIn(token, description)

        metadata = yaml.safe_load(
            (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual(
            {
                "display_name": "Product Performance Engineering",
                "short_description": "Diagnose and optimize web and mobile performance",
                "default_prompt": "Use $product-performance-engineering to diagnose and improve this measured web or mobile performance problem.",
            },
            metadata["interface"],
        )

    def test_ppe_002_references_are_exact_direct_and_conditional(self) -> None:
        found = {path.name for path in (SKILL_ROOT / "references").iterdir()}
        self.assertEqual(REFERENCE_NAMES, found)
        self.assertLessEqual(len(self.skill.splitlines()), 150)
        linked = set(re.findall(r"\]\(references/([^)]+)\)", self.skill))
        self.assertEqual(REFERENCE_NAMES, linked)
        for name in REFERENCE_NAMES:
            nearby = self.skill[max(0, self.skill.index(name) - 200) : self.skill.index(name)]
            self.assertRegex(nearby.casefold(), r"read|load")

    def test_ppe_003_core_workflow_is_measurement_first_and_causal(self) -> None:
        core = self.skill.casefold()
        for token in (
            "running product",
            "code and architecture",
            "framework",
            "runtime",
            "versions",
            "devices",
            "browsers",
            "design system",
            "infrastructure",
            "field",
            "laboratory",
            "trace",
            "profile",
            "task or operation",
            "cache state",
            "data volume",
            "network condition",
            "cold",
            "warm",
            "hot",
            "metric and unit",
            "baseline",
            "percentile",
            "variance",
            "repeatable",
            "hypothesis",
            "critical path",
            "fail-first",
            "smallest causal",
            "functional equivalence",
            "distribution",
            "physical-device",
            "limitations",
        ):
            self.assertIn(token, core)
        self.assertRegex(core, r"(?:measure|baseline).*(?:before|precedes).*optimiz")
        self.assertRegex(core, r"root cause.*profil")

    def test_ppe_004_010_reference_contracts(self) -> None:
        required_by_reference = {
            "performance-engineering-foundations.md": (
                "baseline",
                "hypothesis",
                "profiling",
                "causality",
                "variance",
                "percentile",
                "functional equivalence",
                "priorit",
            ),
            "web-performance.md": (
                "lcp",
                "inp",
                "cls",
                "field",
                "laboratory",
                "critical rendering path",
                "long task",
                "hydration",
                "service worker",
                "third-party",
                "memory",
                "route transition",
            ),
            "android-performance.md": (
                "ttid",
                "ttfd",
                "cold",
                "warm",
                "hot",
                "jank",
                "frozen frame",
                "anr",
                "compose",
                "views",
                "perfetto",
                "android vitals",
                "macrobenchmark",
                "microbenchmark",
                "baseline profile",
                "battery",
            ),
            "apple-performance.md": (
                "launch",
                "hang",
                "hitch",
                "instruments",
                "time profiler",
                "metrickit",
                "signpost",
                "swiftui",
                "uikit",
                "memory",
                "energy",
                "physical device",
            ),
            "cross-platform-mobile.md": (
                "react native",
                "kotlin multiplatform",
                "bridge",
                "serialization",
                "interop",
                "android",
                "ios",
                "simulator",
            ),
            "performance-testing-and-budgets.md": (
                "regression",
                "warmup",
                "repetition",
                "distribution",
                "threshold",
                "noise",
                "ci",
                "budget",
                "flaky",
            ),
            "field-observability.md": (
                "rum",
                "android vitals",
                "metrickit",
                "segment",
                "privacy",
                "sampling",
                "correlation",
                "release",
                "telemetry",
            ),
            "experience-and-integrity-boundaries.md": (
                "product-ui-ux-design",
                "optional",
                "functional equivalence",
                "accessibility",
                "security",
                "privacy",
                "consistency",
                "loading",
                "skeleton",
            ),
        }
        for name, tokens in required_by_reference.items():
            text = (SKILL_ROOT / "references" / name).read_text(encoding="utf-8").casefold()
            for token in tokens:
                self.assertIn(token, text, f"{name}:{token}")

    def test_ppe_011_primary_sources_and_evidence_classes(self) -> None:
        combined = "\n".join(
            (SKILL_ROOT / "references" / name).read_text(encoding="utf-8")
            for name in REFERENCE_NAMES
        )
        for source in (
            "https://web.dev/articles/vitals",
            "https://developer.android.com/topic/performance/vitals/launch-time",
            "https://developer.apple.com/documentation/xcode/performance-and-metrics",
            "https://reactnative.dev/docs/profiling",
        ):
            self.assertIn(source, combined)
        for evidence_class in (
            "normative standard",
            "platform guidance",
            "vendor metric",
            "empirical evidence",
            "skill recommendation",
        ):
            self.assertIn(evidence_class, combined.casefold())

    def test_ppe_011a_excluded_cross_platform_stacks_are_absent(self) -> None:
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in SKILL_ROOT.rglob("*")
            if path.is_file()
        ).casefold()
        for excluded in ("flutter", "capacitor", "ionic"):
            self.assertNotIn(excluded, combined)

    def test_ppe_012_guardrails_and_ui_ux_boundary(self) -> None:
        combined = self.skill.casefold() + "\n" + (
            SKILL_ROOT / "references" / "experience-and-integrity-boundaries.md"
        ).read_text(encoding="utf-8").casefold()
        for token in (
            "without a baseline",
            "root cause without profiling",
            "best run",
            "lower budgets",
            "functional correctness",
            "accessibility",
            "permissions",
            "data protection",
            "skeleton",
            "cache",
            "invalidation",
            "concurrency",
            "race condition",
            "background",
            "memoization",
            "lazy loading",
            "virtualization",
            "pooling",
            "emulator",
            "simulator",
            "external service",
            "production load",
            "diagnosis-only",
            "install",
            "field performance",
            "usability",
            "product-ui-ux-design",
            "works independently",
        ):
            self.assertIn(token, combined)

    def test_ppe_013_catalog_architecture_and_current_inventory(self) -> None:
        catalog = json.loads(
            (ROOT / "catalog" / "collections.json").read_text(encoding="utf-8")
        )
        collection = next(
            item
            for item in catalog["collections"]
            if item["name"] == "product-performance"
        )
        self.assertEqual(["product-performance-engineering"], collection["skills"])
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        architecture = (ROOT / "docs" / "architecture.md").read_text(encoding="utf-8")
        self.assertIn("Product Performance Engineering", readme)
        self.assertIn("48 directories", readme)
        self.assertIn("48 skills", architecture)
        self.assertIn("product-performance-engineering", architecture)

    def test_ppe_014_evaluation_cases_and_composition(self) -> None:
        catalog = json.loads((ROOT / "evals" / "catalog.json").read_text(encoding="utf-8"))
        routing = next(
            item
            for item in catalog["routing"]
            if item["skill"] == "product-performance-engineering"
        )
        self.assertEqual("RT-044", routing["criterion"])
        self.assertEqual(
            {"ui-ux-only", "game-performance", "postgresql-only", "ci-release-only"},
            {item["name"] for item in routing["negatives"]},
        )
        behavior = next(
            item
            for item in catalog["behavior"]
            if item["skill"] == "product-performance-engineering"
        )
        self.assertEqual("BH-044", behavior["criterion"])
        fixture = (ROOT / behavior["fixture"] / "TASK.md").read_text(
            encoding="utf-8"
        ).casefold()
        for token in (
            "lcp",
            "critical rendering path",
            "long task",
            "layout instability",
            "ttid",
            "ttfd",
            "jank",
            "anr",
            "hang",
            "hitch",
            "memory",
            "lifecycle",
            "cross-platform",
            "functional equivalence",
            "missing measurement",
        ):
            self.assertIn(token, fixture)
        composition = next(
            item
            for item in catalog["composition"]
            if item["skill"] == "product-performance-engineering"
        )
        self.assertEqual("CP-044", composition["criterion"])
        self.assertEqual(["product-ui-ux-design"], composition["related"])
        variants = {item["name"]: item for item in composition["variants"]}
        self.assertTrue(variants["composed-specialized"]["applicable"])
        self.assertTrue(variants["baseline-minimal"]["applicable"])
        security = next(
            item
            for item in catalog["security"]
            if item["skill"] == "product-performance-engineering"
        )
        self.assertEqual("SEC-044", security["criterion"])
        self.assertIn("trace", security["stimulus"].casefold())
        self.assertIn("production", security["stimulus"].casefold())

    def test_ppe_015_behavior_oracle_rejects_unsafe_claims(self) -> None:
        from evals.oracle_data import ORACLES
        from evals.verifiers import verify_workspace

        fixture = ROOT / "evals" / "fixtures" / "product-performance-engineering"
        oracle = ORACLES["product-performance-engineering"]
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp) / "workspace"
            shutil.copytree(fixture, workspace)
            self.assertEqual("fail", verify_workspace("product-performance-engineering", workspace)["status"])
            for output in oracle["outputs"]:
                target = workspace / output["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(output["sample"], encoding="utf-8")
            self.assertEqual("pass", verify_workspace("product-performance-engineering", workspace)["status"])

            report = workspace / "performance-analysis.md"
            pristine = report.read_text(encoding="utf-8")
            mutants = (
                ("Baseline: repeated samples", "Baseline: absent"),
                ("median and p95", "best run only"),
                ("Functional equivalence: failed; candidate rejected", "Functional equivalence: passed"),
                ("Field improvement: not claimed", "Field improvement: verified"),
                ("Root cause: unsupported without profile", "Root cause: database verified"),
                ("Budget unchanged: 2500 ms", "Budget relaxed: 3500 ms"),
                ("Skeleton is not an optimization", "Skeleton hides the delay"),
                ("Physical-device verification: unavailable", "Simulator proves physical performance"),
            )
            for original, replacement in mutants:
                with self.subTest(mutant=original):
                    self.assertIn(original, pristine)
                    report.write_text(pristine.replace(original, replacement, 1), encoding="utf-8")
                    self.assertEqual(
                        "fail",
                        verify_workspace("product-performance-engineering", workspace)["status"],
                    )
            report.write_text(pristine, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
