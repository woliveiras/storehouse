from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "product-ui-ux-design"
REFERENCE_NAMES = {
    "product-ux-foundations.md",
    "accessibility-and-inclusive-design.md",
    "web-product-design.md",
    "mobile-product-design.md",
    "design-systems.md",
    "saas.md",
    "ecommerce.md",
    "cms.md",
    "crm.md",
    "erp.md",
    "experience-performance.md",
    "usability-verification.md",
}


class ProductUiUxDesignContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

    def test_pud_001_identity_and_interface_metadata(self) -> None:
        frontmatter = yaml.safe_load(self.skill.split("---", 2)[1])
        self.assertEqual("product-ui-ux-design", frontmatter["name"])
        description = frontmatter["description"]
        for token in (
            "design", "audit", "improve", "web", "mobile", "SaaS",
            "e-commerce", "CMS", "CRM", "ERP", "information architecture",
            "navigation", "forms", "tables", "onboarding", "responsive",
            "interaction", "usability", "accessibility", "design systems",
            "game UI", "promotional art", "backend",
        ):
            self.assertIn(token.casefold(), description.casefold())
        metadata = yaml.safe_load(
            (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual(
            {
                "display_name": "Product UI/UX Design",
                "short_description": "Design usable web and mobile products",
                "default_prompt": "Use $product-ui-ux-design to design or review this web or mobile product experience.",
            },
            metadata["interface"],
        )

    def test_pud_002_references_are_exact_direct_and_conditional(self) -> None:
        found = {path.name for path in (SKILL_ROOT / "references").iterdir()}
        self.assertEqual(REFERENCE_NAMES, found)
        self.assertLessEqual(len(self.skill.splitlines()), 150)
        linked = set(re.findall(r"\]\(references/([^)]+)\)", self.skill))
        self.assertEqual(REFERENCE_NAMES, linked)
        for name in REFERENCE_NAMES:
            nearby = self.skill[max(0, self.skill.index(name) - 180) : self.skill.index(name)]
            self.assertRegex(nearby.casefold(), r"read|load")

    def test_pud_003_006_core_and_reference_contract(self) -> None:
        core_tokens = (
            "running interface", "code", "design system", "requirements",
            "analytics", "feedback", "roles", "permissions", "domain vocabulary",
            "component names", "entry", "exit", "loading", "empty", "error",
            "recovery", "offline", "confirmation", "cancellation", "destructive",
            "observations", "evidence", "heuristics", "decisions", "hypotheses",
            "limitations", "keyboard", "touch", "pointer", "assistive",
        )
        for token in core_tokens:
            self.assertIn(token, self.skill.casefold())

        required_by_reference = {
            "product-ux-foundations.md": ("journey", "information architecture", "microcopy", "severity"),
            "accessibility-and-inclusive-design.md": ("wcag 2.2", "keyboard", "focus", "screen reader", "human"),
            "web-product-design.md": ("deep link", "refresh", "multiple tabs", "dense"),
            "mobile-product-design.md": ("ios", "android", "safe area", "virtual keyboard", "back"),
            "design-systems.md": ("token", "variant", "composition", "governance"),
            "saas.md": ("activation", "workspace", "multi-tenancy", "downgrade", "cancel"),
            "ecommerce.md": ("guest checkout", "shipping", "tax", "payment", "return"),
            "cms.md": ("content model", "autosave", "preview", "approval", "version"),
            "crm.md": ("lead", "contact", "account", "opportunit", "deduplic"),
            "erp.md": ("master data", "segregation of duties", "currency", "audit"),
            "experience-performance.md": (
                "experience contract", "core web vitals", "ttid", "ttfd",
                "profiling", "root cause", "optimistic",
            ),
            "usability-verification.md": ("walkthrough", "heuristic", "task-based", "qualitative", "quantitative"),
        }
        for name, tokens in required_by_reference.items():
            text = (SKILL_ROOT / "references" / name).read_text(encoding="utf-8").casefold()
            for token in tokens:
                self.assertIn(token, text, f"{name}:{token}")

    def test_pud_005_sources_and_guardrails_are_explicit(self) -> None:
        accessibility = (
            SKILL_ROOT / "references" / "accessibility-and-inclusive-design.md"
        ).read_text(encoding="utf-8")
        self.assertIn("https://www.w3.org/TR/WCAG22/", accessibility)
        self.assertIn("https://developer.apple.com/", accessibility)
        self.assertIn("https://developer.android.com/", accessibility)
        self.assertIn("normative", accessibility.casefold())
        self.assertIn("platform guidance", accessibility.casefold())
        self.assertIn("automated", accessibility.casefold())

        for guardrail in (
            "trend", "beautiful", "invent", "pop-up", "color", "animation",
            "sound", "dark pattern", "false urgency", "cancellation", "financial",
            "destructive", "crm", "erp", "figma", "browser automation",
            "audit-only", "automated checks", "domain vocabulary",
        ):
            self.assertIn(guardrail, self.skill.casefold())

    def test_pud_007_catalog_and_current_inventory(self) -> None:
        catalog = json.loads(
            (ROOT / "catalog" / "collections.json").read_text(encoding="utf-8")
        )
        collection = next(
            item for item in catalog["collections"] if item["name"] == "product-design"
        )
        self.assertEqual(["product-ui-ux-design"], collection["skills"])
        self.assertIn("Product UI/UX Design", (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_pud_008_011_evaluation_cases(self) -> None:
        catalog = json.loads((ROOT / "evals" / "catalog.json").read_text(encoding="utf-8"))
        routing = next(item for item in catalog["routing"] if item["skill"] == "product-ui-ux-design")
        self.assertEqual("RT-043", routing["criterion"])
        self.assertEqual(
            {"game-ui", "promotional-art", "backend-only"},
            {item["name"] for item in routing["negatives"]},
        )
        behavior = next(item for item in catalog["behavior"] if item["skill"] == "product-ui-ux-design")
        self.assertEqual("BH-043", behavior["criterion"])
        fixture = (ROOT / behavior["fixture"] / "TASK.md").read_text(encoding="utf-8").casefold()
        for token in ("saas", "e-commerce", "cms", "crm", "erp", "accessibility", "error", "not executable"):
            self.assertIn(token, fixture)
        for token in ("experience-performance", "field", "laboratory", "technical root cause", "profiling"):
            self.assertIn(token, fixture)
        composition = next(item for item in catalog["composition"] if item["skill"] == "product-ui-ux-design")
        self.assertEqual("CP-043", composition["criterion"])
        security = next(item for item in catalog["security"] if item["skill"] == "product-ui-ux-design")
        self.assertEqual("SEC-043", security["criterion"])
        self.assertIn("untrusted", security["stimulus"].casefold())

    def test_pud_013_experience_performance_has_clear_engineering_boundary(self) -> None:
        reference = (
            SKILL_ROOT / "references" / "experience-performance.md"
        ).read_text(encoding="utf-8").casefold()
        for source in (
            "https://web.dev/articles/vitals",
            "https://developer.android.com/topic/performance/vitals/launch-time",
            "https://developer.apple.com/documentation/xcode/improving-app-responsiveness",
        ):
            self.assertIn(source, reference)
        for token in (
            "field measurement", "laboratory", "critical task", "perceived performance",
            "cold start", "warm start", "hot start", "hang", "hitch", "offline",
            "do not claim", "technical root cause", "engineering performance",
        ):
            self.assertIn(token, reference)
        self.assertIn(
            "experience-performance.md",
            self.skill,
        )
        self.assertRegex(
            self.skill.casefold(),
            r"experience-performance\.md.*(?:latency|loading|startup|responsiveness)",
        )


if __name__ == "__main__":
    unittest.main()
