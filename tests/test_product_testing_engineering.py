from __future__ import annotations

import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "product-testing-engineering"
SKILL_MD = SKILL_ROOT / "SKILL.md"
DESCRIPTION = (
    "Design, implement when authorized, review, and evolve risk-based test systems "
    "for web and mobile products across unit, component, integration, contract, "
    "end-to-end, accessibility, resilience, persistence, and platform boundaries. "
    "Use when selecting test seams, building deterministic fixtures, diagnosing "
    "flaky tests, designing coverage, or verifying APIs, state, offline behavior, "
    "concurrency, and tenant isolation. Do not use for implementing one approved "
    "behavior through TDD, ordinary CI wiring, performance benchmarking, "
    "security-only testing, game testing, or manual QA alone."
)
REFERENCE_NAMES = {
    "risk-based-testing-foundations.md",
    "unit-and-component-testing.md",
    "integration-contract-and-api-testing.md",
    "end-to-end-and-journey-testing.md",
    "mobile-offline-and-device-testing.md",
    "data-tenancy-and-migration-testing.md",
    "determinism-isolation-and-flakiness.md",
    "coverage-oracles-and-evidence.md",
    "accessibility-and-visual-testing.md",
}
ASSET_NAMES = {
    "risk-coverage-matrix-template.md",
    "test-strategy-template.md",
}


class ProductTestingEngineeringContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assertTrue(
            SKILL_MD.is_file(),
            "fail-first: product-testing-engineering has not been implemented",
        )
        self.skill = SKILL_MD.read_text(encoding="utf-8")

    def test_pte_001_exact_identity_description_and_interface_metadata(self) -> None:
        frontmatter = yaml.safe_load(self.skill.split("---", 2)[1])
        self.assertEqual(
            {"name": "product-testing-engineering", "description": DESCRIPTION},
            frontmatter,
        )
        metadata = yaml.safe_load(
            (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual(
            {
                "display_name": "Product Testing Engineering",
                "short_description": "Design reliable web and mobile product test systems",
                "default_prompt": "Use $product-testing-engineering to design a risk-based test strategy for this web or mobile product.",
            },
            metadata["interface"],
        )

    def test_pte_002_routing_is_specific_positive_and_negative(self) -> None:
        description = yaml.safe_load(self.skill.split("---", 2)[1])[
            "description"
        ].casefold()
        for token in (
            "risk-based",
            "web",
            "mobile",
            "unit",
            "component",
            "integration",
            "contract",
            "end-to-end",
            "accessibility",
            "resilience",
            "persistence",
            "test seams",
            "deterministic fixtures",
            "flaky tests",
            "coverage",
            "apis",
            "offline",
            "concurrency",
            "tenant isolation",
            "tdd",
            "ci wiring",
            "performance benchmarking",
            "security-only",
            "game testing",
            "manual qa alone",
        ):
            self.assertIn(token, description)

    def test_pte_003_resources_are_exact_direct_and_conditional(self) -> None:
        references = {path.name for path in (SKILL_ROOT / "references").iterdir()}
        assets = {path.name for path in (SKILL_ROOT / "assets").iterdir()}
        self.assertEqual(REFERENCE_NAMES, references)
        self.assertEqual(ASSET_NAMES, assets)
        self.assertLessEqual(len(self.skill.splitlines()), 150)
        linked = set(re.findall(r"\]\(references/([^)]+)\)", self.skill))
        self.assertEqual(REFERENCE_NAMES, linked)
        for name in REFERENCE_NAMES:
            nearby = self.skill[
                max(0, self.skill.index(name) - 260) : self.skill.index(name)
            ]
            self.assertRegex(nearby.casefold(), r"read|load")
        for name in ASSET_NAMES:
            self.assertIn(f"assets/{name}", self.skill)

    def test_pte_004_core_workflow_is_risk_first_and_oracle_driven(self) -> None:
        core = self.skill.split("---", 2)[2].casefold()
        for token in (
            "governing behavior",
            "contracts",
            "risks",
            "architecture",
            "platforms",
            "failure history",
            "journeys",
            "invariants",
            "boundaries",
            "states",
            "consequences",
            "prioritize by risk",
            "public seam",
            "independent oracle",
            "plausibly wrong",
            "unit",
            "component",
            "integration",
            "contract",
            "end-to-end",
            "clock",
            "ids",
            "randomness",
            "network",
            "concurrency",
            "data",
            "fixtures",
            "fail-first",
            "behavioral reason",
            "success",
            "failure",
            "boundary",
            "replay",
            "retry",
            "duplication",
            "offline",
            "recovery",
            "flakiness",
            "browser",
            "physical device",
            "human",
            "residual risk",
        ):
            self.assertIn(token, core)
        self.assertLess(core.index("prioritize by risk"), core.index("public seam"))
        self.assertLess(core.index("public seam"), core.index("independent oracle"))

    def test_pte_005_reference_contracts_cover_the_required_system(self) -> None:
        required_by_reference = {
            "risk-based-testing-foundations.md": (
                "risk",
                "consequence",
                "likelihood",
                "detectability",
                "journey",
                "invariant",
                "boundary",
                "heuristic",
                "test pyramid",
            ),
            "unit-and-component-testing.md": (
                "public seam",
                "observable behavior",
                "implementation detail",
                "test double",
                "fake",
                "mock",
                "testing library",
                "vitest",
            ),
            "integration-contract-and-api-testing.md": (
                "integration",
                "contract",
                "api",
                "consumer",
                "provider",
                "openapi",
                "retry",
                "idempotency",
                "failure",
            ),
            "end-to-end-and-journey-testing.md": (
                "end-to-end",
                "critical journey",
                "playwright",
                "locator",
                "auto-wait",
                "production",
                "external",
                "flaky",
            ),
            "mobile-offline-and-device-testing.md": (
                "android",
                "apple",
                "react native",
                "offline",
                "reconnect",
                "background",
                "process death",
                "emulator",
                "simulator",
                "physical device",
            ),
            "data-tenancy-and-migration-testing.md": (
                "persistence",
                "tenant",
                "cross-tenant",
                "migration",
                "rollback",
                "concurrency",
                "transaction",
                "serialization",
                "synthetic",
            ),
            "determinism-isolation-and-flakiness.md": (
                "clock",
                "randomness",
                "id",
                "network",
                "parallel",
                "cleanup",
                "shared state",
                "sleep",
                "retry",
                "root cause",
            ),
            "coverage-oracles-and-evidence.md": (
                "coverage",
                "not proof",
                "oracle",
                "independent",
                "mutant",
                "fail-first",
                "evidence",
                "limitation",
            ),
            "accessibility-and-visual-testing.md": (
                "wcag",
                "w3c",
                "keyboard",
                "screen reader",
                "visual",
                "snapshot",
                "human",
                "conformance",
            ),
        }
        for name, tokens in required_by_reference.items():
            text = (SKILL_ROOT / "references" / name).read_text(
                encoding="utf-8"
            ).casefold()
            for token in tokens:
                self.assertIn(token, text, f"{name}:{token}")

    def test_pte_006_primary_sources_and_evidence_classes(self) -> None:
        combined = "\n".join(
            (SKILL_ROOT / "references" / name).read_text(encoding="utf-8")
            for name in REFERENCE_NAMES
        )
        for source in (
            "https://testing-library.com/docs/guiding-principles",
            "https://playwright.dev/docs/best-practices",
            "https://vitest.dev/guide/mocking",
            "https://www.w3.org/WAI/test-evaluate/",
            "https://developer.android.com/training/testing/fundamentals/strategies",
            "https://developer.apple.com/documentation/xcode/testing",
            "https://reactnative.dev/docs/testing-overview",
            "https://spec.openapis.org/oas/",
            "https://www.postgresql.org/docs/current/transaction-iso.html",
        ):
            self.assertIn(source, combined)
        for evidence_class in (
            "normative standard",
            "official platform guidance",
            "official tool guidance",
            "empirical evidence",
            "engineering heuristic",
        ):
            self.assertIn(evidence_class, combined.casefold())

    def test_pte_007_guardrails_reject_common_false_confidence(self) -> None:
        combined = self.skill.casefold() + "\n" + "\n".join(
            (SKILL_ROOT / "references" / name)
            .read_text(encoding="utf-8")
            .casefold()
            for name in REFERENCE_NAMES
        )
        for token in (
            "maximize test count",
            "coverage percentage",
            "universal test pyramid",
            "mock everything",
            "private implementation",
            "rewrite assertions",
            "arbitrary sleeps",
            "indiscriminate retries",
            "production data",
            "real data",
            "simulator",
            "physical device",
            "manual checklist",
            "invent",
            "strategy-only",
            "diagnosis-only",
            "device farm",
            "production",
        ):
            self.assertIn(token, combined)

    def test_pte_008_ownership_boundaries_and_standalone_operation(self) -> None:
        combined = self.skill.casefold() + "\n" + (
            SKILL_ROOT / "references" / "risk-based-testing-foundations.md"
        ).read_text(encoding="utf-8").casefold()
        for token in (
            "baseline tdd",
            "one approved behavior",
            "fail-first check",
            "ci-typescript",
            "ci-android",
            "workflow",
            "matrix",
            "cache",
            "permissions",
            "product-performance-engineering",
            "metrics",
            "profiling",
            "benchmark",
            "product-security-privacy-engineering",
            "threat",
            "trust boundaries",
            "abuse cases",
            "product-ui-ux-design",
            "experience",
            "accessibility",
            "game-dev-2d-testing",
            "phaser",
            "godot",
            "works independently",
            "optionally",
        ):
            self.assertIn(token, combined)

    def test_pte_009_assets_are_reusable_and_complete(self) -> None:
        matrix = (
            SKILL_ROOT / "assets" / "risk-coverage-matrix-template.md"
        ).read_text(encoding="utf-8").casefold()
        strategy = (
            SKILL_ROOT / "assets" / "test-strategy-template.md"
        ).read_text(encoding="utf-8").casefold()
        for token in (
            "risk",
            "seam",
            "level",
            "fixture",
            "oracle",
            "evidence",
            "residual",
        ):
            self.assertIn(token, matrix)
        for token in (
            "scope",
            "authority",
            "risk",
            "coverage",
            "determinism",
            "isolation",
            "flakiness",
            "device",
            "accessibility",
            "limitations",
        ):
            self.assertIn(token, strategy)

    def test_pte_010_catalog_architecture_readme_and_inventory(self) -> None:
        catalog = json.loads(
            (ROOT / "catalog" / "collections.json").read_text(encoding="utf-8")
        )
        collection = next(
            item for item in catalog["collections"] if item["name"] == "product-testing"
        )
        self.assertEqual(["product-testing-engineering"], collection["skills"])
        self.assertIn("Product Testing Engineering", collection["description"])
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        architecture = (ROOT / "docs" / "architecture.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Product Testing Engineering", readme)
        self.assertIn("--skill product-testing-engineering", readme)
        self.assertIn("48 directories", readme)
        self.assertIn("48 skills", architecture)
        self.assertIn("product-testing-engineering", architecture)

    def test_pte_011_routing_behavior_composition_and_security_cases(self) -> None:
        catalog = json.loads(
            (ROOT / "evals" / "catalog.json").read_text(encoding="utf-8")
        )
        routing = next(
            item
            for item in catalog["routing"]
            if item["skill"] == "product-testing-engineering"
        )
        self.assertEqual("RT-048", routing["criterion"])
        self.assertTrue(routing["implicit"]["applicable"])
        self.assertEqual(
            {
                "baseline-tdd",
                "ci-workflow",
                "performance-benchmark",
                "security-threat-model",
                "game-testing",
            },
            {item["name"] for item in routing["negatives"]},
        )
        baseline_negative = next(
            item for item in routing["negatives"] if item["name"] == "baseline-tdd"
        )
        self.assertEqual("tdd", baseline_negative["against"])
        self.assertEqual("tdd", baseline_negative["external_baseline_skill"])

        behavior = next(
            item
            for item in catalog["behavior"]
            if item["skill"] == "product-testing-engineering"
        )
        self.assertEqual("BH-048", behavior["criterion"])
        self.assertEqual(["product-test-strategy.md"], behavior["required_outputs"])
        self.assertTrue(behavior["reject_noop"])

        composition = next(
            item
            for item in catalog["composition"]
            if item["skill"] == "product-testing-engineering"
        )
        self.assertEqual("CP-048", composition["criterion"])
        self.assertEqual(
            [
                "product-security-privacy-engineering",
                "product-performance-engineering",
                "product-ui-ux-design",
            ],
            composition["related"],
        )
        variants = {item["name"]: item for item in composition["variants"]}
        for name in ("control", "focal", "composed-specialized", "baseline-minimal"):
            self.assertTrue(variants[name]["applicable"])
        composed = variants["composed-specialized"]["oracle"].casefold()
        for token in (
            "testing",
            "security",
            "performance",
            "ui/ux",
            "ownership",
        ):
            self.assertIn(token, composed)

        security = next(
            item
            for item in catalog["security"]
            if item["skill"] == "product-testing-engineering"
        )
        self.assertEqual("SEC-048", security["criterion"])
        for token in (
            "canary",
            "delete",
            "threshold",
            "real data",
            "production",
            "protected",
        ):
            self.assertIn(token, security["stimulus"].casefold())
        self.assertTrue(security["trajectory_policy"]["required"])
        self.assertEqual(
            "needs-review", security["trajectory_policy"]["unavailable_verdict"]
        )

    def test_pte_012_fixture_oracle_and_verifier_reject_targeted_mutants(self) -> None:
        from evals.oracle_data import ORACLES
        from evals.verifiers import verify_workspace

        fixture = ROOT / "evals" / "fixtures" / "product-testing-engineering"
        oracle = ORACLES["product-testing-engineering"]
        self.assertEqual(
            {"product-test-evidence.json"}, set(oracle["inputs"])
        )
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp) / "workspace"
            shutil.copytree(fixture, workspace)
            self.assertEqual(
                "fail", verify_workspace("product-testing-engineering", workspace)["status"]
            )
            output = oracle["outputs"][0]
            target = workspace / output["path"]
            target.write_text(output["sample"], encoding="utf-8")
            self.assertEqual(
                "pass", verify_workspace("product-testing-engineering", workspace)["status"]
            )
            mutants = (
                (
                    "Coverage is supporting evidence, never proof.",
                    "100% coverage proves the product is correct.",
                ),
                (
                    "Assertions remain behavior-derived and unchanged.",
                    "Assertions were weakened to accept the current behavior.",
                ),
                (
                    "No production, external end-to-end, or device-farm execution was performed.",
                    "Production end-to-end and device-farm execution passed.",
                ),
                (
                    "Tenant crossing is denied in both directions.",
                    "Tenant crossing is allowed for shared fixtures.",
                ),
            )
            calibrated = target.read_text(encoding="utf-8")
            for original, replacement in mutants:
                with self.subTest(mutant=original):
                    self.assertIn(original, calibrated)
                    target.write_text(
                        calibrated.replace(original, replacement, 1),
                        encoding="utf-8",
                    )
                    self.assertEqual(
                        "fail",
                        verify_workspace("product-testing-engineering", workspace)[
                            "status"
                        ],
                    )
                    target.write_text(calibrated, encoding="utf-8")

    def test_pte_013_fixture_covers_required_product_risks(self) -> None:
        evidence = json.loads(
            (
                ROOT
                / "evals"
                / "fixtures"
                / "product-testing-engineering"
                / "product-test-evidence.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual({"web", "mobile", "api", "persistence", "tenancy"}, set(evidence["surfaces"]))
        joined = json.dumps(evidence).casefold()
        for token in (
            "excessive mocks",
            "sleep",
            "wall clock",
            "shared data",
            "100%",
            "offline",
            "retry",
            "duplicate",
            "tenant",
            "migration",
            "accessibility",
            "simulator",
        ):
            self.assertIn(token, joined)

    def test_pte_014_external_baseline_tdd_negative_is_materializable(self) -> None:
        from evals.runner import _record

        catalog = json.loads(
            (ROOT / "evals" / "catalog.json").read_text(encoding="utf-8")
        )
        record = _record(catalog, "RT-048:negative-baseline-tdd")
        self.assertEqual("tdd", record["expected_skill"])
        self.assertEqual("tdd", record["external_baseline_skill"])
        self.assertEqual("product-testing-engineering", record["avoid_skill"])

    def test_pte_015_no_auxiliary_or_consumer_runtime_files(self) -> None:
        allowed = {
            "SKILL.md",
            "agents/openai.yaml",
            *(f"assets/{name}" for name in ASSET_NAMES),
            *(f"references/{name}" for name in REFERENCE_NAMES),
        }
        found = {
            path.relative_to(SKILL_ROOT).as_posix()
            for path in SKILL_ROOT.rglob("*")
            if path.is_file()
        }
        self.assertEqual(allowed, found)
        for forbidden in (
            "README.md",
            "package.json",
            "pyproject.toml",
            "requirements.txt",
            "uv.lock",
            "pnpm-lock.yaml",
        ):
            self.assertNotIn(forbidden, found)


if __name__ == "__main__":
    unittest.main()
