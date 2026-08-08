from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

from evals.isolation import safe_temp_parent


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="storehouse-promptfoo-validate-", dir=safe_temp_parent()) as raw:
        state = Path(raw).resolve()
        env = {key: os.environ[key] for key in ("PATH", "LANG", "LC_ALL", "TERM") if key in os.environ}
        env.update({
            "PROMPTFOO_CONFIG_DIR": str(state),
            "PROMPTFOO_DISABLE_SHARE": "true",
            "PROMPTFOO_DISABLE_TELEMETRY": "true",
            "STOREHOUSE_EVAL_CODEX_HOME": str(state / "unused-codex-home"),
            "STOREHOUSE_EVAL_WORKSPACE_ROOT": str(state / "unused-workspace"),
        })
        env.pop("OPENAI_API_KEY", None)
        env.pop("CODEX_API_KEY", None)
        completed = subprocess.run(
            ["pnpm", "exec", "promptfoo", "validate", "-c", "evals/promptfoo/promptfooconfig.yaml"],
            cwd=ROOT, env=env, check=False,
        )
        if completed.returncode:
            return completed.returncode
    print("Promptfoo configuration is valid in disposable local state.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
