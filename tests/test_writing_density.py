from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def read_skill(name: str) -> str:
    root = SKILLS / name
    content = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(root.rglob("*.md"))
    )
    return " ".join(content.casefold().split())


class WritingDensityContractTests(unittest.TestCase):
    def test_wd_001_all_writing_skills_require_a_density_pass(self) -> None:
        for name in (
            "writing-blog-post",
            "writing-technical-edit",
            "writing-academic-edit",
        ):
            with self.subTest(skill=name):
                skill = read_skill(name)
                self.assertIn("information density", skill)
                self.assertIn("match length to complexity", skill)
                self.assertIn("loss test", skill)

    def test_wd_002_blog_density_does_not_require_recap_sections(self) -> None:
        skill = read_skill("writing-blog-post")
        self.assertIn("omit the conclusion", skill)
        self.assertIn("necessary caveat", skill)

    def test_wd_003_technical_density_preserves_substance(self) -> None:
        skill = read_skill("writing-technical-edit")
        self.assertIn("accuracy outranks brevity", skill)
        self.assertIn("do not manufacture", skill)

    def test_wd_004_academic_density_preserves_scientific_scope(self) -> None:
        skill = read_skill("writing-academic-edit")
        self.assertIn("accuracy outranks brevity", skill)
        self.assertIn("legitimate uncertainty", skill)

    def test_wd_005_chat_specific_paragraph_limit_is_not_imported(self) -> None:
        for name in (
            "writing-blog-post",
            "writing-technical-edit",
            "writing-academic-edit",
        ):
            with self.subTest(skill=name):
                self.assertNotIn("2–5 compact paragraphs", read_skill(name))


if __name__ == "__main__":
    unittest.main()
