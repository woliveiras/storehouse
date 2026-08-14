from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "backend-service-architecture"


class BackendServiceArchitectureTests(unittest.TestCase):
    def test_bsa_001_core_routes_framework_detail_progressively(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for token in (
            "NestJS",
            "FastAPI",
            "Fiber",
            "references/nestjs.md",
            "references/fastapi.md",
            "references/fiber.md",
            "Next.js",
            "BFF",
        ):
            self.assertIn(token, skill)

    def test_bsa_002_framework_references_preserve_common_boundaries(self) -> None:
        expectations = {
            "nestjs.md": ("modules", "providers", "controllers", "guards", "interceptors"),
            "fastapi.md": ("APIRouter", "Depends", "Pydantic", "lifespan", "async"),
            "fiber.md": ("fiber.Ctx", "middleware", "interfaces", "context.Context", "error handler"),
        }
        for filename, tokens in expectations.items():
            content = (SKILL / "references" / filename).read_text(encoding="utf-8")
            for token in tokens:
                self.assertIn(token, content, filename)

    def test_bsa_003_eval_contract_is_complete(self) -> None:
        catalog = json.loads((ROOT / "evals" / "catalog.json").read_text(encoding="utf-8"))
        expected = {
            "routing": "RT-045",
            "behavior": "BH-045",
            "composition": "CP-045",
            "security": "SEC-045",
        }
        for section, criterion in expected.items():
            item = next(
                entry
                for entry in catalog[section]
                if entry["skill"] == "backend-service-architecture"
            )
            self.assertEqual(criterion, item["criterion"])


if __name__ == "__main__":
    unittest.main()
