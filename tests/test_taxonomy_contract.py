from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

EXPECTED_SKILLS = {
    "ai-eng-agent-design",
    "ai-eng-llm-integration",
    "ai-eng-rag-pipeline",
    "backend-service-architecture",
    "ci-ai-eng",
    "ci-android",
    "ci-game-dev-2d",
    "ci-go",
    "ci-python",
    "ci-rust",
    "ci-terraform",
    "ci-typescript",
    "cloud-ops",
    "cloud-supabase",
    "database-postgresql",
    "game-dev-2d-ai",
    "game-dev-2d-art",
    "game-dev-2d-audio",
    "game-dev-2d-feel",
    "game-dev-2d-gameplay",
    "game-dev-2d-performance",
    "game-dev-2d-procedural-generation",
    "game-dev-2d-save-progression",
    "game-dev-2d-testing",
    "game-dev-2d-ui-accessibility",
    "infra-terraform",
    "product-performance-engineering",
    "product-security-privacy-engineering",
    "product-ui-ux-design",
    "release-android",
    "release-ai-eng",
    "release-game-dev-2d",
    "release-go",
    "release-python",
    "release-rust",
    "release-terraform",
    "release-typescript",
    "research-case-study-design",
    "research-paper-authoring",
    "sdd-specification",
    "web-nextjs-architecture",
    "web-state-xstate",
    "web-state-zustand",
    "web-validation-zod",
    "writing-academic-edit",
    "writing-blog-post",
    "writing-technical-edit",
}


class TaxonomyContractTests(unittest.TestCase):
    def test_exact_domain_first_inventory(self) -> None:
        found = {path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()}
        self.assertEqual(EXPECTED_SKILLS, found)
        self.assertEqual(47, len(found))

    def test_directory_and_frontmatter_names_match(self) -> None:
        for name in sorted(EXPECTED_SKILLS):
            raw = (SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8")
            metadata = yaml.safe_load(raw.split("---", 2)[1])
            self.assertEqual(name, metadata["name"])
            self.assertRegex(name, SKILL_NAME)
            self.assertLess(len(name), 64)

    def test_ci_and_release_technology_suffixes_are_symmetric(self) -> None:
        ci = {name.removeprefix("ci-") for name in EXPECTED_SKILLS if name.startswith("ci-")}
        release = {
            name.removeprefix("release-")
            for name in EXPECTED_SKILLS
            if name.startswith("release-")
        }
        self.assertEqual(
            {
                "ai-eng",
                "android",
                "game-dev-2d",
                "go",
                "python",
                "rust",
                "terraform",
                "typescript",
            },
            ci,
        )
        self.assertEqual(ci, release)

    def test_progressive_provider_and_framework_references_exist(self) -> None:
        expected = {
            "backend-service-architecture": {"nestjs.md", "fastapi.md", "fiber.md"},
            "ai-eng-rag-pipeline": {"chromadb.md", "pgvector.md"},
            "ai-eng-agent-design": {"langgraph.md", "crewai.md"},
            "cloud-ops": {"google-cloud.md", "aws.md"},
            "database-postgresql": {
                "modeling.md",
                "query-review.md",
                "performance.md",
                "migrations-and-operations.md",
            },
            "writing-blog-post": {
                "technical-blog-structure.md",
                "voice-and-style.md",
                "astro-mdx.md",
                "quality-checklist.md",
            },
            "product-ui-ux-design": {
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
            },
            "product-performance-engineering": {
                "performance-engineering-foundations.md",
                "web-performance.md",
                "android-performance.md",
                "apple-performance.md",
                "cross-platform-mobile.md",
                "performance-testing-and-budgets.md",
                "field-observability.md",
                "experience-and-integrity-boundaries.md",
            },
            "product-security-privacy-engineering": {
                "security-privacy-foundations.md",
                "identity-authorization-and-tenancy.md",
                "web-and-api-security.md",
                "mobile-product-security.md",
                "sensitive-data-lifecycle.md",
                "application-security-testing.md",
                "incident-containment-and-recovery.md",
                "regulated-data-and-compliance-claims.md",
            },
            "web-nextjs-architecture": {
                "app-router-and-project-structure.md",
                "server-client-boundaries.md",
                "data-actions-and-bff.md",
                "rendering-streaming-and-navigation.md",
                "caching-and-revalidation.md",
                "runtimes-and-deployment.md",
                "security-and-verification.md",
                "pages-router-migration.md",
            },
        }
        for skill, references in expected.items():
            found = {
                path.name
                for path in (SKILLS_ROOT / skill / "references").iterdir()
                if path.is_file()
            }
            self.assertEqual(references, found, skill)


if __name__ == "__main__":
    unittest.main()
