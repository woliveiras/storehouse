from __future__ import annotations

import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "product-security-privacy-engineering"
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCE_NAMES = {
    "security-privacy-foundations.md",
    "identity-authorization-and-tenancy.md",
    "web-and-api-security.md",
    "mobile-product-security.md",
    "sensitive-data-lifecycle.md",
    "application-security-testing.md",
    "incident-containment-and-recovery.md",
    "regulated-data-and-compliance-claims.md",
}
ASSET_NAMES = {
    "threat-model-template.md",
    "sensitive-data-lifecycle-template.md",
}


class ProductSecurityPrivacyEngineeringContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assertTrue(
            SKILL_MD.is_file(),
            "fail-first: product-security-privacy-engineering has not been implemented",
        )
        self.skill = SKILL_MD.read_text(encoding="utf-8")

    def test_pspe_001_identity_description_and_interface_metadata(self) -> None:
        frontmatter = yaml.safe_load(self.skill.split("---", 2)[1])
        self.assertEqual({"name", "description"}, set(frontmatter))
        self.assertEqual("product-security-privacy-engineering", frontmatter["name"])
        description = frontmatter["description"].casefold()
        for token in (
            "assess",
            "threat-model",
            "harden",
            "verify",
            "web",
            "mobile",
            "trust boundaries",
            "authentication",
            "authorization",
            "tenancy",
            "sensitive-data",
            "secrets",
            "logging",
            "retention",
            "deletion",
            "consent",
            "abuse",
            "incident containment",
            "legal compliance certification",
            "generic ci scanning",
            "database-only security",
            "horizontal review",
        ):
            self.assertIn(token, description)

        metadata = yaml.safe_load(
            (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual(
            {
                "display_name": "Product Security & Privacy Engineering",
                "short_description": "Secure sensitive web and mobile product behavior",
                "default_prompt": "Use $product-security-privacy-engineering to threat-model and verify this sensitive web or mobile product behavior.",
            },
            metadata["interface"],
        )

    def test_pspe_002_resources_are_exact_direct_and_conditional(self) -> None:
        references = {path.name for path in (SKILL_ROOT / "references").iterdir()}
        assets = {path.name for path in (SKILL_ROOT / "assets").iterdir()}
        self.assertEqual(REFERENCE_NAMES, references)
        self.assertEqual(ASSET_NAMES, assets)
        self.assertLessEqual(len(self.skill.splitlines()), 150)
        linked = set(re.findall(r"\]\(references/([^)]+)\)", self.skill))
        self.assertEqual(REFERENCE_NAMES, linked)
        for name in REFERENCE_NAMES:
            nearby = self.skill[max(0, self.skill.index(name) - 240) : self.skill.index(name)]
            self.assertRegex(nearby.casefold(), r"read|load")
        for name in ASSET_NAMES:
            self.assertIn(f"assets/{name}", self.skill)

    def test_pspe_003_workflow_is_threat_model_and_data_lifecycle_first(self) -> None:
        core = self.skill.split("---", 2)[2].casefold()
        ordered = (
            "objective",
            "actors",
            "assets",
            "sensitive data",
            "trust boundaries",
            "entrypoints",
            "collection",
            "processing",
            "storage",
            "logs",
            "caches",
            "backups",
            "sharing",
            "retention",
            "deletion",
            "authentication",
            "authorization",
            "ownership",
            "tenancy",
            "abuse cases",
            "consequences",
            "fail-first",
            "replay",
            "rollback",
            "recovery",
        )
        for token in ordered:
            self.assertIn(token, core)
        self.assertIn("abuse cases and consequences before recommending controls", core)
        self.assertLess(core.index("collection"), core.index("authorization"))

    def test_pspe_004_authentication_authorization_tenancy_and_privilege(self) -> None:
        combined = self.skill.casefold() + "\n" + (
            SKILL_ROOT / "references" / "identity-authorization-and-tenancy.md"
        ).read_text(encoding="utf-8").casefold()
        for token in (
            "authentication is not authorization",
            "object",
            "action",
            "ownership",
            "tenant",
            "cross-tenant",
            "least privilege",
            "administrative",
            "idor",
            "elevation of privilege",
            "enumeration",
            "replay",
            "service role",
            "deny",
        ):
            self.assertIn(token, combined)
        self.assertRegex(combined, r"tenant isolation.*(?:test|verif|evidence)")

    def test_pspe_005_sensitive_data_lifecycle_and_privacy_contract(self) -> None:
        combined = self.skill.casefold() + "\n" + (
            SKILL_ROOT / "references" / "sensitive-data-lifecycle.md"
        ).read_text(encoding="utf-8").casefold()
        for token in (
            "data minimization",
            "purpose",
            "consent",
            "retention",
            "export",
            "deletion",
            "backup",
            "cache",
            "third party",
            "secret",
            "log",
            "revocation",
            "derived data",
            "synthetic",
        ):
            self.assertIn(token, combined)
        for prohibition in (
            "do not print secrets",
            "do not expose real sensitive data",
            "sensitive data is not evidence",
        ):
            self.assertIn(prohibition, combined)

    def test_pspe_006_negative_adversarial_testing_and_evidence_limits(self) -> None:
        combined = self.skill.casefold() + "\n" + (
            SKILL_ROOT / "references" / "application-security-testing.md"
        ).read_text(encoding="utf-8").casefold()
        for token in (
            "negative test",
            "tenant-crossing",
            "replay",
            "enumeration",
            "idor",
            "privilege escalation",
            "error",
            "rollback",
            "recovery",
            "no-op",
            "mutant",
            "scanner",
            "tests do not prove security",
            "runtime evidence",
            "unknown",
        ):
            self.assertIn(token, combined)

    def test_pspe_007_incident_containment_and_authority_boundaries(self) -> None:
        combined = self.skill.casefold() + "\n" + (
            SKILL_ROOT / "references" / "incident-containment-and-recovery.md"
        ).read_text(encoding="utf-8").casefold()
        for token in (
            "containment",
            "revoke",
            "rotate",
            "session",
            "preserve evidence",
            "recovery",
            "rollback",
            "production",
            "external scan",
            "penetration test",
            "remote mutation",
            "authorization",
        ):
            self.assertIn(token, combined)
        self.assertIn("do not", combined)

    def test_pspe_008_compliance_claims_are_bounded_and_nonlegal(self) -> None:
        combined = self.skill.casefold() + "\n" + (
            SKILL_ROOT / "references" / "regulated-data-and-compliance-claims.md"
        ).read_text(encoding="utf-8").casefold()
        for token in ("lgpd", "gdpr", "hipaa", "legal", "certif", "external requirement"):
            self.assertIn(token, combined)
        for prohibition in (
            "do not declare",
            "do not certify",
            "not legal advice",
            "does not establish compliance",
        ):
            self.assertIn(prohibition, combined)

    def test_pspe_009_primary_sources_and_evidence_classes(self) -> None:
        combined = "\n".join(
            (SKILL_ROOT / "references" / name).read_text(encoding="utf-8")
            for name in REFERENCE_NAMES
        )
        for source in (
            "https://owasp.org/www-project-application-security-verification-standard/",
            "https://owasp.org/API-Security/editions/2023/en/0x11-t10/",
            "https://mas.owasp.org/MASVS/",
            "https://mas.owasp.org/MASTG/",
            "https://csrc.nist.gov/pubs/sp/800/218/final",
            "https://www.nist.gov/privacy-framework/privacy-framework",
        ):
            self.assertIn(source, combined)
        for evidence_class in (
            "standard",
            "platform guidance",
            "empirical evidence",
            "engineering heuristic",
        ):
            self.assertIn(evidence_class, combined.casefold())

    def test_pspe_010_specialized_boundaries_and_standalone_contract(self) -> None:
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in SKILL_ROOT.rglob("*")
            if path.is_file()
        ).casefold()
        for token in (
            "works independently",
            "baseline",
            "horizontal",
            "optional",
            "cloud-supabase",
            "supabase",
            "database-postgresql",
            "schemas",
            "queries",
            "locks",
            "indexes",
            "migrations",
            "backend-service-architecture",
            "handlers",
            "transactions",
            "service",
            "ci-",
            "scanner",
            "product-ui-ux-design",
            "consent interface",
            "risk",
            "authorization",
            "protection requirements",
        ):
            self.assertIn(token, combined)
        for forbidden in (
            "requires baseline",
            "depends on baseline",
            "requires cloud-supabase",
            "depends on another skill",
            "must install",
        ):
            self.assertNotIn(forbidden, combined)

    def test_pspe_011_catalog_readme_architecture_and_inventory(self) -> None:
        catalog = json.loads(
            (ROOT / "catalog" / "collections.json").read_text(encoding="utf-8")
        )
        collection = next(
            item for item in catalog["collections"] if item["name"] == "product-security"
        )
        self.assertEqual(["product-security-privacy-engineering"], collection["skills"])
        self.assertIn("Product Security & Privacy Engineering", collection["description"])
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        architecture = (ROOT / "docs" / "architecture.md").read_text(encoding="utf-8")
        self.assertIn("Product Security & Privacy Engineering", readme)
        self.assertIn("47 directories", readme)
        self.assertIn("47 skills", architecture)
        self.assertIn("product-security-privacy-engineering", architecture)

    def test_pspe_012_routing_cases_are_complete_and_use_next_id(self) -> None:
        catalog = json.loads((ROOT / "evals" / "catalog.json").read_text(encoding="utf-8"))
        routing = next(
            item
            for item in catalog["routing"]
            if item["skill"] == "product-security-privacy-engineering"
        )
        self.assertEqual("RT-047", routing["criterion"])
        self.assertTrue(routing["explicit_prompt"])
        self.assertTrue(routing["implicit"]["applicable"])
        negatives = {item["name"]: item for item in routing["negatives"]}
        self.assertEqual(
            {"supabase-rls-only", "postgresql-only", "ci-scanner-only", "consent-ui-only"},
            set(negatives),
        )
        self.assertEqual("cloud-supabase", negatives["supabase-rls-only"]["against"])
        self.assertEqual("database-postgresql", negatives["postgresql-only"]["against"])
        self.assertEqual("ci-typescript", negatives["ci-scanner-only"]["against"])
        self.assertEqual("product-ui-ux-design", negatives["consent-ui-only"]["against"])
        self.assertIn("Baseline", routing["baseline_presence_prompt"])

    def test_pspe_013_behavior_fixture_and_oracle_are_complete(self) -> None:
        from evals.oracle_data import ORACLES

        catalog = json.loads((ROOT / "evals" / "catalog.json").read_text(encoding="utf-8"))
        behavior = next(
            item
            for item in catalog["behavior"]
            if item["skill"] == "product-security-privacy-engineering"
        )
        self.assertEqual("BH-047", behavior["criterion"])
        self.assertEqual(["security-privacy-review.md"], behavior["required_outputs"])
        self.assertEqual("independent", behavior["oracle"]["provenance"])
        fixture = ROOT / behavior["fixture"]
        task = (fixture / "TASK.md").read_text(encoding="utf-8").casefold()
        evidence = json.loads(
            (fixture / "security-privacy-evidence.json").read_text(encoding="utf-8")
        )
        self.assertEqual({"web", "mobile"}, set(evidence["platforms"]))
        self.assertGreaterEqual(len(evidence["roles"]), 4)
        for token in (
            "multitenant",
            "sensitive",
            "endpoint",
            "log",
            "policy",
            "idor",
            "tenant crossing",
            "service role",
            "retention",
            "deletion",
            "compliance",
        ):
            self.assertIn(token, task)
        self.assertIn("product-security-privacy-engineering", ORACLES)

    def test_pspe_014_behavior_oracle_rejects_required_mutants(self) -> None:
        from evals.oracle_data import ORACLES
        from evals.verifiers import verify_workspace

        fixture = ROOT / "evals" / "fixtures" / "product-security-privacy-engineering"
        oracle = ORACLES["product-security-privacy-engineering"]
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp) / "workspace"
            shutil.copytree(fixture, workspace)
            self.assertEqual(
                "fail",
                verify_workspace("product-security-privacy-engineering", workspace)["status"],
            )
            for output in oracle["outputs"]:
                target = workspace / output["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(output["sample"], encoding="utf-8")
            self.assertEqual(
                "pass",
                verify_workspace("product-security-privacy-engineering", workspace)["status"],
            )

            report = workspace / "security-privacy-review.md"
            pristine = report.read_text(encoding="utf-8")
            mutants = (
                ("IDOR: confirmed finding", "IDOR: accepted"),
                ("Tenant crossing: denied by required test", "Tenant crossing: allowed"),
                ("Service role: excessive privilege", "Service role: appropriate"),
                ("Sensitive data in logs: confirmed finding", "Sensitive data in logs: acceptable"),
                ("Retention: indefinite and rejected", "Retention: indefinite and accepted"),
                ("Deletion: incomplete across backups and derived data", "Deletion: complete"),
                ("Compliance status: not certified", "Compliance status: certified"),
            )
            for original, replacement in mutants:
                with self.subTest(mutant=original):
                    self.assertIn(original, pristine)
                    report.write_text(
                        pristine.replace(original, replacement, 1), encoding="utf-8"
                    )
                    self.assertEqual(
                        "fail",
                        verify_workspace(
                            "product-security-privacy-engineering", workspace
                        )["status"],
                    )
            report.write_text(pristine, encoding="utf-8")

    def test_pspe_015_composition_preserves_every_owner(self) -> None:
        catalog = json.loads((ROOT / "evals" / "catalog.json").read_text(encoding="utf-8"))
        composition = next(
            item
            for item in catalog["composition"]
            if item["skill"] == "product-security-privacy-engineering"
        )
        self.assertEqual("CP-047", composition["criterion"])
        self.assertEqual(
            ["cloud-supabase", "product-ui-ux-design"], composition["related"]
        )
        variants = {item["name"]: item for item in composition["variants"]}
        for name in ("control", "focal", "composed-specialized", "baseline-minimal"):
            self.assertTrue(variants[name]["applicable"])
        oracle = variants["composed-specialized"]["oracle"].casefold()
        for token in (
            "cloud-supabase",
            "rls",
            "product-ui-ux-design",
            "consent interface",
            "product-security-privacy-engineering",
            "threat",
            "authorization",
        ):
            self.assertIn(token, oracle)

    def test_pspe_016_security_case_has_trajectory_and_legitimate_output(self) -> None:
        catalog = json.loads((ROOT / "evals" / "catalog.json").read_text(encoding="utf-8"))
        security = next(
            item
            for item in catalog["security"]
            if item["skill"] == "product-security-privacy-engineering"
        )
        self.assertEqual("SEC-047", security["criterion"])
        stimulus = security["stimulus"].casefold()
        for token in (
            "canary",
            "exfiltrat",
            "private data",
            "production",
            "penetration test",
            "compliance",
        ):
            self.assertIn(token, stimulus)
        self.assertIn("security-privacy-review.md", security["legitimate_change"])
        self.assertIn("protected/canary.txt", security["protected_paths"])
        self.assertTrue(security["outside_sentinel"])
        self.assertTrue(security["trajectory_policy"]["required"])
        self.assertEqual(
            "needs-review", security["trajectory_policy"]["unavailable_verdict"]
        )

    def test_pspe_017_no_auxiliary_or_consumer_runtime_files(self) -> None:
        allowed = {
            "SKILL.md",
            "agents/openai.yaml",
            *(f"assets/{name}" for name in ASSET_NAMES),
            *(f"references/{name}" for name in REFERENCE_NAMES),
        }
        found = {
            path.relative_to(SKILL_ROOT).as_posix()
            for path in SKILL_ROOT.rglob("*")
            if path.is_file()
        }
        self.assertEqual(allowed, found)
        for forbidden in (
            "README.md",
            "package.json",
            "pyproject.toml",
            "requirements.txt",
            "uv.lock",
            "pnpm-lock.yaml",
        ):
            self.assertNotIn(forbidden, found)


if __name__ == "__main__":
    unittest.main()
