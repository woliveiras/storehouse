from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tomllib
import unittest
from pathlib import Path
from urllib.parse import unquote

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
GEREMMYAS_COMMIT = "783ac878213b61acb914b9151c779c6de0b84286"
TUXEDO_COMMIT = "168922a54b695fd2446295c58157981079d2d5d6"
GEREMMYAS_TREE_DIGEST = "7de30d71108e8c4e73641a70aaa2d9541ce97f6b826cca528f6eeed0bb73e20d"
TUXEDO_TREE_DIGEST = "3ed55c2bcd4614cd7074a6ff4ff01199a81b4dd9f31d9912fa25f191c85a967f"
GEREMMYAS_LICENSE_DIGEST = "24923e703cfafa4e2c5098f4d5b0442ab43f9405dbdbb9fd961707c32e5e4702"

MIGRATED = {
    "android-ci-setup",
    "chromadb-rag-workflow",
    "game-ai-2d",
    "game-art-2d",
    "game-audio-2d",
    "game-build-and-release",
    "game-feel-2d",
    "game-performance-2d",
    "game-save-n-progress",
    "game-testing-2d",
    "game-ui-accessibility",
    "gameplay-programming-2d",
    "gcloud-operation",
    "go-ci-setup",
    "langgraph-agent-design",
    "llm-integration-review",
    "manage-state-with-zustand",
    "migrate-react-router",
    "model-state-with-xstate",
    "paper-review",
    "postgres-query-review",
    "procedural-generation-2d",
    "python-ci-setup",
    "rust-ci-setup",
    "rust-release",
    "scientific-case-study-research",
    "scientific-paper",
    "skill-authoring",
    "supabase-workflow",
    "terraform-change",
    "text-review",
    "typescript-ci-setup",
    "validate-with-zod",
}

EXCLUDED = {
    "brainstorming",
    "bugfix",
    "ci-workflow",
    "decision-framework",
    "design-deep-modules",
    "docs",
    "git-commit",
    "improve-architecture",
    "premortem",
    "refine",
    "session-bridge",
    "shape-domain",
    "spec",
    "tdd",
    "technical-research",
    "verify",
}

OWNED = {"spec"}
SKILLS = MIGRATED | OWNED

COLLECTIONS = {
    "game-core",
    "game-ui",
    "game-systems",
    "game-performance",
    "game-audio",
    "game-art",
    "game-delivery",
    "game-dev",
    "android",
    "go",
    "python",
    "rust",
    "typescript",
    "web",
    "data",
    "infrastructure",
    "ai",
    "scientific-research",
    "writing",
    "skill-maintenance",
    "sdd",
}

SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
RESOURCE_REFERENCE = re.compile(r"(?<![A-Za-z0-9_.-])((?:references|scripts|assets)/[A-Za-z0-9_./-]+)")
FORBIDDEN_FILENAMES = {
    ".DS_Store",
    "Thumbs.db",
    "package.json",
    "pnpm-lock.yaml",
    "pyproject.toml",
    "uv.lock",
}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo", ".log"}


def read_frontmatter(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        raise AssertionError(f"missing YAML frontmatter: {path.relative_to(ROOT)}")
    parsed = yaml.safe_load(match.group(1))
    if not isinstance(parsed, dict):
        raise AssertionError(f"frontmatter is not a mapping: {path.relative_to(ROOT)}")
    return parsed, text[match.end() :]


def expand_collections(catalog: dict[str, object]) -> dict[str, list[str]]:
    items = catalog["collections"]
    assert isinstance(items, list)
    by_name = {item["name"]: item for item in items}
    expanded: dict[str, list[str]] = {}

    def visit(name: str, stack: tuple[str, ...] = ()) -> list[str]:
        if name in expanded:
            return expanded[name]
        if name in stack:
            raise AssertionError(f"collection cycle: {' -> '.join((*stack, name))}")
        item = by_name[name]
        result: list[str] = list(item.get("skills", []))
        for included in item.get("includes", []):
            result.extend(visit(included, (*stack, name)))
        if len(result) != len(set(result)):
            raise AssertionError(f"duplicate expanded skill in collection {name}")
        expanded[name] = result
        return result

    for collection_name in by_name:
        visit(collection_name)
    return expanded


class RepositoryContractTests(unittest.TestCase):
    def test_as_027_public_project_identity_is_canonical(self) -> None:
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        collections_schema = json.loads(
            (ROOT / "catalog" / "collections.schema.json").read_text(encoding="utf-8")
        )
        skills_schema = json.loads(
            (ROOT / "catalog" / "skills.schema.json").read_text(encoding="utf-8")
        )
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertEqual("storehouse", package["name"])
        self.assertEqual("storehouse", pyproject["project"]["name"])
        self.assertIn("Storehouse", package["description"])
        self.assertIn("Storehouse", pyproject["project"]["description"])
        self.assertEqual(
            "https://github.com/woliveiras/storehouse/catalog/collections.schema.json",
            collections_schema["$id"],
        )
        self.assertEqual(
            "https://github.com/woliveiras/storehouse/catalog/skills.schema.json",
            skills_schema["$id"],
        )
        self.assertTrue(readme.startswith("# Storehouse\n"))
        self.assertIn("## Storehouse and Tuxedo", readme)
        self.assertTrue((ROOT / "docs" / "development-dependencies.md").is_file())
        self.assertFalse((ROOT / "docs" / "maintainer-dependencies.md").exists())

    def test_sh_002_through_005_storehouse_identity_is_canonical(self) -> None:
        legacy_name = "agent" + "-skills"
        legacy_env = "AGENT" + "_SKILLS_"
        failures: list[str] = []
        tracked = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout.split(b"\0")
        for raw_path in tracked:
            if not raw_path:
                continue
            path = ROOT / raw_path.decode("utf-8")
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for forbidden in (legacy_name, legacy_env):
                if forbidden in text:
                    failures.append(f"{path.relative_to(ROOT)} contains {forbidden}")
        self.assertEqual([], failures)

    def test_as_027_dependency_versions_have_single_source(self) -> None:
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        dependencies = set(package["devDependencies"])
        for requirement in pyproject["dependency-groups"]["dev"]:
            name, _version = requirement.split("==", 1)
            dependencies.add(name)

        documentation = [ROOT / "README.md", ROOT / "AGENTS.md"]
        documentation.extend(sorted((ROOT / "docs").rglob("*.md")))
        documentation.extend(sorted((ROOT / "specs").rglob("*.md")))
        version_pattern = re.compile(r"(?<![-A-Za-z])v?\d+\.\d+(?:\.\d+)?\b")
        violations: list[str] = []
        for path in documentation:
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                lowered = line.lower()
                for name in dependencies:
                    offset = lowered.find(name.lower())
                    while offset >= 0:
                        context = line[offset : offset + len(name) + 40]
                        if version_pattern.search(context):
                            violations.append(
                                f"{path.relative_to(ROOT)}:{line_number}: {context.strip()}"
                            )
                        offset = lowered.find(name.lower(), offset + len(name))
        self.assertEqual([], violations)

    def test_as_001_exact_inventory_equation(self) -> None:
        self.assertEqual(33, len(MIGRATED))
        self.assertEqual(16, len(EXCLUDED))
        self.assertFalse(MIGRATED & EXCLUDED)
        self.assertEqual(49, len(MIGRATED | EXCLUDED))

    def test_as_002_optional_live_source_baseline(self) -> None:
        geremmyas = os.environ.get("STOREHOUSE_GEREMMYAS_SOURCE")
        tuxedo = os.environ.get("STOREHOUSE_TUXEDO_SOURCE")
        if not geremmyas or not tuxedo:
            self.skipTest("set both source environment variables for live read-only reconciliation")

        def git(repo: str, *args: str) -> bytes:
            return subprocess.run(
                ["git", "-C", repo, *args], check=True, capture_output=True
            ).stdout

        self.assertEqual(GEREMMYAS_COMMIT, git(geremmyas, "rev-parse", "HEAD").decode().strip())
        self.assertEqual(b"", git(geremmyas, "status", "--porcelain=v1", "--untracked-files=all"))
        ger_tree = git(geremmyas, "ls-tree", "-r", "--full-tree", "HEAD", "content/skills")
        self.assertEqual(GEREMMYAS_TREE_DIGEST, hashlib.sha256(ger_tree).hexdigest())
        frozen_tux_tree = git(tuxedo, "ls-tree", "-r", "--full-tree", TUXEDO_COMMIT, "plugins/tuxedo/skills")
        self.assertEqual(TUXEDO_TREE_DIGEST, hashlib.sha256(frozen_tux_tree).hexdigest())
        license_text = git(geremmyas, "show", f"{GEREMMYAS_COMMIT}:LICENSE")
        self.assertEqual(GEREMMYAS_LICENSE_DIGEST, hashlib.sha256(license_text).hexdigest())
        self.assertIn(b"MIT License", license_text)

        source_names = {
            path.name
            for path in (Path(geremmyas) / "content" / "skills").iterdir()
            if path.is_dir()
        }
        self.assertEqual(MIGRATED | EXCLUDED, source_names)
        catalog = json.loads((ROOT / "catalog" / "skills.json").read_text(encoding="utf-8"))
        by_name = {item["name"]: item for item in catalog["skills"]}
        for name in MIGRATED:
            source_root = Path(geremmyas) / "content" / "skills" / name
            source_files = {
                path.relative_to(source_root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in source_root.rglob("*") if path.is_file()
            }
            dispositions = {item["path"]: item for item in by_name[name]["files"]}
            self.assertEqual(source_files, {path: item["source_sha256"] for path, item in dispositions.items()})
            for relative, item in dispositions.items():
                destination = SKILLS_ROOT / name / relative
                self.assertTrue(destination.is_file())
                self.assertEqual(hashlib.sha256(destination.read_bytes()).hexdigest(), item["destination_sha256"])
                if item["disposition"] == "preserved":
                    self.assertEqual(item["source_sha256"], item["destination_sha256"])
                else:
                    self.assertEqual("adapted", item["disposition"])
                    self.assertNotEqual(item["source_sha256"], item["destination_sha256"])
                    self.assertTrue(item.get("note"))

    def test_as_003_exact_destination_inventory(self) -> None:
        found = {path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()}
        self.assertEqual(SKILLS, found)
        self.assertFalse((EXCLUDED - OWNED) & found)
        self.assertEqual(34, len(list(SKILLS_ROOT.rglob("SKILL.md"))))

    def test_as_005_skill_frontmatter_and_routing(self) -> None:
        names: list[str] = []
        for skill in sorted(SKILLS):
            metadata, body = read_frontmatter(SKILLS_ROOT / skill / "SKILL.md")
            self.assertEqual({"name", "description"}, set(metadata), skill)
            self.assertEqual(skill, metadata["name"])
            self.assertRegex(skill, SKILL_NAME)
            description = metadata["description"]
            self.assertIsInstance(description, str)
            assert isinstance(description, str)
            self.assertLessEqual(len(description), 1024)
            self.assertRegex(description, r"(?i)\buse when\b", skill)
            self.assertRegex(description, r"(?i)\bdo not use\b", skill)
            self.assertTrue(body.strip(), skill)
            names.append(skill)
        self.assertEqual(len(names), len(set(names)))

    def test_as_006_relative_links_resolve(self) -> None:
        failures: list[str] = []
        for markdown in SKILLS_ROOT.rglob("*.md"):
            text = markdown.read_text(encoding="utf-8")
            for raw in LINK.findall(text):
                target = raw.split("#", 1)[0].strip().strip("<>")
                if not target or re.match(r"^(?:https?|mailto):", target):
                    continue
                resolved = (markdown.parent / unquote(target)).resolve()
                try:
                    resolved.relative_to(markdown.parents[len(markdown.relative_to(SKILLS_ROOT).parts) - 1])
                except (ValueError, IndexError):
                    failures.append(f"escaping link {markdown.relative_to(ROOT)} -> {target}")
                    continue
                if not resolved.exists():
                    failures.append(f"missing link {markdown.relative_to(ROOT)} -> {target}")
        self.assertEqual([], failures)

    def test_as_006_explicit_owned_resources_resolve_and_yaml_is_valid(self) -> None:
        failures: list[str] = []
        for markdown in SKILLS_ROOT.rglob("*.md"):
            text = markdown.read_text(encoding="utf-8")
            for raw in RESOURCE_REFERENCE.findall(text):
                target = raw.rstrip(".,:;)")
                if not (markdown.parent / target).exists():
                    failures.append(f"missing resource {markdown.relative_to(ROOT)} -> {target}")
        for yaml_path in list(SKILLS_ROOT.rglob("*.yaml")) + list(SKILLS_ROOT.rglob("*.yml")):
            try:
                parsed = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
            except yaml.YAMLError as exc:
                failures.append(f"invalid YAML {yaml_path.relative_to(ROOT)}: {exc}")
                continue
            if not isinstance(parsed, dict):
                failures.append(f"YAML is not a mapping: {yaml_path.relative_to(ROOT)}")
        self.assertEqual([], failures)

    def test_as_007_no_accidental_distribution_dependencies(self) -> None:
        forbidden = {
            "GEREMMYAS_TARGET": "Geremmyas command marker",
            "geremmyas.yml": "Geremmyas manifest",
            ".geremmyas/": "Geremmyas state",
            "content/skills/": "Geremmyas source path",
            "catalog/packs.json": "Geremmyas pack catalog",
            "/Users/": "personal absolute path",
        }
        failures: list[str] = []
        for path in SKILLS_ROOT.rglob("*"):
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for needle, reason in forbidden.items():
                if needle.casefold() in text.casefold():
                    failures.append(f"{path.relative_to(ROOT)}: {reason}")
        self.assertEqual([], failures)

        script_metadata = "\n".join(path.read_text(encoding="utf-8") for path in SKILLS_ROOT.rglob("*.py"))
        self.assertNotIn("Pillow>=", script_metadata)
        self.assertIn("Pillow==12.0.0", script_metadata)
        rust_guidance = (SKILLS_ROOT / "rust-ci-setup/SKILL.md").read_text(encoding="utf-8") + (SKILLS_ROOT / "rust-release/SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("rust-toolchain@stable", rust_guidance)
        self.assertNotIn("cargo +nightly miri", rust_guidance)
        migrated_pattern = "|".join(re.escape(name) for name in sorted(MIGRATED, key=len, reverse=True))
        for skill in MIGRATED:
            text = (SKILLS_ROOT / skill / "SKILL.md").read_text(encoding="utf-8")
            for match in re.finditer(rf"\$(?:{migrated_pattern})", text):
                nearby = text[max(0, match.start() - 180):match.start()].casefold()
                self.assertTrue("if installed" in nearby or "optional" in nearby, f"mandatory companion reference in {skill}")
        art = (SKILLS_ROOT / "game-art-2d" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("optional helpers", art)
        self.assertIn("skill itself does not", art)
        self.assertIn("fallback", art.casefold())

    def test_as_008_game_scope(self) -> None:
        game_names = {name for name in MIGRATED if name.startswith("game-") or name in {"gameplay-programming-2d", "procedural-generation-2d"}}
        for name in game_names:
            text = (SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("2D", text, name)
            self.assertRegex(text, r"Phaser|Godot", name)
            self.assertNotRegex(text, r"(?i)\bUnity\b|\bPixiJS\b", name)
            whole_tree = "\n".join(
                path.read_text(encoding="utf-8", errors="replace")
                for path in (SKILLS_ROOT / name).rglob("*") if path.is_file()
            )
            self.assertNotRegex(whole_tree, r"(?i)\bUnity\b|\bPixiJS\b", name)
        for name in game_names:
            for path in (SKILLS_ROOT / name).rglob("*"):
                if not path.is_file():
                    continue
                try:
                    lines = path.read_text(encoding="utf-8").splitlines()
                except UnicodeDecodeError:
                    continue
                for line in (line for line in lines if re.search(r"(?i)\b3D\b", line)):
                    self.assertRegex(line, r"(?i)do not use|route .* elsewhere", f"unbounded 3D scope in {path.relative_to(ROOT)}")

    def test_as_009_provenance_inventory_is_complete(self) -> None:
        catalog = json.loads((ROOT / "catalog" / "skills.json").read_text(encoding="utf-8"))
        self.assertEqual(2, catalog["schema_version"])
        self.assertEqual(GEREMMYAS_COMMIT, catalog["source"]["commit"])
        self.assertEqual(GEREMMYAS_LICENSE_DIGEST, catalog["source"]["license_sha256"])
        entries = catalog["skills"]
        self.assertEqual(SKILLS, {item["name"] for item in entries})
        migrated_entries = [item for item in entries if item["ownership"] == "migrated"]
        owned_entries = [item for item in entries if item["ownership"] == "storehouse"]
        self.assertEqual(MIGRATED, {item["name"] for item in migrated_entries})
        self.assertEqual(OWNED, {item["name"] for item in owned_entries})
        self.assertEqual(106, sum(len(item["files"]) for item in migrated_entries))
        disposition_counts = {kind: 0 for kind in ("preserved", "adapted", "excluded")}
        for item in migrated_entries:
            self.assertEqual(f"content/skills/{item['name']}", item["source_path"])
            self.assertRegex(item["source_tree_sha256"], r"^[0-9a-f]{64}$")
            self.assertTrue(item["categories"])
            self.assertIn(item["security"]["sensitive"], {True, False})
            self.assertTrue(item["compatibility"]["standalone"])
            self.assertTrue(item["files"])
            for file_item in item["files"]:
                self.assertIn(file_item["disposition"], {"preserved", "adapted", "excluded"})
                disposition_counts[file_item["disposition"]] += 1
                self.assertRegex(file_item["source_sha256"], r"^[0-9a-f]{64}$")
                if file_item["disposition"] != "excluded":
                    destination = SKILLS_ROOT / item["name"] / file_item["path"]
                    self.assertTrue(destination.is_file())
                    self.assertEqual(hashlib.sha256(destination.read_bytes()).hexdigest(), file_item["destination_sha256"])
                if file_item["disposition"] == "preserved":
                    self.assertEqual(file_item["source_sha256"], file_item["destination_sha256"])
                elif file_item["disposition"] == "adapted":
                    self.assertNotEqual(file_item["source_sha256"], file_item["destination_sha256"])
                    self.assertTrue(file_item.get("note"))
        self.assertEqual({"preserved": 77, "adapted": 29, "excluded": 0}, disposition_counts)
        for item in owned_entries:
            self.assertRegex(item["source_tree_sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual("woliveiras/tuxedo", item["origin"]["repository"])
            self.assertTrue(item["compatibility"]["standalone"])
            self.assertTrue(item["files"])
            for file_item in item["files"]:
                self.assertEqual("owned", file_item["disposition"])
                destination = SKILLS_ROOT / item["name"] / file_item["path"]
                self.assertEqual(hashlib.sha256(destination.read_bytes()).hexdigest(), file_item["destination_sha256"])

    def test_as_010_011_012_collections(self) -> None:
        catalog = json.loads((ROOT / "catalog" / "collections.json").read_text(encoding="utf-8"))
        self.assertEqual(1, catalog["schema_version"])
        items = catalog["collections"]
        names = [item["name"] for item in items]
        self.assertEqual(COLLECTIONS, set(names))
        self.assertEqual(len(names), len(set(names)))
        for item in items:
            self.assertEqual(set(item) - {"name", "description", "skills", "includes"}, set())
            self.assertTrue(item["description"])
            self.assertEqual(len(item.get("skills", [])), len(set(item.get("skills", []))))
            self.assertTrue(set(item.get("skills", [])) <= SKILLS)
            self.assertTrue(set(item.get("includes", [])) <= COLLECTIONS)
        expanded = expand_collections(catalog)
        self.assertEqual(SKILLS, set().union(*(set(value) for value in expanded.values())))
        self.assertEqual(
            [
                "gameplay-programming-2d",
                "game-testing-2d",
                "game-ui-accessibility",
                "game-feel-2d",
                "game-ai-2d",
                "procedural-generation-2d",
                "game-save-n-progress",
                "game-performance-2d",
                "game-audio-2d",
                "game-art-2d",
                "game-build-and-release",
            ],
            expanded["game-dev"],
        )

    def test_as_011_invalid_collection_graphs_fail(self) -> None:
        with self.assertRaises(AssertionError):
            expand_collections({"collections": [
                {"name": "a", "skills": ["game-ai-2d"], "includes": ["b"]},
                {"name": "b", "includes": ["a"]},
            ]})
        with self.assertRaises(AssertionError):
            expand_collections({"collections": [
                {"name": "a", "skills": ["game-ai-2d"], "includes": ["b"]},
                {"name": "b", "skills": ["game-ai-2d"]},
            ]})
        with self.assertRaises(KeyError):
            expand_collections({"collections": [{"name": "a", "includes": ["missing"]}]})

    def test_as_013_014_readme_commands_match_catalog(self) -> None:
        from maintenance.catalog import render_install_commands

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("<!-- collections:start -->", readme)
        self.assertIn("<!-- collections:end -->", readme)
        actual = readme.split("<!-- collections:start -->", 1)[1].split("<!-- collections:end -->", 1)[0].strip()
        expected = render_install_commands().strip()
        self.assertEqual(expected, actual)
        for phrase in (
            "Tuxedo",
            "project",
            "independent",
            "collection",
            "npx skills add woliveiras/storehouse --list",
            "npx skills update",
            "npx skills remove",
            "DISABLE_TELEMETRY=1",
        ):
            self.assertIn(phrase, readme)

    def test_as_017_no_forbidden_or_generated_files_in_skills(self) -> None:
        failures: list[str] = []
        for path in SKILLS_ROOT.rglob("*"):
            if path.name in FORBIDDEN_FILENAMES or path.suffix in FORBIDDEN_SUFFIXES or "__pycache__" in path.parts:
                failures.append(str(path.relative_to(ROOT)))
            if path.is_symlink():
                failures.append(f"symlink: {path.relative_to(ROOT)}")
        self.assertEqual([], failures)


if __name__ == "__main__":
    unittest.main()
