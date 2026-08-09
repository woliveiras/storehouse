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
        self.assertEqual(42, len(found))

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
