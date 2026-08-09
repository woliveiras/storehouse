from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from maintenance.catalog_data import SKILLS


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    validator = shutil.which("agentskills")
    if not validator:
        raise SystemExit("official agentskills validator is unavailable; run through UV with the locked dev group")
    failures: list[str] = []
    for skill in SKILLS:
        result = subprocess.run(
            [validator, "validate", str(ROOT / "skills" / skill)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        if result.returncode:
            failures.append(f"{skill}: {(result.stdout + result.stderr).strip()}")
    if failures:
        raise SystemExit("official skill validation failed:\n" + "\n".join(failures))
    print(f"Official Agent Skills validation passed for {len(SKILLS)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
