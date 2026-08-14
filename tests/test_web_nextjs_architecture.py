from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "web-nextjs-architecture"
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCE_NAMES = {
    "app-router-and-project-structure.md",
    "server-client-boundaries.md",
    "data-actions-and-bff.md",
    "rendering-streaming-and-navigation.md",
    "caching-and-revalidation.md",
    "runtimes-and-deployment.md",
    "security-and-verification.md",
    "pages-router-migration.md",
}


class WebNextjsArchitectureContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assertTrue(
            SKILL_MD.is_file(),
            "fail-first: web-nextjs-architecture has not been implemented",
        )
        self.skill = SKILL_MD.read_text(encoding="utf-8")

    def test_wna_001_identity_and_interface_metadata(self) -> None:
        frontmatter = yaml.safe_load(self.skill.split("---", 2)[1])
        self.assertEqual({"name", "description"}, set(frontmatter))
        self.assertEqual("web-nextjs-architecture", frontmatter["name"])
        description = frontmatter["description"].casefold()
        for token in (
            "next.js",
            "app router",
            "pages router",
            "server component",
            "client component",
            "server action",
            "route handler",
            "cache",
            "render",
            "stream",
            "runtime",
            "deployment",
            "backend service",
        ):
            self.assertIn(token, description)

        metadata = yaml.safe_load(
            (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual(
            {
                "display_name": "Next.js Architecture",
                "short_description": "Design full-stack Next.js architecture",
                "default_prompt": "Use $web-nextjs-architecture to design or review this Next.js application's architecture.",
            },
            metadata["interface"],
        )

    def test_wna_002_references_are_exact_direct_and_conditional(self) -> None:
        found = {path.name for path in (SKILL_ROOT / "references").iterdir()}
        self.assertEqual(REFERENCE_NAMES, found)
        self.assertLessEqual(len(self.skill.splitlines()), 150)
        linked = set(re.findall(r"\]\(references/([^)]+)\)", self.skill))
        self.assertEqual(REFERENCE_NAMES, linked)
        for name in REFERENCE_NAMES:
            nearby = self.skill[max(0, self.skill.index(name) - 220) : self.skill.index(name)]
            self.assertRegex(nearby.casefold(), r"read|load")

    def test_wna_003_core_inspects_versioned_execution_model(self) -> None:
        core = self.skill.casefold()
        for token in (
            "exact next.js",
            "react version",
            "app router",
            "pages router",
            "cachecomponents",
            "node.js",
            "edge",
            "static export",
            "serverless",
            "self-host",
            "route tree",
            "deployment adapter",
            "verified evidence",
            "hypotheses",
        ):
            self.assertIn(token, core)

    def test_wna_004_010_reference_contracts(self) -> None:
        required_by_reference = {
            "app-router-and-project-structure.md": (
                "route group", "private folder", "parallel route", "intercepting route",
                "layout", "bounded context", "nextjs.org/docs/app/getting-started/project-structure",
            ),
            "server-client-boundaries.md": (
                "use client", "server-only", "serializable", "module graph",
                "hydration", "secret", "nextjs.org/docs/app/getting-started/server-and-client-components",
            ),
            "data-actions-and-bff.md": (
                "server component", "server action", "route handler", "webhook",
                "round trip", "backend-service-architecture", "not a full backend replacement",
            ),
            "rendering-streaming-and-navigation.md": (
                "suspense", "streaming", "loading", "error", "not-found",
                "waterfall", "prefetch", "route transition",
            ),
            "caching-and-revalidation.md": (
                "cache components", "use cache", "cachelife", "cachetag",
                "updatetag", "revalidatetag", "revalidatepath", "personalized",
                "multi-instance", "previous model",
            ),
            "runtimes-and-deployment.md": (
                "node.js", "edge runtime", "static export", "serverless",
                "filesystem", "websocket", "reverse proxy", "standalone",
            ),
            "security-and-verification.md": (
                "public-facing", "authorization", "proxy", "optimistic",
                "data access layer", "next_public", "production build", "browser",
            ),
            "pages-router-migration.md": (
                "pages router", "app router", "getserversideprops", "getstaticprops",
                "api routes", "incremental", "rollback",
            ),
        }
        for name, tokens in required_by_reference.items():
            content = (SKILL_ROOT / "references" / name).read_text(encoding="utf-8").casefold()
            for token in tokens:
                self.assertIn(token, content, f"{name}:{token}")

    def test_wna_011_backend_boundary_and_independence(self) -> None:
        core = self.skill.casefold()
        for token in (
            "backend-service-architecture",
            "optional",
            "not a dependency",
            "business capability",
            "transaction",
            "idempotency",
            "microservice",
        ):
            self.assertIn(token, core)
        self.assertIn("full-stack next.js", core)

    def test_wna_012_catalog_inventory_and_docs(self) -> None:
        catalog = json.loads((ROOT / "catalog" / "collections.json").read_text(encoding="utf-8"))
        collection = next(item for item in catalog["collections"] if item["name"] == "nextjs")
        self.assertEqual(["web-nextjs-architecture"], collection["skills"])
        self.assertIn("Next.js architecture", (ROOT / "README.md").read_text(encoding="utf-8"))
        architecture = (ROOT / "docs" / "architecture.md").read_text(encoding="utf-8")
        self.assertIn("47 skills", architecture)
        self.assertIn("web-nextjs-architecture", architecture)

    def test_wna_013_016_evaluation_cases(self) -> None:
        catalog = json.loads((ROOT / "evals" / "catalog.json").read_text(encoding="utf-8"))
        routing = next(item for item in catalog["routing"] if item["skill"] == "web-nextjs-architecture")
        self.assertEqual("RT-046", routing["criterion"])
        self.assertEqual(
            {"backend-only", "react-only", "database-only"},
            {item["name"] for item in routing["negatives"]},
        )
        behavior = next(item for item in catalog["behavior"] if item["skill"] == "web-nextjs-architecture")
        self.assertEqual("BH-046", behavior["criterion"])
        fixture = (ROOT / behavior["fixture"] / "TASK.md").read_text(encoding="utf-8").casefold()
        for token in ("app router", "server component", "server action", "route handler", "cache components", "deployment"):
            self.assertIn(token, fixture)
        composition = next(item for item in catalog["composition"] if item["skill"] == "web-nextjs-architecture")
        self.assertEqual("CP-046", composition["criterion"])
        self.assertIn("backend-service-architecture", composition["related"])
        security = next(item for item in catalog["security"] if item["skill"] == "web-nextjs-architecture")
        self.assertEqual("SEC-046", security["criterion"])
        self.assertIn("untrusted", security["stimulus"].casefold())


if __name__ == "__main__":
    unittest.main()
