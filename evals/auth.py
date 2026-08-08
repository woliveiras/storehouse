from __future__ import annotations

import argparse
import shutil
import subprocess

from evals.isolation import child_environment, resolve_dedicated_home, validate_home_content


EXPECTED_STATUS = "Logged in using ChatGPT"


def _codex() -> str:
    configured = __import__("os").environ.get("STOREHOUSE_EVAL_CODEX_PATH", "codex")
    return shutil.which(configured) or configured


def status(require_login: bool = False) -> bool:
    home = resolve_dedicated_home()
    validate_home_content(home)
    if not home.exists():
        if require_login:
            raise RuntimeError("dedicated evaluation home does not exist; run eval:login explicitly")
        print("Dedicated evaluation home does not exist; not logged in.")
        return False
    completed = subprocess.run(
        [_codex(), "login", "status"], env=child_environment(home), text=True,
        capture_output=True, check=False,
    )
    combined = "\n".join((completed.stdout, completed.stderr)).strip()
    labels = {line.strip() for line in combined.splitlines() if line.strip()}
    if completed.returncode != 0 or labels != {EXPECTED_STATUS}:
        if require_login:
            raise RuntimeError("dedicated Codex home is not authenticated with ChatGPT")
        print("Dedicated evaluation home is not authenticated with ChatGPT.")
        return False
    print(EXPECTED_STATUS)
    return True


def login() -> None:
    home = resolve_dedicated_home()
    validate_home_content(home)
    home.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run([_codex(), "login"], env=child_environment(home), check=False)
    if completed.returncode != 0 or not status(require_login=True):
        raise RuntimeError("dedicated ChatGPT/Codex login failed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("status", "login"))
    args = parser.parse_args()
    if args.action == "login":
        login()
    else:
        status()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
