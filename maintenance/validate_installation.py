from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from maintenance.catalog import expand_collections
from evals.isolation import safe_temp_parent


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "node_modules" / ".bin" / "skills"


def _run(command: list[str], cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, check=False)
    if completed.returncode:
        raise RuntimeError(f"installation command failed: {' '.join(command)}\n{completed.stdout}\n{completed.stderr}")
    return completed


def clean_environment(home: Path) -> dict[str, str]:
    env = {key: os.environ[key] for key in ("PATH", "LANG", "LC_ALL", "TERM", "TMPDIR") if key in os.environ}
    env.update({"HOME": str(home), "XDG_CONFIG_HOME": str(home / "xdg-config"), "XDG_CACHE_HOME": str(home / "xdg-cache"), "DISABLE_TELEMETRY": "1", "DO_NOT_TRACK": "1"})
    return env


def installation_commands(collection: list[str]) -> dict[str, list[str]]:
    multi = [str(CLI), "add", str(ROOT)]
    for skill in collection:
        multi.extend(["--skill", skill])
    multi.extend(["--agent", "claude-code", "opencode", "github-copilot", "--copy", "-y"])
    return {
        "list": [str(CLI), "add", str(ROOT), "--list"],
        "single": [str(CLI), "add", str(ROOT), "--skill", "gameplay-programming-2d", "--agent", "codex", "--copy", "-y"],
        "collection": multi,
    }


def main() -> int:
    if not CLI.is_file():
        raise SystemExit("pinned skills CLI is unavailable; run pnpm install --frozen-lockfile")
    with tempfile.TemporaryDirectory(prefix="agent-skills-install-", dir=safe_temp_parent()) as raw:
        scratch = Path(raw).resolve()
        protected = [ROOT.resolve(), Path.home().resolve() / ".codex"]
        for name in ("AGENT_SKILLS_GEREMMYAS_SOURCE", "AGENT_SKILLS_TUXEDO_SOURCE"):
            if os.environ.get(name):
                protected.append(Path(os.environ[name]).expanduser().resolve())
        if any(scratch == root or root in scratch.parents for root in protected):
            raise RuntimeError("clean-room scratch overlaps a protected path")
        home = scratch / "home"
        project = scratch / "project"
        home.mkdir()
        project.mkdir()
        env = clean_environment(home)
        _run(["git", "init", "--quiet"], project, env)
        collection = expand_collections()["game-core"]
        commands = installation_commands(collection)
        listed = _run(commands["list"], project, env)
        if "gameplay-programming-2d" not in listed.stdout + listed.stderr:
            raise RuntimeError("official CLI did not discover the representative skill")
        _run(commands["single"], project, env)
        single_path = project / ".agents/skills/gameplay-programming-2d/SKILL.md"
        if not single_path.is_file():
            raise RuntimeError("Codex project installation was not discoverable")
        multi = _run(commands["collection"], project, env)
        universal = {skill for skill in collection if (project / f".agents/skills/{skill}/SKILL.md").is_file()}
        claude = {skill for skill in collection if (project / f".claude/skills/{skill}/SKILL.md").is_file()}
        if universal != set(collection) or claude != set(collection):
            raise RuntimeError(f"multi-skill installation discovery incomplete: universal={sorted(universal)} claude={sorted(claude)}")
        report = {
            "cli_version": _run([str(CLI), "--version"], project, env).stdout.strip(),
            "single": "gameplay-programming-2d",
            "collection": "game-core",
            "collection_skills": collection,
            "targets_requested": ["codex", "claude-code", "opencode", "github-copilot"],
            "discovery_paths_observed": [".agents/skills", ".claude/skills"],
            "personal_configuration_touched": False,
            "scratch_removed_on_exit": True,
            "output_excerpt": " ".join((listed.stdout + multi.stdout).split())[:400],
        }
        print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
