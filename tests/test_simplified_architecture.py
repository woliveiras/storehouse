from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SimplifiedArchitectureTests(unittest.TestCase):
    def test_eval_catalog_covers_every_distributed_skill(self) -> None:
        skills = {
            path.name
            for path in (ROOT / "skills").iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        }
        catalog = json.loads((ROOT / "evals" / "catalog.json").read_text(encoding="utf-8"))

        for section in ("routing", "behavior", "composition"):
            self.assertEqual(skills, {item["skill"] for item in catalog[section]}, section)
        self.assertTrue({item["skill"] for item in catalog["security"]} <= skills)


if __name__ == "__main__":
    unittest.main()
