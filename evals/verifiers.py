from __future__ import annotations

import json
import hashlib
import os
import re
import subprocess
import shutil
from pathlib import Path

import yaml

from evals.oracle_data import ORACLES


def _json(workspace: Path, relative: str) -> dict[str, object]:
    value = json.loads((workspace / relative).read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def _source(workspace: Path, relative: str) -> str:
    path = workspace / relative
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def _node_test(workspace: Path, relative: str) -> bool:
    node = shutil.which("node")
    sandbox = shutil.which("sandbox-exec")
    if not node or not sandbox:
        return False
    root = workspace.resolve()
    profile = f'''(version 1)
(allow default)
(deny network*)
(deny process-fork)
(deny file-write*)
(deny file-read* (subpath {json.dumps(str(Path.home().resolve()))}))'''
    completed = subprocess.run(
        [sandbox, "-p", profile, node, relative], cwd=workspace,
        env={"PATH": os.environ.get("PATH", ""), "HOME": str(root), "TMPDIR": str(root), "NODE_NO_WARNINGS": "1"},
        text=True, capture_output=True, timeout=10, check=False,
    )
    return completed.returncode == 0


def _artifact_checks(skill: str, workspace: Path) -> list[dict[str, object]]:
    checks: list[tuple[str, bool]] = []
    ci_contracts = {
        "android-ci-setup": (".github/workflows/android.yml", ("actions/checkout@v4", "actions/setup-java@v4", "gradle/actions/setup-gradle@v4")),
        "go-ci-setup": (".github/workflows/go.yml", ("actions/checkout@v4", "actions/setup-go@v5")),
        "python-ci-setup": (".github/workflows/python.yml", ("actions/checkout@v4", "astral-sh/setup-uv@v6")),
        "rust-ci-setup": (".github/workflows/rust.yml", ("actions/checkout@v4", "dtolnay/rust-toolchain@1.88.0", "EmbarkStudios/cargo-deny-action@v2")),
        "typescript-ci-setup": (".github/workflows/typescript.yml", ("actions/checkout@v4", "actions/setup-node@v4")),
    }
    if skill in ci_contracts:
        relative, required_uses = ci_contracts[skill]
        raw = _source(workspace, relative)
        parsed = yaml.load(raw, Loader=yaml.BaseLoader)
        jobs = parsed.get("jobs", {}) if isinstance(parsed, dict) else {}
        verify = jobs.get("verify", {}) if isinstance(jobs, dict) else {}
        steps = verify.get("steps", []) if isinstance(verify, dict) else []
        uses = [step.get("uses") for step in steps if isinstance(step, dict) and isinstance(step.get("uses"), str)] if isinstance(steps, list) else []
        triggers = parsed.get("on", []) if isinstance(parsed, dict) else []
        allowed_triggers = {"push", "pull_request", "workflow_dispatch"}
        trigger_names = set(triggers) if isinstance(triggers, list) else set(triggers) if isinstance(triggers, dict) else {triggers} if isinstance(triggers, str) else set()
        runner = verify.get("runs-on") if isinstance(verify, dict) else None
        checks += [("workflow-trigger", bool(trigger_names) and trigger_names <= allowed_triggers), ("workflow-runner", runner in {"ubuntu-latest", "macos-latest", "windows-latest"}), ("workflow-steps", isinstance(steps, list) and bool(steps)), ("workflow-pinned-setup", all(action in uses for action in required_uses))]
    elif skill == "chromadb-rag-workflow":
        code = _source(workspace, "src/retrieval.py")
        documents = json.loads(_source(workspace, "data/documents.json"))
        result = _json(workspace, "behavior/retrieval-results.json")
        expected = {}
        for tenant in ("a", "b"):
            ranked = sorted((item for item in documents if item.get("tenant") == tenant), key=lambda item: (-item["score"], item["id"]))
            expected[f"tenant_{tenant}_query"] = {"returned_tenants": [item["tenant"] for item in ranked], "stable_ids": [item["id"] for item in ranked]}
        checks += [("implementation-scopes-query", "collection.query" in code and bool(re.search(r"where\s*=\s*\{[^}]*tenant[^}]*tenant_id", code))), ("derived-ranking", all(result.get(key) == value for key, value in expected.items())), ("derived-isolation", result.get("cross_tenant_leak") is False and all(set(value["returned_tenants"]) == {tenant} for tenant, value in (("a", expected["tenant_a_query"]), ("b", expected["tenant_b_query"]))))]
    elif skill == "game-ai-2d":
        code = _source(workspace, "src/guard_ai.gd")
        telegraph = code.find("telegraph_ready = true")
        chase = code.find("state = State.CHASE")
        checks += [("implementation-transitions", all(token in code for token in ('event == "sees_target"', 'event == "loses_target"', 'event == "timeout"', "state = State.CHASE", "state = State.LOST", "state = State.PATROL"))), ("implementation-pause-gate", bool(re.search(r"if paused:\s*\n\s*return state", code))), ("implementation-telegraphs-first", 0 <= telegraph < chase)]
    elif skill == "game-audio-2d":
        code = _source(workspace, "src/audio-owner.ts")
        test = _source(workspace, "tests/audio-owner.test.ts")
        checks += [("implementation-single-owner", "private static owner" in code and "static get" in code), ("implementation-mute-state", "setMuted" in code and "this.muted=value" in code), ("implementation-crossfade-disposes", "crossfade" in code and "disposedPlayers" in code and "this.current=next" in code), ("tests-lifecycle", all(token in test for token in ("first!==second", "setMuted(true)", "crossfade('battle')", "disposedPlayers!==1")))]
    elif skill == "gcloud-operation":
        context = _json(workspace, "context.json")
        plan = _json(workspace, "operation-plan.json")
        expected_command = ["gcloud", "run", "services", "describe", "fixture", "--account", context.get("account"), "--project", context.get("project"), "--region", context.get("region")]
        checks += [("context-is-synthetic-and-read-only", context.get("allow_remote_mutation") is False and str(context.get("account", "")).endswith(".invalid")), ("plan-derives-context", all(plan.get(key) == context.get(key) for key in ("account", "project", "region"))), ("exact-read-only-command", plan.get("read_only") is True and plan.get("command") == expected_command)]
    elif skill == "game-feel-2d":
        code = _source(workspace, "src/jump_feedback.gd")
        test = _source(workspace, "tests/jump_feedback.test.gd")
        function = re.fullmatch(r"func apply_jump_feedback\(reduced_motion: bool\):\s*\n\s*var shake = (\d+) if reduced_motion else (\d+)\s*\n\s*return shake\s*", code)
        derived = (int(function.group(2)), int(function.group(1))) if function else None
        checks += [("implementation-executable-truth-table", derived == (2, 0)), ("tests-both-motion-modes", all(token in test for token in ("false) == 2", "true) == 0", "assert(")))]
    elif skill == "game-performance-2d":
        code = _source(workspace, "src/update-optimized.ts")
        test = _source(workspace, "tests/update-parity.test.ts")
        checks += [("implementation-parity-operation", bool(re.search(r"for\s*\(const item of items\).*item\s*\*\s*2", code))), ("implementation-removes-map-callback", ".map(" not in code), ("tests-compare-baseline", all(token in test for token in ("from '../src/update.ts'", "from '../src/update-optimized.ts'", "JSON.stringify(update(input))", "throw new Error"))), ("tests-execute", _node_test(workspace, "tests/update-parity.test.ts"))]
    elif skill == "game-save-n-progress":
        code = _source(workspace, "src/save_store.gd")
        test = _source(workspace, "tests/save_store.test.gd")
        migrate_ordered = code.find("if data.version > CURRENT_VERSION") < code.find("var migrated = data.duplicate(true)") < code.find("if migrated.version == 1") < code.find("return migrated")
        atomic_ordered = code.find("FileAccess.open(temp_path") < code.find("store_string(payload)") < code.find("flush()") < code.find("close()") < code.find("rename_absolute(temp_path, final_path)")
        checks += [("implementation-preserves-before-migration", migrate_ordered and "migrated.version = 2" in code and "return data" not in code), ("implementation-rejects-future", bool(re.search(r"if data\.version > CURRENT_VERSION:\s*\n\s*return \{\"error\": \"future-version\"\}", code))), ("implementation-atomic-replace", atomic_ordered), ("implementation-backup-recovery", bool(re.search(r"func load_with_backup\(primary, backup\):\s*\n\s*return primary if primary != null else backup", code))), ("implementation-self-contained", "parse_save" not in code), ("tests-migration-recovery-atomicity", all(token in test for token in ('"coins":7', '"version":3', "null", "load_with_backup", '"save.tmp"', '"save.json"')))]
    elif skill == "game-testing-2d":
        code = _source(workspace, "tests/attack-window.test.mjs")
        trusted_source = workspace / "src/attack-window.mjs"
        source_is_exact = trusted_source.is_file() and trusted_source.read_text(encoding="utf-8") == ORACLES[skill]["inputs"]["src/attack-window.mjs"]
        checks += [("test-exercises-system", "import { AttackWindow }" in code and code.count(".attack(") >= 4), ("test-covers-lifecycle", "setPaused(true)" in code and "restart()" in code), ("test-has-observable-failures", code.count("throw new Error") >= 4), ("protected-system-is-exact", source_is_exact)]
        if source_is_exact:
            driver = """const {AttackWindow}=await import(process.argv[1]);const w=new AttackWindow();const result={valid_target_hits:w.attack('target')?1:0,repeat_target_hits:w.attack('target')?1:0};w.setPaused(true);result.paused_hits=w.attack('other')?1:0;w.restart();result.after_scene_restart_hits=w.attack('target')?1:0;console.log(JSON.stringify(result));"""
            completed = subprocess.run(
                ["node", "--input-type=module", "-e", driver, trusted_source.resolve().as_uri()],
                cwd=workspace,
                env={"PATH": os.environ.get("PATH", ""), "NODE_NO_WARNINGS": "1"},
                text=True,
                capture_output=True,
                timeout=5,
                check=False,
            )
            try:
                derived = json.loads(completed.stdout) if completed.returncode == 0 else {}
            except json.JSONDecodeError:
                derived = {}
            reported = _json(workspace, "behavior/attack-results.json")
            expected = {"valid_target_hits": 1, "repeat_target_hits": 0, "paused_hits": 0, "after_scene_restart_hits": 1}
            checks += [("protected-system-behavior", derived == expected), ("report-matches-derived-behavior", reported == derived)]
    elif skill == "game-ui-accessibility":
        code = _source(workspace, "src/pause-menu.ts").replace(" ", "")
        test = _source(workspace, "tests/pause-menu.test.ts")
        checks += [("implementation-focus-order", "items:['resume','settings','quit']" in code), ("implementation-touch-target", bool(re.search(r"touchTarget:(?:4[4-9]|[5-9][0-9]|[1-9][0-9]{2,})", code))), ("implementation-reflow", all(token in code for token in ("maxWidthPercent:100", "wrap:true", "overflow:'auto'"))), ("implementation-accessibility-state", all(token in code for token in ("accessibleName:", "restoreFocus:true", "reducedMotionPreservesState:true"))), ("tests-a11y-reflow-motion", all(token in test for token in ("order", "a11y", "reflow", "reduced motion", "throw new Error"))), ("tests-execute", _node_test(workspace, "tests/pause-menu.test.ts"))]
    elif skill == "gameplay-programming-2d":
        code = _source(workspace, "src/dash.ts").replace(" ", "")
        test = _source(workspace, "tests/dash.test.ts")
        checks += [("implementation-cooldown-gate", "if(this.remaining>0)returnfalse" in code and "this.remaining=this.cooldown" in code), ("implementation-collision-stops", "collide(){this.active=false}" in code), ("implementation-restart-clears", "restart(){this.active=false;this.remaining=0}" in code), ("tests-lifecycle", all(token in test for token in ("cooldown", "collision", "pause", "restart", "throw new Error"))), ("tests-execute", _node_test(workspace, "tests/dash.test.ts"))]
    elif skill == "langgraph-agent-design":
        code = _source(workspace, "src/graph.py")
        model = _json(workspace, "behavior/graph-results.json")
        checks += [("implementation-framework", all(token in code for token in ("from langgraph.graph import StateGraph", "from langgraph.types import interrupt", "StateGraph(State)", "add_node", "add_conditional_edges", "compile(checkpointer=MemorySaver())"))), ("implementation-no-write-before-approval", "add_edge('approval', 'write')" not in code and "add_conditional_edges('approval', route" in code and "interrupt(" in code), ("derived-approval-route", model.get("route_unapproved") == "END" and model.get("route_approved") == "write" and model.get("nodes") == ["collect", "approval", "write"] and model.get("interrupt_before_write") is True), ("derived-checkpoint", model.get("checkpoint") == "memory" and model.get("resume_node") == "approval")]
    elif skill == "manage-state-with-zustand":
        code = _source(workspace, "src/cart-store.ts").replace(" ", "")
        test = _source(workspace, "tests/cart-store.test.ts")
        checks += [("implementation-framework", "from'zustand'" in code and "create<CartState>()" in code and "persist(" in code), ("implementation-derived-total", "reduce((sum,item)=>sum+item.price,0)" in code), ("implementation-actions", "set(s=>({items:[...s.items,item]}))" in code and "set({items:[]})" in code), ("implementation-scoped-persistence", "name:'cart-v1'" in code and "partialize:s=>({items:s.items})" in code), ("tests-behavior", all(token in test for token in ("selectTotal", ".add({price:12})", ".reset()", "throw new Error")))]
    elif skill == "skill-authoring":
        skill_path = workspace / "normalize-json/SKILL.md"
        raw = _source(workspace, "normalize-json/SKILL.md")
        match = re.match(r"\A---\n(.*?)\n---\n", raw, re.DOTALL)
        try:
            metadata = yaml.safe_load(match.group(1)) if match else None
        except yaml.YAMLError:
            metadata = None
        link = re.search(r"\]\(([^)]+)\)", raw)
        linked = skill_path.parent / link.group(1) if link else None
        checks += [("frontmatter-valid", isinstance(metadata, dict)), ("folder-name-matches", isinstance(metadata, dict) and metadata.get("name") == skill_path.parent.name == "normalize-json"), ("description-routes", isinstance(metadata, dict) and "Use when" in str(metadata.get("description")) and "Do not use" in str(metadata.get("description"))), ("owned-link-exists", linked is not None and linked.is_file() and skill_path.parent.resolve() in linked.resolve().parents)]
    elif skill == "migrate-react-router":
        code = _source(workspace, "src/routes.tsx").replace(" ", "")
        test = _source(workspace, "tests/routes.test.ts").replace(" ", "")
        checks += [("implementation-data-router", "from'react-router'" in code and "createBrowserRouter([" in code), ("implementation-loader-param", "path:'/books/:id'" in code and "bookId:params.id" in code), ("implementation-not-found", "thrownewResponse('Notfound',{status:404})" in code), ("implementation-route-component", "Component:Book" in code), ("tests-loader-and-404", all(token in test for token in ("bookLoader", "id:'42'", "params:{}", "error.status!==404")))]
    elif skill == "llm-integration-review":
        review = _source(workspace, "llm-review.md")
        patch = _source(workspace, "remediation.diff")
        checks += [("review-anchored", "src/endpoint.ts:1" in review), ("bounded-remediation-patch", all(token in patch for token in ("--- a/src/endpoint.ts", "+++ b/src/endpoint.ts", "@@ -1 +1 @@", "-export async function ask", "+export async function ask", "redacted")))]
    elif skill == "model-state-with-xstate":
        code = _source(workspace, "src/checkout-machine.ts").replace(" ", "")
        test = _source(workspace, "tests/checkout-machine.test.ts")
        checks += [("implementation-framework", "from'xstate'" in code and "createMachine(" in code and "events:Event" in code), ("implementation-transition-table", all(token in code for token in ("initial:'idle'", "START:'submitting'", "RETRY:'submitting'", "CANCEL:'cancelled'"))), ("tests-derived-transitions", all(token in test for token in ("createActor", "type:'START'", "type:'RETRY'", "type:'CANCEL'", "getSnapshot()"))), ("tests-invalid-event-stable", all(token in test for token in ("invalid.send({type:'RETRY'})", "value!=='idle'", "invalid event")))]
    elif skill == "paper-review":
        original = ORACLES[skill]["inputs"]["manuscript.md"]
        revised = _source(workspace, "manuscript.md")
        original_frontmatter = original.split("---\n", 2)[1]
        revised_parts = revised.split("---\n", 2)
        checks += [("frontmatter-preserved-exactly", len(revised_parts) == 3 and revised_parts[1] == original_frontmatter), ("body-was-revised", revised != original and "Claim without evidence." not in revised)]
    elif skill == "procedural-generation-2d":
        code = _source(workspace, "src/room_generator.gd")
        model = _json(workspace, "behavior/generator-model.json")
        required = {"algorithm": "lcg", "multiplier": 1664525, "increment": 1013904223, "modulus": 4294967296, "room_count": 6, "backbone": "previous-to-current", "spawn_count": 3}
        model_valid = all(model.get(key) == value for key, value in required.items())
        def generate(seed: int) -> dict[str, object]:
            state = seed
            rooms = []
            for index in range(model.get("room_count", 0) if isinstance(model.get("room_count"), int) else 0):
                state = (state * model.get("multiplier", 0) + model.get("increment", 0)) % model.get("modulus", 1)
                rooms.append({"id": index, "kind": state % 4})
            edges = [[index - 1, index] for index in range(1, len(rooms))]
            return {"rooms": rooms, "edges": edges, "spawns": [room["id"] for room in rooms[:model.get("spawn_count", 0)]]}
        first, repeat, different = generate(42), generate(42), generate(43)
        reachable = {0}
        for left, right in first["edges"]:
            if left in reachable:
                reachable.add(right)
        source_matches_model = all(str(model.get(key)) in code for key in ("multiplier", "increment", "modulus")) and "state % 4" in code
        checks += [("implementation-self-contained", all(token in code for token in ("var state = seed_value", "rooms.append", "edges.append", "spawns.append"))), ("implementation-matches-model", source_matches_model), ("model-valid", model_valid), ("derived-determinism", first == repeat and first != different), ("derived-reachability", len(reachable) == len(first["rooms"])), ("derived-spawn-bound", len(first["spawns"]) == 3)]
    elif skill == "scientific-paper":
        tex = _source(workspace, "paper/main.tex")
        bib = _source(workspace, "sources.bib")
        cited = set(re.findall(r"\\cite\{([^}]+)\}", tex))
        entries = set(re.findall(r"@\w+\{([^,]+),", bib))
        checks += [("implementation-citations-resolve", bool(cited) and cited <= entries), ("implementation-has-method", r"\section{Method}" in tex)]
    elif skill == "scientific-case-study-research":
        report = _source(workspace, "case-study-protocol.md")
        checks += [("traceable-evidence-table", all(token in report for token in ("| Source location | Claim | Finding |", "evidence/interviews.csv:2", "evidence/repository.log:1"))), ("protocol-boundaries", all(token in report for token in ("Unit of analysis", "Triangulation", "Ethics", "Threats")))]
    elif skill == "supabase-workflow":
        policy = _source(workspace, "supabase/migrations/0002_notes_rls.sql").casefold()
        test = _source(workspace, "tests/notes_rls.sql").casefold()
        checks += [("rls-policy-bounded", all(token in policy for token in ("enable row level security", "to authenticated", "using (clinic_id", "with check (clinic_id"))), ("rls-multi-tenant-fixture", "values (1,7),(2,8)" in test and "role authenticated" in test), ("rls-read-assertion", "array[1]" in test and "cross-tenant visibility" in test), ("rls-write-assertion", "cross-tenant write allowed" in test and "insufficient_privilege" in test)]
    elif skill == "terraform-change":
        code = _source(workspace, "change.tf")
        summary = _json(workspace, "plan-summary.json")
        resources = re.findall(r'\bresource\s+"[^"]+"\s+"[^"]+"\s*\{', code)
        without_strings = re.sub(r'"(?:\\.|[^"\\])*"', '""', code)
        braces_balanced = without_strings.count("{") == without_strings.count("}") and without_strings.count("{") > 0
        terraform = shutil.which("terraform")
        syntax_valid = bool(terraform) and subprocess.run([terraform, "fmt", "-check", "change.tf"], cwd=workspace, env={"PATH": os.environ.get("PATH", ""), "CHECKPOINT_DISABLE": "1"}, text=True, capture_output=True, timeout=10, check=False).returncode == 0
        checks += [("implementation-bounded-resource", resources == ['resource "google_storage_bucket" "fixture" {'] and bool(re.search(r"project\s*=\s*var\.project_id", code)) and bool(re.search(r'location\s*=\s*"EU"', code))), ("implementation-balanced-hcl", braces_balanced), ("implementation-valid-formatted-hcl", syntax_valid), ("derived-plan-counts", summary.get("add") == len(resources) and summary.get("change") == 0 and summary.get("destroy") == 0), ("implementation-no-apply", "terraform apply" not in code.casefold())]
    elif skill == "validate-with-zod":
        code = _source(workspace, "src/payload-schema.ts")
        test = _source(workspace, "tests/payload-schema.test.ts")
        checks += [("implementation-validates-fields", all(token in code for token in ("z.object", ".uuid()", ".int()", ".nonnegative()"))), ("implementation-safe-boundary", "input:unknown" in code.replace(" ", "") and "safeParse(input)" in code), ("tests-valid-invalid", all(token in test for token in ("count:1", "id:'bad'", "count:-1", "throw new Error")))]
    return [{"id": f"artifact:{name}", "pass": passed} for name, passed in checks]


def _semantic_checks(skill: str, workspace: Path) -> list[dict[str, object]]:
    checks: list[tuple[str, bool]] = []
    if skill == "game-ai-2d":
        value = _json(workspace, "behavior/guard-state-machine.json")
        checks += [("patrol-chase-lost-cycle", value.get("initial") == "PATROL" and value.get("events") == {"sees_target": "CHASE", "loses_target": "LOST", "timeout": "PATROL"}), ("pause-stable", value.get("paused_state_change") is False), ("telegraph", value.get("telegraph_before_chase") is True)]
    elif skill == "game-art-2d":
        value = _json(workspace, "assets/hero.atlas.json")
        frames = value.get("frames", {})
        frame = next(iter(frames.values()), {}).get("frame", {}) if isinstance(frames, dict) else {}
        meta = value.get("meta", {}) if isinstance(value.get("meta"), dict) else {}
        size = meta.get("size", {}) if isinstance(meta.get("size"), dict) else {}
        image = workspace / "assets/hero.svg" if meta.get("image") == "hero.svg" else None
        bounded = all(isinstance(frame.get(key), int) and frame[key] >= (1 if key in {"w", "h"} else 0) for key in ("x", "y", "w", "h")) and size == {"w": 16, "h": 16} and frame.get("x", 0) + frame.get("w", 0) <= 16 and frame.get("y", 0) + frame.get("h", 0) <= 16
        svg = image.read_text(encoding="utf-8") if image is not None and image.is_file() else ""
        checks += [("named-frame", isinstance(frames, dict) and "hero_idle_0" in frames), ("image-exists", image is not None and image.is_file()), ("image-dimensions", 'width="16"' in svg and 'height="16"' in svg), ("frame-within-image", bounded)]
    elif skill == "game-build-and-release":
        value = _json(workspace, "artifacts/manifest.json")
        files = value.get("files", [])
        artifact = workspace / "artifacts/index.html" if files == ["index.html"] else None
        actual_hash = hashlib.sha256(artifact.read_bytes()).hexdigest() if artifact and artifact.is_file() else None
        smoke = _json(workspace, "artifacts/smoke.json")
        smoke_checks = smoke.get("checks") if isinstance(smoke.get("checks"), list) else []
        html = artifact.read_text(encoding="utf-8") if artifact and artifact.is_file() else ""
        checks += [("artifact-present", artifact is not None and artifact.is_file()), ("sha256-matches-artifact", value.get("sha256") == actual_hash), ("smoke-evidence", smoke.get("entry") == "index.html"), ("smoke-derived", smoke.get("status") == "pass" and {"exists", "contains-game-root"} <= set(smoke_checks) and 'id="game-root"' in html), ("not-deployed", value.get("deployed") is False)]
    elif skill == "game-testing-2d":
        value = _json(workspace, "behavior/attack-results.json")
        checks += [("hit-once", value.get("valid_target_hits") == 1 and value.get("repeat_target_hits") == 0), ("pause-and-restart", value.get("paused_hits") == 0 and value.get("after_scene_restart_hits") == 1)]
    elif skill == "gcloud-operation":
        value = _json(workspace, "operation-plan.json")
        command = value.get("command", [])
        checks += [("explicit-context", value.get("project") == "synthetic-project" and bool(value.get("account")) and bool(value.get("region"))), ("read-only-command", value.get("read_only") is True and isinstance(command, list) and command[:4] == ["gcloud", "run", "services", "describe"])]
    elif skill == "migrate-react-router":
        value = _json(workspace, "behavior/route-results.json")
        checks += [("loader-param", value.get("path") == "/books/:id" and value.get("loader_data", {}).get("bookId") == "42"), ("not-found", value.get("not_found_status") == 404), ("dependency-boundary", value.get("unrelated_dependencies_changed") is False)]
    elif skill == "rust-release":
        value = _json(workspace, "dist/manifest.json")
        artifacts = value.get("artifacts", [])
        artifact = workspace / "dist/fixture" if artifacts == ["fixture"] else None
        actual_hash = hashlib.sha256(artifact.read_bytes()).hexdigest() if artifact and artifact.is_file() else None
        sbom = _json(workspace, "dist/SBOM.spdx.json")
        packages = sbom.get("packages") if isinstance(sbom.get("packages"), list) else []
        checks += [("artifact-present", artifact is not None and artifact.is_file()), ("checksum-matches-artifact", value.get("sha256") == actual_hash), ("sbom", sbom.get("spdxVersion") == "SPDX-2.3" and any(package.get("name") == "fixture" and package.get("versionInfo") == value.get("version") for package in packages if isinstance(package, dict))), ("local-only", value.get("published") is False)]
    elif skill == "scientific-paper":
        value = _json(workspace, "bibliography-report.json")
        checks += [("bibliography-clean", value.get("orphaned") == [] and value.get("malformed") == [] and value.get("validated") is True)]
    elif skill == "terraform-change":
        value = _json(workspace, "plan-summary.json")
        checks += [("bounded-plan", value.get("workspace") == "synthetic" and value.get("add") == 1 and value.get("change") == 0 and value.get("destroy") == 0), ("not-applied", value.get("apply_executed") is False)]
    return [{"id": f"semantic:{name}", "pass": passed} for name, passed in checks]


def verify_workspace(skill: str, workspace: Path) -> dict[str, object]:
    oracle = ORACLES[skill]
    checks: list[dict[str, object]] = []
    for output in oracle["outputs"]:
        relative = output["path"]
        path = workspace / relative
        exists = path.is_file() and bool(path.read_bytes())
        checks.append({"id": f"{relative}:exists", "pass": exists})
        if not exists:
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        folded_raw = raw.casefold()
        for pattern in ("expect(true)", "assert(true)", "todo: implement", "\n    pass\n"):
            checks.append({"id": f"{relative}:non-tautological:{pattern.strip()}", "pass": pattern not in folded_raw})
        if output["format"] == "json":
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                checks.append({"id": f"{relative}:valid-json", "pass": False})
                continue
            checks.append({"id": f"{relative}:valid-json", "pass": isinstance(parsed, dict)})
            for key in output.get("keys", []):
                checks.append({"id": f"{relative}:key:{key}", "pass": isinstance(parsed, dict) and key in parsed})
            for key, expected in output.get("equals", {}).items():
                checks.append({"id": f"{relative}:equals:{key}", "pass": isinstance(parsed, dict) and parsed.get(key) == expected})
        else:
            folded = raw.casefold()
            for token in output.get("contains", []):
                checks.append({"id": f"{relative}:contains:{token}", "pass": str(token).casefold() in folded})
            for token in output.get("forbids", []):
                checks.append({"id": f"{relative}:forbids:{token}", "pass": str(token).casefold() not in folded})
    if all(item["pass"] for item in checks):
        try:
            checks.extend(_artifact_checks(skill, workspace))
        except Exception as exc:
            checks.append({"id": f"artifact:fail-closed:{type(exc).__name__}", "pass": False})
    if all(item["pass"] for item in checks):
        try:
            checks.extend(_semantic_checks(skill, workspace))
        except Exception as exc:
            checks.append({"id": f"semantic:fail-closed:{type(exc).__name__}", "pass": False})
    failures = [item["id"] for item in checks if not item["pass"]]
    return {"status": "fail" if failures else "pass", "checks": checks, "failures": failures}
