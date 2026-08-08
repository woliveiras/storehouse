from __future__ import annotations

from typing import Iterable


VERDICTS = {"pass", "fail", "needs-review"}


def combine_verdicts(verdicts: Iterable[str]) -> str:
    values = list(verdicts)
    if not values or any(value not in VERDICTS for value in values):
        raise ValueError("verdicts must be pass, fail, or needs-review")
    if "fail" in values:
        return "fail"
    if "needs-review" in values:
        return "needs-review"
    return "pass"


def sanitize_result(raw: dict[str, object]) -> dict[str, str]:
    case_id = raw.get("case_id")
    verdict = raw.get("verdict")
    reason = raw.get("reason")
    if not isinstance(case_id, str) or verdict not in VERDICTS or not isinstance(reason, str):
        raise ValueError("result is missing safe required fields")
    # Raw reasons can echo prompts, credentials, canaries, or traces. Persist a
    # fixed category only; detailed evidence remains inside disposable state.
    return {"case_id": case_id, "verdict": str(verdict), "reason": "sanitized evaluation outcome"}
