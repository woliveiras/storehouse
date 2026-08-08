from __future__ import annotations

import os
import tempfile
import tomllib
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


ROOT = Path(__file__).resolve().parents[1]
EVAL_HOME_ENV = "AGENT_SKILLS_EVAL_CODEX_HOME"
DEFAULT_HOME = ".codex-agent-skills-evals"
ALLOWED_ROOT_ENTRIES = {
    "auth.json", "config.toml", "history.jsonl", "logs", "sessions", "shell_snapshots",
    "skills", "plugins", "state.sqlite", "state.sqlite-shm", "state.sqlite-wal", "version.json",
}
ALLOWED_CONFIG_KEYS = {"cli_auth_credentials_store", "projects"}
ALLOWED_PROJECT_KEYS = {"trust_level"}
ALLOWED_TRUST = {"trusted", "untrusted"}
SOURCE_ROOT_ENVS = ("AGENT_SKILLS_GEREMMYAS_SOURCE", "AGENT_SKILLS_TUXEDO_SOURCE")
SIBLING_SOURCE_ROOTS = (ROOT.parent / "geremmyas", ROOT.parent / "tuxedo")


def _inside(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def protected_roots() -> list[Path]:
    roots = [ROOT.resolve(), Path.home().resolve() / ".codex", *(path.resolve() for path in SIBLING_SOURCE_ROOTS if path.exists())]
    for name in SOURCE_ROOT_ENVS:
        raw = os.environ.get(name)
        if raw:
            source = Path(raw).expanduser()
            if not source.is_absolute():
                raise RuntimeError(f"{name} must be absolute before isolation can be proven")
            roots.append(source.resolve(strict=False))
    return roots


def assert_safe_scratch_parent(path: Path) -> Path:
    candidate = path.expanduser()
    if not candidate.is_absolute():
        raise RuntimeError("scratch parent must be absolute")
    resolved = candidate.resolve(strict=False)
    if any(_inside(resolved, root) for root in protected_roots()):
        raise RuntimeError("scratch parent overlaps a protected checkout or Codex home")
    for ancestor in (resolved, *resolved.parents):
        if (ancestor / ".git").exists():
            raise RuntimeError("scratch parent is inside a Git checkout")
    return resolved


def safe_temp_parent() -> Path:
    return assert_safe_scratch_parent(Path(tempfile.gettempdir()))


def resolve_dedicated_home() -> Path:
    raw = os.environ.get(EVAL_HOME_ENV, str(Path.home() / DEFAULT_HOME))
    candidate = Path(raw).expanduser()
    if not candidate.is_absolute():
        raise RuntimeError(f"{EVAL_HOME_ENV} must be an absolute path")
    lexical = Path(os.path.abspath(candidate))
    roots = protected_roots()
    configured = os.environ.get("CODEX_HOME")
    if configured:
        configured_path = Path(configured).expanduser()
        if not configured_path.is_absolute():
            raise RuntimeError("personal CODEX_HOME must be absolute before isolation can be proven")
        roots.append(configured_path.resolve(strict=False))
    if lexical == Path(lexical.anchor) or any(_inside(lexical, root) for root in roots):
        raise RuntimeError("dedicated evaluation home overlaps a checkout, root, or personal Codex home")
    resolved = candidate.resolve(strict=False)
    if any(_inside(resolved, root) for root in roots):
        raise RuntimeError("dedicated evaluation home resolves through a protected location")
    return resolved


def _assert_real_tree(path: Path) -> None:
    if path.is_symlink():
        raise RuntimeError(f"evaluation home content must not be a symlink: {path.name}")
    if path.is_dir():
        for child in path.iterdir():
            _assert_real_tree(child)


def validate_home_content(home: Path) -> None:
    if not home.exists():
        return
    if home.is_symlink() or not home.is_dir():
        raise RuntimeError("dedicated evaluation home must be a real directory")
    for entry in home.iterdir():
        _assert_real_tree(entry)
        if entry.name not in ALLOWED_ROOT_ENTRIES:
            raise RuntimeError(f"unknown evaluation-home entry: {entry.name}")
    skills = home / "skills"
    if skills.exists() and {item.name for item in skills.iterdir()} - {".system"}:
        raise RuntimeError("evaluation home contains non-system skills")
    plugins = home / "plugins"
    if plugins.exists():
        allowed = {"cache", ".remote-plugin-install-staging"}
        if {item.name for item in plugins.iterdir()} - allowed:
            raise RuntimeError("evaluation home contains unknown plugins")
        cache = plugins / "cache"
        if cache.exists() and {item.name for item in cache.iterdir()} - {"openai-curated-remote"}:
            raise RuntimeError("evaluation home contains an unknown plugin cache namespace")
        staging = plugins / ".remote-plugin-install-staging"
        if staging.exists() and any(staging.iterdir()):
            raise RuntimeError("evaluation home contains staged plugin content")
    config = home / "config.toml"
    if config.exists():
        try:
            parsed = tomllib.loads(config.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
            raise RuntimeError("evaluation config.toml is unreadable") from exc
        if set(parsed) - ALLOWED_CONFIG_KEYS:
            raise RuntimeError("evaluation config.toml contains behavior-bearing or unknown settings")
        projects = parsed.get("projects", {})
        if not isinstance(projects, dict):
            raise RuntimeError("evaluation project trust metadata must be a table")
        for project, metadata in projects.items():
            if not Path(project).is_absolute() or not isinstance(metadata, dict):
                raise RuntimeError("unsafe project trust metadata")
            if set(metadata) != ALLOWED_PROJECT_KEYS or metadata.get("trust_level") not in ALLOWED_TRUST:
                raise RuntimeError("unsupported project trust metadata")


def child_environment(home: Path) -> dict[str, str]:
    env = {key: os.environ[key] for key in ("PATH", "LANG", "LC_ALL", "TERM", "TMPDIR") if key in os.environ}
    env.update({"HOME": str(home), "XDG_CONFIG_HOME": str(home / "xdg-config"), "XDG_CACHE_HOME": str(home / "xdg-cache"), "CODEX_HOME": str(home), EVAL_HOME_ENV: str(home), "PROMPTFOO_DISABLE_SHARE": "true", "PROMPTFOO_DISABLE_TELEMETRY": "true"})
    return env


@contextmanager
def disposable_state() -> Iterator[tuple[Path, Path]]:
    with tempfile.TemporaryDirectory(prefix="agent-skills-eval-", dir=safe_temp_parent()) as raw:
        base = Path(raw).resolve()
        if any(_inside(base, root) for root in protected_roots()):
            raise RuntimeError("temporary evaluation state overlaps a protected root")
        workspace = base / "workspaces"
        promptfoo = base / "promptfoo"
        workspace.mkdir()
        promptfoo.mkdir()
        yield workspace, promptfoo
