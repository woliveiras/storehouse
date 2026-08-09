from __future__ import annotations

import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGACY_TOKEN = "tuxe" + "do"
BASELINE_SKILLS = {
    "brainstorming",
    "bugfix",
    "ci-workflow",
    "decision-framework",
    "design-deep-modules",
    "docs",
    "git-commit",
    "improve-architecture",
    "measurer",
    "premortem",
    "refine",
    "security-review",
    "session-bridge",
    "shape-domain",
    "tdd",
    "technical-research",
    "verify",
}


def tracked_legacy_matches() -> list[str]:
    tracked = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout.split(b"\0")
    matches: list[str] = []
    for raw in tracked:
        if not raw:
            continue
        relative = raw.decode()
        path = ROOT / relative
        if not path.exists() and not path.is_symlink():
            continue
        candidate = relative.lower()
        if path.is_symlink():
            candidate += "\n" + os.readlink(path).lower()
        elif path.is_file():
            candidate += "\n" + path.read_text(encoding="utf-8", errors="ignore").lower()
        if LEGACY_TOKEN in candidate:
            matches.append(relative)
    return matches


class BaselineIntegrationTests(unittest.TestCase):
    def test_current_tree_has_no_legacy_companion_identity(self):
        self.assertEqual([], tracked_legacy_matches())

    def test_current_product_relationship_is_documented(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("## Storehouse and Baseline", readme)
        self.assertIn("Baseline provides the foundation", readme)
        self.assertIn("Storehouse provides optional depth", readme)
        self.assertIn("woliveiras/baseline", readme)

    def test_catalog_and_composition_use_baseline_identity(self):
        config = (ROOT / "evals/config.py").read_text(encoding="utf-8")
        catalog = (ROOT / "evals/catalog.json").read_text(encoding="utf-8")
        runner = (ROOT / "evals/runner.py").read_text(encoding="utf-8")
        isolation = (ROOT / "evals/isolation.py").read_text(encoding="utf-8")
        combined = "\n".join((config, catalog, runner, isolation))
        for marker in (
            "BASELINE_COMMIT",
            "STOREHOUSE_BASELINE_SOURCE",
            "baseline_presence_prompt",
            "baseline-minimal",
            "baseline-full-plugin",
            "plugins/baseline/skills",
            "external Baseline verify",
        ):
            self.assertIn(marker, combined)
        self.assertIn(
            'repository / "plugins" / "baseline" / "skills"',
            runner,
        )
        self.assertNotIn('repository / "plugins" / "control"', runner)
        self.assertNotIn(LEGACY_TOKEN.upper(), combined)
        self.assertNotIn(LEGACY_TOKEN, combined.lower())

    def test_control_variants_do_not_reuse_the_product_name(self):
        catalog = (ROOT / "evals/catalog.json").read_text(encoding="utf-8")
        self.assertIn('"name": "control"', catalog)
        self.assertNotIn('"name": "' + "base" + 'line"', catalog)

    def test_storehouse_does_not_duplicate_baseline_skills(self):
        distributed = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
        self.assertEqual(set(), distributed & BASELINE_SKILLS)


if __name__ == "__main__":
    unittest.main()
