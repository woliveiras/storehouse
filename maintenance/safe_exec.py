from __future__ import annotations

import os
import sys

from evals.isolation import safe_temp_parent


def main() -> int:
    if len(sys.argv) < 2:
        raise SystemExit("usage: python -m maintenance.safe_exec COMMAND [ARG ...]")
    env = os.environ.copy()
    env["TMPDIR"] = str(safe_temp_parent())
    os.execvpe(sys.argv[1], sys.argv[1:], env)
    return 127


if __name__ == "__main__":
    raise SystemExit(main())
