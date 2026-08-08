from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path


@unittest.skipUnless(os.environ.get("AGENT_SKILLS_RUN_EXTERNAL") == "1", "enabled by validate:sources")
class ExternalSourceContractTests(unittest.TestCase):
    def test_as_015_clean_room_official_cli_installation(self) -> None:
        from maintenance.validate_installation import main

        self.assertEqual(0, main())

    def test_as_016_real_official_validator_accepts_all_skills(self) -> None:
        from maintenance.official_validate import main

        self.assertEqual(0, main())

    def test_as_002_source_drift_is_rejected(self) -> None:
        from maintenance.validate import _catalog_check

        source = Path(os.environ["AGENT_SKILLS_GEREMMYAS_SOURCE"]) / "content" / "skills"
        with tempfile.TemporaryDirectory() as raw:
            synthetic = Path(raw) / "geremmyas"
            target = synthetic / "content" / "skills"
            target.parent.mkdir(parents=True)
            import shutil

            shutil.copytree(source, target)
            skill = target / "android-ci-setup" / "SKILL.md"
            skill.write_text(skill.read_text(encoding="utf-8") + "\nsource drift\n", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                _catalog_check(synthetic)


if __name__ == "__main__":
    unittest.main()
