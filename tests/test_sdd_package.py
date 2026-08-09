from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


class SddPackageTests(unittest.TestCase):
    def test_sdd_collection_is_canonical_selective_and_installable(self) -> None:
        catalog = json.loads((ROOT / "catalog/collections.json").read_text(encoding="utf-8"))
        sdd = next(item for item in catalog["collections"] if item["name"] == "sdd")
        self.assertEqual(["sdd-specification"], sdd["skills"])
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("### `sdd`", readme)
        self.assertIn("--skill sdd-specification", readme)

    def test_sdd_skill_owns_the_complete_method(self) -> None:
        root = SKILLS / "sdd-specification"
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
        metadata = (root / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn("name: sdd-specification", skill)
        for required in (
            "metadata-first",
            "stable acceptance criteria",
            "behavior/oracle matrix",
            "provenance",
            "reconcile",
            "formal SDD review",
        ):
            self.assertIn(required, skill)
        self.assertIn("allow_implicit_invocation: true", metadata)
        for relative in (
            "assets/spec-template.md",
            "assets/behavior-matrix-template.md",
            "assets/evidence-template.md",
            "references/metadata.md",
            "references/behavior-matrix.md",
            "references/provenance.md",
            "references/review-contract.md",
        ):
            self.assertTrue((root / relative).is_file(), relative)

    def test_sdd_is_independent_and_composes_by_capability(self) -> None:
        text = "\n".join(path.read_text(encoding="utf-8") for path in (SKILLS / "sdd-specification").rglob("*.md"))
        self.assertIn("optional", text.lower())
        self.assertIn("TDD capability", text)
        self.assertIn("review capability", text)
        self.assertNotIn("/Developer/woliveiras/baseline", text)
        self.assertNotIn("import ", text)

    def test_baseline_workflows_are_not_duplicated(self) -> None:
        inventory = {path.name for path in SKILLS.iterdir() if path.is_dir()}
        self.assertFalse({"tdd", "bugfix", "verify"} & inventory)
        self.assertIn("sdd-specification", inventory)

    def test_git_is_the_default_archive_for_inactive_sdd_artifacts(self) -> None:
        contract = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        reconciliation = (SKILLS / "sdd-specification/references/reconciliation.md").read_text(encoding="utf-8")
        self.assertIn("Git is the default archive", contract)
        self.assertIn("Git history is the default archive", reconciliation)


if __name__ == "__main__":
    unittest.main()
