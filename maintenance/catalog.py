from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

from maintenance.catalog_data import (
    CODEX_METADATA,
    COLLECTIONS,
    LICENSE_SHA256,
    MIGRATED,
    SENSITIVE,
    SOURCE_COMMIT,
    SOURCE_TREE_SHA256,
    TUXEDO_COMMIT,
    TUXEDO_TREE_SHA256,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ENV = "STOREHOUSE_GEREMMYAS_SOURCE"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def expand_collections() -> dict[str, list[str]]:
    by_name = {item["name"]: item for item in COLLECTIONS}
    expanded: dict[str, list[str]] = {}

    def visit(name: str, stack: tuple[str, ...] = ()) -> list[str]:
        if name in expanded:
            return expanded[name]
        if name in stack:
            raise RuntimeError(f"collection cycle: {' -> '.join((*stack, name))}")
        item = by_name[name]
        result = list(item.get("skills", []))
        for included in item.get("includes", []):
            result.extend(visit(included, (*stack, name)))
        if len(result) != len(set(result)):
            raise RuntimeError(f"duplicate expanded skill in {name}")
        expanded[name] = result
        return result

    for name in by_name:
        visit(name)
    return expanded


def render_install_commands() -> str:
    expanded = expand_collections()
    blocks: list[str] = []
    for item in COLLECTIONS:
        skills = expanded[item["name"]]
        command_lines = ["npx skills add woliveiras/storehouse \\"]
        for index, skill in enumerate(skills):
            suffix = " \\" if index < len(skills) - 1 else ""
            command_lines.append(f"  --skill {skill}{suffix}")
        blocks.extend(
            [
                f"### `{item['name']}`",
                "",
                item["description"],
                "",
                "```bash",
                *command_lines,
                "```",
                "",
            ]
        )
    return "\n".join(blocks).rstrip() + "\n"


def adaptation_note(relative: str) -> str:
    if relative == "skill-authoring/SKILL.md":
        return "Rewritten around the official Agent Skills format and standalone distribution."
    if relative in {
        "gcloud-operation/SKILL.md",
        "postgres-query-review/SKILL.md",
        "terraform-change/SKILL.md",
    }:
        return "Replaced the Geremmyas target marker with portable target evidence."
    if relative in {
        "manage-state-with-zustand/SKILL.md",
        "model-state-with-xstate/SKILL.md",
        "validate-with-zod/SKILL.md",
    }:
        return "Removed reliance on Geremmyas-installed auto-loading instruction files."
    if relative == "migrate-react-router/SKILL.md":
        return "Made dependency updates respect the consumer project's package manager."
    if relative == "game-art-2d/SKILL.md":
        return "Kept deliberate Codex image tooling while adding a standalone cross-client fallback."
    if relative == "scientific-paper/SKILL.md":
        return "Made companion-skill composition optional and changed script execution to UV."
    if relative.endswith("/SKILL.md") and relative.split("/", 1)[0].startswith(("game-", "gameplay", "procedural")):
        return "Made companion specialized-skill composition explicitly optional."
    return "Adapted for standalone portable use."


def build_skills_catalog(source: Path) -> dict[str, object]:
    expanded = expand_collections()
    categories = {
        skill: [name for name, names in expanded.items() if skill in names]
        for skill in MIGRATED
    }
    skills: list[dict[str, object]] = []
    for name in MIGRATED:
        source_root = source / "content" / "skills" / name
        destination_root = ROOT / "skills" / name
        source_files = sorted(item for item in source_root.rglob("*") if item.is_file())
        destination_paths = {
            item.relative_to(destination_root).as_posix()
            for item in destination_root.rglob("*")
            if item.is_file()
        }
        files: list[dict[str, object]] = []
        for source_file in source_files:
            path = source_file.relative_to(source_root).as_posix()
            destination_file = destination_root / path
            if not destination_file.is_file():
                disposition = "excluded"
                destination_digest = None
                note = "Excluded only when explicitly justified by the migration."
            else:
                destination_digest = sha256(destination_file)
                disposition = "preserved" if sha256(source_file) == destination_digest else "adapted"
                note = None if disposition == "preserved" else adaptation_note(f"{name}/{path}")
            entry: dict[str, object] = {
                "path": path,
                "disposition": disposition,
                "source_sha256": sha256(source_file),
            }
            if destination_digest:
                entry["destination_sha256"] = destination_digest
            if note:
                entry["note"] = note
            files.append(entry)
        source_paths = {item.relative_to(source_root).as_posix() for item in source_files}
        unexpected = destination_paths - source_paths
        if unexpected:
            raise RuntimeError(f"unowned destination files in {name}: {sorted(unexpected)}")
        domains = SENSITIVE.get(name, [])
        skills.append(
            {
                "name": name,
                "source_path": f"content/skills/{name}",
                "source_tree_sha256": tree_sha256(source_root),
                "categories": categories[name],
                "security": {
                    "sensitive": bool(domains),
                    "domains": domains,
                    "rationale": (
                        "Additional adversarial coverage is required for the listed sensitive surfaces."
                        if domains
                        else "Ordinary scoped writes remain protected by behavior-eval hashes and sentinels."
                    ),
                },
                "compatibility": {
                    "standalone": True,
                    "format": "Agent Skills",
                    "codex_openai_yaml": name in CODEX_METADATA,
                    "tuxedo": "optional",
                },
                "files": files,
            }
        )
    return {
        "schema_version": 1,
        "source": {
            "repository": "woliveiras/geremmyas",
            "commit": SOURCE_COMMIT,
            "skills_tree_listing_sha256": SOURCE_TREE_SHA256,
            "license": "MIT",
            "license_sha256": LICENSE_SHA256,
            "license_scope": "Geremmyas repository files at the frozen source commit; no skill-local exception was found.",
        },
        "tuxedo_exclusion_source": {
            "repository": "woliveiras/tuxedo",
            "commit": TUXEDO_COMMIT,
            "skills_tree_listing_sha256": TUXEDO_TREE_SHA256,
        },
        "skills": skills,
    }


def rendered_files(source: Path) -> dict[Path, str]:
    collections = {"schema_version": 1, "collections": list(COLLECTIONS)}
    skills = build_skills_catalog(source)
    return {
        ROOT / "catalog" / "collections.json": json.dumps(collections, indent=2, ensure_ascii=False) + "\n",
        ROOT / "catalog" / "skills.json": json.dumps(skills, indent=2, ensure_ascii=False) + "\n",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        parser.error("choose exactly one of --write or --check")
    raw_source = os.environ.get(SOURCE_ENV)
    if not raw_source:
        raise SystemExit(f"{SOURCE_ENV} is required for provenance generation/checking")
    source = Path(raw_source).expanduser().resolve()
    outputs = rendered_files(source)
    failures: list[str] = []
    for path, content in outputs.items():
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        elif not path.is_file() or path.read_text(encoding="utf-8") != content:
            failures.append(str(path.relative_to(ROOT)))
    if failures:
        print("catalog drift: " + ", ".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
