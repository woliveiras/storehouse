from __future__ import annotations

import json
import re
import subprocess
import tomllib
import unittest
from pathlib import Path
from urllib.parse import unquote

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
RESOURCE_REFERENCE = re.compile(
    r"(?<![A-Za-z0-9_.-])((?:references|scripts|assets)/[A-Za-z0-9_./-]+)"
)
FORBIDDEN_FILENAMES = {
    ".DS_Store",
    "Thumbs.db",
    "package.json",
    "pnpm-lock.yaml",
    "pyproject.toml",
    "uv.lock",
}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo", ".log"}


def skill_names() -> set[str]:
    return {
        path.name
        for path in SKILLS_ROOT.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }


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
        result = list(item.get("skills", []))
        for included in item.get("includes", []):
            result.extend(visit(included, (*stack, name)))
        if len(result) != len(set(result)):
            raise AssertionError(f"duplicate expanded skill in collection {name}")
        expanded[name] = result
        return result

    for collection_name in by_name:
        visit(collection_name)
    return expanded


def render_install_commands(catalog: dict[str, object]) -> str:
    expanded = expand_collections(catalog)
    blocks: list[str] = []
    for item in catalog["collections"]:
        command = ["npx skills add woliveiras/storehouse \\"]
        skills = expanded[item["name"]]
        for index, skill in enumerate(skills):
            suffix = " \\" if index < len(skills) - 1 else ""
            command.append(f"  --skill {skill}{suffix}")
        blocks.extend(
            [
                f"### `{item['name']}`",
                "",
                item["description"],
                "",
                "```bash",
                *command,
                "```",
                "",
            ]
        )
    return "\n".join(blocks).strip()


class RepositoryContractTests(unittest.TestCase):
    def test_public_identity_is_canonical(self) -> None:
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        schema = json.loads(
            (ROOT / "catalog" / "collections.schema.json").read_text(encoding="utf-8")
        )
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertEqual("storehouse", package["name"])
        self.assertEqual("storehouse", pyproject["project"]["name"])
        self.assertIn("Storehouse", package["description"])
        self.assertIn("Storehouse", pyproject["project"]["description"])
        self.assertEqual(
            "https://github.com/woliveiras/storehouse/catalog/collections.schema.json",
            schema["$id"],
        )
        self.assertTrue(readme.startswith("# Storehouse\n"))

    def test_no_legacy_repository_identity(self) -> None:
        legacy_name = "agent" + "-skills"
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
            text = path.read_text(encoding="utf-8", errors="ignore")
            if legacy_name in text:
                failures.append(str(path.relative_to(ROOT)))
        self.assertEqual([], failures)

    def test_skill_frontmatter_and_routing(self) -> None:
        for skill in sorted(skill_names()):
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

    def test_relative_links_and_owned_resources_resolve(self) -> None:
        failures: list[str] = []
        for markdown in SKILLS_ROOT.rglob("*.md"):
            text = markdown.read_text(encoding="utf-8")
            skill_root = SKILLS_ROOT / markdown.relative_to(SKILLS_ROOT).parts[0]
            for raw in LINK.findall(text):
                target = raw.split("#", 1)[0].strip().strip("<>")
                if not target or re.match(r"^(?:https?|mailto):", target):
                    continue
                resolved = (markdown.parent / unquote(target)).resolve()
                try:
                    resolved.relative_to(skill_root)
                except ValueError:
                    failures.append(f"escaping link {markdown.relative_to(ROOT)} -> {target}")
                    continue
                if not resolved.exists():
                    failures.append(f"missing link {markdown.relative_to(ROOT)} -> {target}")
            for raw in RESOURCE_REFERENCE.findall(text):
                target = raw.rstrip(".,:;)")
                if not (markdown.parent / target).exists():
                    failures.append(f"missing resource {markdown.relative_to(ROOT)} -> {target}")
        self.assertEqual([], failures)

    def test_skill_yaml_is_valid(self) -> None:
        failures: list[str] = []
        for path in [*SKILLS_ROOT.rglob("*.yaml"), *SKILLS_ROOT.rglob("*.yml")]:
            try:
                parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
            except yaml.YAMLError as exc:
                failures.append(f"{path.relative_to(ROOT)}: {exc}")
                continue
            if not isinstance(parsed, dict):
                failures.append(f"{path.relative_to(ROOT)} is not a mapping")
        self.assertEqual([], failures)

    def test_skills_have_no_repository_or_personal_dependencies(self) -> None:
        forbidden = {
            "/Users/": "personal absolute path",
            "catalog/collections.json": "repository catalog",
            "evals/": "repository evaluation harness",
            "tests/": "repository test suite",
        }
        failures: list[str] = []
        for path in SKILLS_ROOT.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for needle, reason in forbidden.items():
                if needle.casefold() in text.casefold():
                    failures.append(f"{path.relative_to(ROOT)}: {reason}")
        self.assertEqual([], failures)

    def test_skill_dependency_and_composition_contracts(self) -> None:
        names = skill_names()
        script_metadata = "\n".join(
            path.read_text(encoding="utf-8") for path in SKILLS_ROOT.rglob("*.py")
        )
        self.assertNotIn("Pillow>=", script_metadata)
        self.assertIn("Pillow==12.0.0", script_metadata)

        rust = (
            (SKILLS_ROOT / "ci-rust/SKILL.md").read_text(encoding="utf-8")
            + (SKILLS_ROOT / "release-rust/SKILL.md").read_text(encoding="utf-8")
        )
        self.assertNotIn("rust-toolchain@stable", rust)
        self.assertNotIn("cargo +nightly miri", rust)

        skill_pattern = "|".join(
            re.escape(name) for name in sorted(names, key=len, reverse=True)
        )
        for skill in names:
            text = (SKILLS_ROOT / skill / "SKILL.md").read_text(encoding="utf-8")
            for match in re.finditer(rf"\$(?:{skill_pattern})", text):
                nearby = text[max(0, match.start() - 180) : match.start()].casefold()
                self.assertTrue(
                    "if installed" in nearby or "optional" in nearby,
                    f"mandatory companion reference in {skill}",
                )

        art = (SKILLS_ROOT / "game-dev-2d-art/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("optional helpers", art)
        self.assertIn("skill itself does not", art)
        self.assertIn("fallback", art.casefold())

    def test_game_scope_is_2d_phaser_or_godot(self) -> None:
        for name in {name for name in skill_names() if "game-dev-2d" in name}:
            tree = "\n".join(
                path.read_text(encoding="utf-8", errors="replace")
                for path in (SKILLS_ROOT / name).rglob("*")
                if path.is_file()
            )
            self.assertIn("2D", tree, name)
            self.assertRegex(tree, r"Phaser|Godot", name)
            self.assertNotRegex(tree, r"(?i)\bUnity\b|\bPixiJS\b", name)
            for line in (line for line in tree.splitlines() if re.search(r"(?i)\b3D\b", line)):
                self.assertRegex(
                    line,
                    r"(?i)do not use|route .* elsewhere",
                    f"unbounded 3D scope in {name}",
                )

    def test_collections_are_valid_and_cover_every_skill(self) -> None:
        catalog = json.loads(
            (ROOT / "catalog" / "collections.json").read_text(encoding="utf-8")
        )
        schema = json.loads(
            (ROOT / "catalog" / "collections.schema.json").read_text(encoding="utf-8")
        )
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(catalog)

        expanded = expand_collections(catalog)
        self.assertEqual(
            skill_names(), set().union(*(set(value) for value in expanded.values()))
        )
        self.assertEqual(
            [
                "game-dev-2d-gameplay",
                "game-dev-2d-testing",
                "game-dev-2d-ui-accessibility",
                "game-dev-2d-feel",
                "game-dev-2d-ai",
                "game-dev-2d-procedural-generation",
                "game-dev-2d-save-progression",
                "game-dev-2d-performance",
                "game-dev-2d-audio",
                "game-dev-2d-art",
                "ci-game-dev-2d",
                "release-game-dev-2d",
            ],
            expanded["game-dev"],
        )

    def test_collection_graph_rejects_cycles_and_duplicates(self) -> None:
        with self.assertRaises(AssertionError):
            expand_collections(
                {
                    "collections": [
                        {"name": "a", "skills": ["one"], "includes": ["b"]},
                        {"name": "b", "includes": ["a"]},
                    ]
                }
            )
        with self.assertRaises(KeyError):
            expand_collections(
                {"collections": [{"name": "a", "includes": ["missing"]}]}
            )
        with self.assertRaises(AssertionError):
            expand_collections(
                {
                    "collections": [
                        {"name": "a", "skills": ["one"], "includes": ["b"]},
                        {"name": "b", "skills": ["one"]},
                    ]
                }
            )

    def test_readme_collection_commands_match_catalog(self) -> None:
        catalog = json.loads(
            (ROOT / "catalog" / "collections.json").read_text(encoding="utf-8")
        )
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        actual = (
            readme.split("<!-- collections:start -->", 1)[1]
            .split("<!-- collections:end -->", 1)[0]
            .strip()
        )
        self.assertEqual(render_install_commands(catalog), actual)
        for phrase in (
            "Baseline",
            "project",
            "independent",
            "collection",
            "npx skills add woliveiras/storehouse --list",
            "npx skills update",
            "npx skills remove",
            "DISABLE_TELEMETRY=1",
        ):
            self.assertIn(phrase, readme)

    def test_no_generated_files_or_symlinks_in_skills(self) -> None:
        failures: list[str] = []
        for path in SKILLS_ROOT.rglob("*"):
            if (
                path.name in FORBIDDEN_FILENAMES
                or path.suffix in FORBIDDEN_SUFFIXES
                or "__pycache__" in path.parts
            ):
                failures.append(str(path.relative_to(ROOT)))
            if path.is_symlink():
                failures.append(f"symlink: {path.relative_to(ROOT)}")
        self.assertEqual([], failures)


if __name__ == "__main__":
    unittest.main()
