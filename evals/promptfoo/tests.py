from __future__ import annotations

import json
import os
from pathlib import Path


def _rubric() -> dict[str, object]:
    return {
        "type": "llm-rubric",
        "value": (
            "Secondary review only: judge whether the final response accurately describes the bounded "
            "observable result and limitations. It cannot override any deterministic workspace failure."
        ),
        "provider": {
            "id": "openai:codex-sdk",
            "config": {
                "model_reasoning_effort": "medium",
                "working_dir": "{{ env.AGENT_SKILLS_EVAL_GRADER_ROOT }}",
                "sandbox_mode": "read-only",
                "approval_policy": "never",
                "network_access_enabled": False,
                "web_search_enabled": False,
                "web_search_mode": "disabled",
                "persist_threads": False,
                "skip_git_repo_check": True,
                "codex_path_override": "{{ env.AGENT_SKILLS_EVAL_CODEX_PATH | default(\"codex\") }}",
                "cli_env": {"CODEX_HOME": "{{ env.AGENT_SKILLS_EVAL_CODEX_HOME }}"},
            },
        },
    }


def generate_tests() -> list[dict[str, object]]:
    raw = os.environ.get("AGENT_SKILLS_EVAL_CASES")
    if not raw:
        # Config validation must remain provider-free and independent of prepared workspaces.
        return [{
            "description": "configuration-smoke",
            "vars": {"workspace_key": "configuration-smoke", "request": "Return a bounded smoke result."},
            "assert": [{"type": "python", "value": "file://assertions.py"}],
        }]
    path = Path(raw)
    cases = json.loads(path.read_text(encoding="utf-8"))
    tests: list[dict[str, object]] = []
    for item in cases:
        assertions: list[dict[str, object]] = [{
            "type": "python",
            "value": "file://assertions.py",
        }]
        if item["secondary_review"]:
            assertions.append(_rubric())
        tests.append({
            "description": item["case_id"],
            "vars": {
                "workspace_key": item["workspace_key"],
                "request": item["request"],
                "case_id": item["case_id"],
                "kind": item["kind"],
                "expected_skill": item.get("expected_skill", ""),
                "avoid_skill": item.get("avoid_skill", ""),
                "secondary_review_attached": item["secondary_review"],
                "required_outputs": item.get("required_outputs", []),
            },
            "assert": assertions,
        })
    return tests
