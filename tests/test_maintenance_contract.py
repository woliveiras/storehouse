from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


class MaintenanceContractTests(unittest.TestCase):
    def test_as_006_script_smokes_execute_all_owned_scripts(self) -> None:
        from maintenance import validate

        validate._script_smokes()

    def test_as_015_clean_room_plan_is_project_scoped_and_credential_free(self) -> None:
        from maintenance.validate_installation import clean_environment, installation_commands

        with mock.patch.dict(os.environ, {"CODEX_HOME": "/personal", "OPENAI_API_KEY": "secret", "CODEX_API_KEY": "secret"}, clear=False):
            env = clean_environment(Path("/tmp/synthetic-storehouse-home"))
        self.assertEqual("1", env["DISABLE_TELEMETRY"])
        self.assertEqual("1", env["DO_NOT_TRACK"])
        self.assertNotIn("CODEX_HOME", env)
        self.assertNotIn("OPENAI_API_KEY", env)
        self.assertNotIn("CODEX_API_KEY", env)
        commands = installation_commands(["gameplay-programming-2d", "game-testing-2d"])
        self.assertIn("--list", commands["list"])
        self.assertIn("--copy", commands["single"])
        self.assertNotIn("--global", commands["single"])
        self.assertEqual(2, commands["collection"].count("--skill"))
        self.assertIn("github-copilot", commands["collection"])

    def test_as_016_official_validator_invokes_exactly_34_skills(self) -> None:
        from maintenance import official_validate
        from maintenance.catalog_data import SKILLS

        completed = mock.Mock(returncode=0, stdout="Valid skill", stderr="")
        with mock.patch.object(official_validate.shutil, "which", return_value="/validator"), mock.patch.object(official_validate.subprocess, "run", return_value=completed) as run:
            self.assertEqual(0, official_validate.main())
        self.assertEqual(34, run.call_count)
        self.assertEqual(set(SKILLS), {Path(call.args[0][-1]).name for call in run.call_args_list})
        self.assertTrue(all(call.args[0][:2] == ["/validator", "validate"] for call in run.call_args_list))

    def test_as_017_single_validation_command_routes_every_gate(self) -> None:
        from maintenance import validate

        argv = ["maintenance.validate"]
        with mock.patch.object(sys, "argv", argv), mock.patch.object(validate, "_run") as run, mock.patch.object(validate, "_syntax_checks") as syntax, mock.patch.object(validate, "_script_smokes") as scripts, mock.patch.object(validate, "_schema_checks") as schemas, mock.patch.object(validate, "official_validate") as official:
            self.assertEqual(0, validate.main())
        run.assert_called_once()
        self.assertIn("unittest", run.call_args.args[0])
        syntax.assert_called_once_with()
        scripts.assert_called_once_with()
        schemas.assert_called_once_with()
        official.assert_called_once_with()

if __name__ == "__main__":
    unittest.main()
