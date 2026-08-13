from __future__ import annotations


def text(path: str, sample: str, *contains: str, forbids: tuple[str, ...] = ()) -> dict[str, object]:
    return {"path": path, "format": "text", "contains": list(contains), "forbids": list(forbids), "sample": sample}


def json_file(path: str, sample: str, *keys: str) -> dict[str, object]:
    return {"path": path, "format": "json", "keys": list(keys), "sample": sample}


PRODUCT_UI_UX_EVIDENCE = '{"runtime_available":false,"analytics_available":false,"research_available":false,"scenarios":[{"id":"saas-onboarding","domain":"SaaS","platform":"web","actor":"invited member","evidence":"Invitation opens an empty workspace; a five-dialog tour appears before the task; the member cannot dismiss step three."},{"id":"ecommerce-checkout","domain":"e-commerce","platform":"web-mobile","actor":"guest shopper","evidence":"Guest checkout exists; shipping and tax appear only after payment details; a declined payment clears the address."},{"id":"cms-editorial","domain":"CMS","platform":"web","actor":"author and editor","evidence":"Autosave has no visible state; preview has no locale label; rejected content returns without reviewer reason."},{"id":"crm-mobile-capture","domain":"CRM","platform":"mobile","actor":"field representative","evidence":"Contact update requires nine fields; offline save shows success; reconnect conflict overwrites the server value."},{"id":"erp-purchase-approval","domain":"ERP","platform":"web","actor":"purchase approver","evidence":"A 24-column table supports bulk approval; currency and company are off-screen; ineligible locked rows remain selected and failure is generic."}]}\n'

PRODUCT_UI_UX_SAMPLE = """# Product UI/UX audit

## Scope and evidence boundary

- Verified fixture evidence: five supplied scenario descriptions in `product-evidence.json`.
- Runtime verification: not performed; the interface is not executable.
- Supplied analytics and user research: none.
- Heuristics: task continuity, visible system status, error prevention, recovery, and inclusive operation.
- Hypotheses: proposed effects require representative user and runtime validation.
- Limitation: browser, device, responsive, keyboard, touch, screen reader, performance, and accessibility conformance remain unverified.

## Prioritized findings

| Priority | Scenario | Verified evidence | Risk | Decision direction |
| --- | --- | --- | --- | --- |
| P0 | CRM mobile capture | Offline save reports success and reconnect overwrites the server value. | Silent data loss and false status. | Distinguish pending, synced, failed, and conflicted states; require explicit conflict resolution. |
| P0 | E-commerce checkout | Declined payment clears the address. | Recovery cost and checkout abandonment. | Preserve non-sensitive fields and return focus to an actionable payment error. |
| P0 | ERP purchase approval | Locked rows remain selected and bulk failure is generic. | Ineligible or ambiguous financial action. | Preview eligible scope and report row-level outcomes. |
| P1 | SaaS onboarding | Five dialogs precede the task and step three cannot be dismissed. | Blocked activation and obstructed cancellation. | Teach in context and preserve skip/resume. |
| P1 | CMS editorial | Autosave, locale preview, and rejection reason are not visible. | Lost work or incorrect publication. | Expose save state, locale, and reviewer reason. |

## Complete state model

For each scenario verify entry, primary path, alternative path, loading, empty state, validation error, system error and recovery, lack of permission, unavailable or offline state, confirmation, cancellation, destructive or financial consequence, success, and next step.

## Experience performance boundary

No field measurement or laboratory measurement was supplied. For each critical task, a later check must identify the user action, first acknowledgement, usable state, completion, and recovery under representative browser, device, connection, data-volume, startup, and resume conditions. Core Web Vitals, TTID, TTFD, hangs, and hitches are platform signals rather than proof of task usability.

This audit owns observable loading, pending, stale, offline, timeout, conflict, success, and failure behavior. Profiling is required before assigning a technical root cause. Bundle, main-thread, API, database, rendering, memory, and energy optimization remain engineering performance work and are not authorized by this audit.

## SaaS onboarding

Decision: open on the first real workspace task, show role and workspace context, replace the dialog sequence with contextual guidance, and allow skip and resume. Empty workspace guidance must name the first useful action and permission limits.

Acceptance: an invited member can reach and complete the first task without completing a tour; skip persists; no-permission and invite-expired states explain recovery.

## E-commerce checkout

Decision: show shipping, tax, currency, and final total before payment; preserve address and cart after a decline; keep guest checkout; reconcile an unknown payment result before allowing a retry.

Acceptance: a declined payment retains non-sensitive data and exposes focusable error guidance; duplicate submission cannot create a second order; confirmation names authoritative order state.

## CMS editorial flow

Decision: show saving, saved, failed, and offline states; label preview locale/channel; return rejected content with reviewer reason and next action; keep publish permission explicit.

Acceptance: an author recovers an interrupted draft, an editor can return with a reason, and preview/publish expose locale, version, actor, and status.

## CRM mobile capture

Decision: stage required capture fields, keep additional detail available, label local pending state honestly, and resolve reconnect conflicts without silent overwrite.

Acceptance: keyboard and touch users can save minimum credible data offline; reconnect produces synced or conflicted, never false success; server and local values are reviewable before resolution.

## ERP purchase approval

Decision: retain dense comparison while pinning identity, company, currency, amount, and eligibility; show selected scope; exclude or explain locked rows before approval; report partial results per row.

Acceptance: keyboard-only approval exposes all critical columns and focus; bulk confirmation states eligible count and financial scope; locked/no-permission/closed-period rows remain unchanged and get actionable outcomes.

## Accessibility and human verification

Verify visible focus, semantic names and table relationships, non-color status, screen-reader announcements, zoom/text scaling, target spacing, reduced motion, localization expansion, and error recovery on supported platforms. Automated checks may assist but cannot establish WCAG conformance or usability. Representative human review remains required.
"""

PRODUCT_PERFORMANCE_EVIDENCE = '{"field_data_available":false,"physical_devices_available":false,"product_executable_available":false,"production_load_authorized":false,"existing_budgets":{"android_ttfd_ms":2500},"scenarios":[{"id":"web-lcp-critical-path","platform":"web","metric":"LCP_ms","baseline":[3260,3180,3340,3210,3300],"candidate":[2210,2280,2190,2240,2260],"profile_evidence":"The LCP image is discovered only after hydration and waits behind a main-thread task.","functional_equivalence":true},{"id":"web-long-task-input","platform":"web","metric":"interaction_latency_ms","baseline":[410,395,430,405,420],"candidate":[175,182,169,178,180],"profile_evidence":"A 286 ms JavaScript task blocks the main thread across the interaction.","functional_equivalence":true},{"id":"web-layout-instability","platform":"web","metric":"CLS","baseline":[0.31,0.29,0.34,0.30,0.32],"candidate":[0.05,0.04,0.06,0.05,0.05],"profile_evidence":"Layout-shift attribution identifies an image without reserved dimensions.","functional_equivalence":true},{"id":"android-startup","platform":"android","metric":"startup_ms","baseline":{"TTID":[720,705,735,710,725],"TTFD":[3120,3050,3180,3090,3150]},"candidate":{"TTID":[650,640,660,645,655],"TTFD":[2180,2210,2150,2190,2170]},"profile_evidence":"Perfetto shows synchronous database deserialization on the main thread before reportFullyDrawn.","functional_equivalence":true},{"id":"android-jank-anr","platform":"android","metric":"render_and_anr","baseline":{"slow_frame_rate":[0.24,0.22,0.25,0.23,0.24],"anr_count":3},"candidate":{"slow_frame_rate":[0.08,0.07,0.09,0.08,0.08],"anr_count":0},"profile_evidence":"Perfetto ties frozen frames and the input-dispatch ANR to blocking storage I/O on the main thread.","functional_equivalence":true},{"id":"ios-launch-hang-hitch","platform":"ios","metric":"launch_and_responsiveness","baseline":{"launch_ms":[1840,1790,1880,1810,1860],"hang_ms":[420,390,440,410,430],"hitch_ms_per_s":[38,36,40,37,39]},"candidate":{"launch_ms":[1310,1280,1340,1290,1320],"hang_ms":[120,110,130,115,125],"hitch_ms_per_s":[12,11,13,12,12]},"profile_evidence":"Instruments attributes launch and main-run-loop blocking to synchronous JSON decoding; the Hitches track identifies repeated SwiftUI updates.","functional_equivalence":true},{"id":"mobile-memory-lifecycle","platform":"mobile","metric":"retained_memory_mb","baseline":[122,151,181,212,243],"candidate":[124,128,126,129,127],"profile_evidence":"Heap diffs retain one screen graph per background/foreground cycle through an observer.","functional_equivalence":true},{"id":"cross-platform-react-native","platform":"react-native","metric":"navigation_latency_ms","baseline":{"android_simulator":[510,495,525,505,515],"ios_simulator":[440,455,435,450,445]},"candidate":null,"profile_evidence":"Shared-layer traces show repeated serialization, but only simulators were available.","functional_equivalence":null},{"id":"functional-equivalence-mutant","platform":"web","metric":"task_ms","baseline":[900,880,920,895,905],"candidate":[210,205,215,208,212],"profile_evidence":"The candidate skips validation work.","functional_equivalence":false},{"id":"missing-measurement","platform":"ios","metric":null,"baseline":null,"candidate":null,"profile_evidence":null,"functional_equivalence":null}]}\n'

PRODUCT_PERFORMANCE_SAMPLE = """# Product performance analysis

## Scope and evidence boundary

- Verified input: synthetic laboratory distributions and bounded profile summaries in `performance-evidence.json`.
- Baseline: repeated samples under the fixture conditions.
- Comparison method: median and p95; no conclusion uses a best execution.
- Field improvement: not claimed; no field data exists.
- Physical-device verification: unavailable; simulator evidence is not hardware proof.
- Browser/runtime execution: unavailable; supplied summaries were analyzed without rerunning the product.
- Production load: not executed and not authorized.
- Code changes: none; this is diagnosis-only work.
- Budget unchanged: 2500 ms for Android TTFD.
- Skeleton is not an optimization and cannot establish a technical improvement.

## Prioritized diagnosis

### P0 — functional-equivalence-mutant

The candidate is faster only because it skips validation. Functional equivalence: failed; candidate rejected. Its timing cannot be accepted as an optimization.

### P0 — android-jank-anr

Measured: repeated slow-frame rates and ANR counts improve in the candidate summary. Supported causal inference: Perfetto connects frozen frames and the input-dispatch ANR to blocking storage I/O on the main thread. Re-run the same release-like journey and preserve storage, lifecycle, cancellation, and output behavior.

### P0 — mobile-memory-lifecycle

Measured: retained memory grows on every lifecycle cycle in the baseline and stabilizes in the candidate. Supported causal inference: heap diffs retain one screen graph per background/foreground cycle through an observer. Verify cleanup, restoration, and process recreation.

### P1 — web-lcp-critical-path

Measured: the repeated LCP distribution improves. Supported causal inference: the critical rendering path delays LCP resource discovery until hydration and then behind main-thread work. Verify discovery, priority, rendering, output, and field behavior separately.

### P1 — web-long-task-input

Measured: the interaction distribution improves. Supported causal inference: a 286 ms long task creates main-thread contention across input and next paint. Preserve ordering, cancellation, and result equivalence when moving or splitting work.

### P1 — web-layout-instability

Measured: the CLS distribution improves. Supported causal inference: layout-shift attribution identifies the image without reserved dimensions. Verify responsive rendering and accessibility rather than treating CLS alone as usability proof.

### P1 — android-startup

Measured: TTID and TTFD are reported separately and both repeated distributions improve; the TTFD candidate is within the unchanged 2500 ms budget. Supported causal inference: Perfetto places synchronous deserialization on the main thread before `reportFullyDrawn`. Verify cold, warm, and hot startup with controlled compilation state.

### P1 — ios-launch-hang-hitch

Measured: repeated launch, hang, and hitch distributions improve. Supported causal inference: Instruments attributes launch and main-run-loop blocking to synchronous decoding and the Hitches track identifies repeated SwiftUI updates. Verify launch, first usable state, frame pacing, memory, and energy separately.

### P2 — cross-platform-react-native

Measured limitation: Android and iOS simulator distributions show a slow navigation path, and shared-layer traces suggest repeated serialization. Root cause remains a hypothesis because native and shared costs were not verified on physical devices. Measure Android and iOS release builds separately across JS, UI/main, native-module, render, memory, and interop paths.

### P2 — missing-measurement

No metric, unit, baseline, executable product, or profile is supplied. Root cause: unsupported without profile. Do not optimize. Establish the task start/end, supported device and OS, release build, cache/data/network state, cold/warm/hot path, repeated baseline distribution, and a discriminating trace before proposing a causal change.

## Regression and integrity criteria

Accept a candidate only when the original repeated scenario improves without relaxed thresholds and functional output, validation, accessibility, permissions, security, privacy, consistency, lifecycle, memory, energy, network, and storage behavior remain equivalent. A no-op, a best-run-only comparison, a false field claim, a relaxed budget, or a faster wrong result must fail.

## Limitations and next evidence

Field, browser/runtime, assistive-technology, and representative physical-device verification remain unavailable. The supplied profile summaries support bounded laboratory inferences only. Collect privacy-reviewed field segmentation after an authorized release and repeat the laboratory scenarios on modest supported Android and iOS devices before claiming population improvement.
"""


# Independent, executable oracles for the controlled fixtures. Samples are
# calibration mutants for unit tests; they are never copied into provider workspaces.
ORACLES: dict[str, dict[str, object]] = {
    "ci-ai-eng": {
        "inputs": {"ai-contract.json": '{"prompts":"v3","tool_schema":"v2","eval_corpus":"fixture-v1","provider_calls_authorized":false}\n'},
        "outputs": [
            text(".github/workflows/ai.yml", "name: AI CI\non: [push, pull_request]\npermissions: read-all\njobs:\n  verify:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: python -m unittest\n      - run: python -m evals.runner --dry-run\n", "AI CI", "pull_request", "permissions: read-all", "ubuntu-latest", "actions/checkout@v4", "python -m unittest", "--dry-run", forbids=("--execute", "secrets.", "deploy", "publish")),
            json_file("eval-plan.json", '{"suite":"full","execute":false,"upper_bound_calls":0,"credentials_required":false,"incomplete_is_green":false}\n', "suite", "execute", "upper_bound_calls", "credentials_required", "incomplete_is_green"),
        ],
    },
    "ci-android": {
        "inputs": {"settings.gradle.kts": 'rootProject.name = "fixture"\n', "gradlew": "#!/bin/sh\nexit 0\n"},
        "outputs": [text(".github/workflows/android.yml", "name: Android CI\non: [push, pull_request]\njobs:\n  verify:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-java@v4\n        with: {distribution: temurin, java-version: '21'}\n      - uses: gradle/actions/setup-gradle@v4\n      - run: ./gradlew lint test assembleDebug\n", "runs-on", "checkout@v4", "setup-java@v4", "setup-gradle@v4", "gradlew", "lint", "test", "assemble", forbids=("publish", "upload"))],
    },
    "ai-eng-rag-pipeline": {
        "inputs": {"data/documents.json": '[{"id":"a-1","tenant":"a","score":0.9,"text":"alpha"},{"id":"a-2","tenant":"a","score":0.8,"text":"alpha two"},{"id":"b-1","tenant":"b","score":0.95,"text":"beta"},{"id":"b-2","tenant":"b","score":0.7,"text":"beta two"}]\n'},
        "outputs": [text("src/retrieval.py", "def retrieve(collection, tenant_id, query):\n    return collection.query(where={'tenant': tenant_id}, query_texts=[query], include=['metadatas', 'distances'])\n", "tenant_id", "where", "query", "distances"), json_file("behavior/retrieval-results.json", '{"tenant_a_query":{"returned_tenants":["a","a"],"stable_ids":["a-1","a-2"]},"tenant_b_query":{"returned_tenants":["b","b"],"stable_ids":["b-1","b-2"]},"cross_tenant_leak":false}\n', "tenant_a_query", "tenant_b_query", "cross_tenant_leak")],
    },
    "game-dev-2d-ai": {
        "inputs": {"project.godot": "[application]\nconfig/name=\"AI fixture\"\n"},
        "outputs": [text("src/guard_ai.gd", "enum State { PATROL, CHASE, LOST }\nvar state = State.PATROL\nvar paused = false\nvar telegraph_ready = false\nfunc handle_event(event):\n    if paused:\n        return state\n    if event == \"sees_target\":\n        telegraph_ready = true\n        state = State.CHASE\n    elif event == \"loses_target\":\n        state = State.LOST\n    elif event == \"timeout\":\n        state = State.PATROL\n    return state\nfunc pause():\n    paused = true\n", "PATROL", "CHASE", "LOST", "pause"), json_file("behavior/guard-state-machine.json", '{"initial":"PATROL","events":{"sees_target":"CHASE","loses_target":"LOST","timeout":"PATROL"},"paused_state_change":false,"telegraph_before_chase":true}\n', "initial", "events", "paused_state_change", "telegraph_before_chase")],
    },
    "game-dev-2d-art": {
        "inputs": {"assets/source/hero.svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" shape-rendering=\"crispEdges\"><rect x=\"4\" y=\"4\" width=\"8\" height=\"8\" fill=\"#ff00ff\"/></svg>\n"},
        "outputs": [text("assets/hero.svg", "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" shape-rendering=\"crispEdges\"><rect x=\"4\" y=\"4\" width=\"8\" height=\"8\" fill=\"#ff00ff\"/></svg>\n", "width=\"16\"", "height=\"16\"", "crispEdges"), json_file("assets/hero.atlas.json", '{"frames":{"hero_idle_0":{"frame":{"x":0,"y":0,"w":16,"h":16}}},"meta":{"image":"hero.svg","size":{"w":16,"h":16}}}\n', "frames", "meta"), text("art-qa.md", "Dimensions: 16x16\nPalette: bounded\nSource: assets/source/hero.svg\nAtlas frame: hero_idle_0\n", "Dimensions", "Palette", "Source: assets/source/hero.svg", "hero_idle_0")],
    },
    "game-dev-2d-audio": {
        "inputs": {"package.json": '{"dependencies":{"phaser":"3.90.0"}}\n'},
        "outputs": [text("src/audio-owner.ts", "export class AudioOwner { private static owner:AudioOwner; muted=false; current='menu'; disposedPlayers=0; static get(){ return this.owner ??= new AudioOwner() } setMuted(value:boolean){ this.muted=value } crossfade(next:string){ const previous=this.current; this.current=next; this.disposedPlayers += previous===next ? 0 : 1; return {previous,next} } destroy(){ this.current='disposed' } }\n", "AudioOwner", "muted", "crossfade", "destroy"), text("tests/audio-owner.test.ts", "import { AudioOwner } from '../src/audio-owner'\nconst first=AudioOwner.get(), second=AudioOwner.get(); if(first!==second) throw new Error('owner')\nfirst.setMuted(true); first.crossfade('battle'); if(!second.muted||second.disposedPlayers!==1) throw new Error('lifecycle')\n", "AudioOwner.get", "setMuted(true)", "crossfade", "disposedPlayers", "throw new Error")],
    },
    "release-game-dev-2d": {
        "inputs": {"package.json": '{"scripts":{"build":"vite build"},"dependencies":{"phaser":"3.90.0"}}\n'},
        "outputs": [text("artifacts/index.html", "<div id=\"game-root\"></div>\n", "game-root"), json_file("artifacts/manifest.json", '{"version":"0.0.0-fixture","files":["index.html"],"sha256":"d2e3dd15abcb607f81e468d9a91cb490383dd7e28c1677208dc146a22a1a2e2b","deployed":false}\n', "version", "files", "sha256", "deployed"), json_file("artifacts/smoke.json", '{"entry":"index.html","status":"pass","checks":["exists","contains-game-root"]}\n', "entry", "status", "checks")],
    },
    "game-dev-2d-feel": {
        "inputs": {"project.godot": "[application]\nconfig/name=\"Feel fixture\"\n"},
        "outputs": [text("src/jump_feedback.gd", "func apply_jump_feedback(reduced_motion: bool):\n    var shake = 0 if reduced_motion else 2\n    return shake\n", "jump", "reduced_motion", "shake"), text("tests/jump_feedback.test.gd", "assert(apply_jump_feedback(false) == 2)\nassert(apply_jump_feedback(true) == 0)\n", "false", "== 2", "true", "== 0")],
    },
    "game-dev-2d-performance": {
        "inputs": {"src/update.ts": "export const update = (items:number[]) => items.map(x => x * 2)\n"},
        "outputs": [text("src/update-optimized.ts", "export function updateOptimized(items:number[]){ const output=[]; for (const item of items) output.push(item*2); return output }\n", "updateOptimized", "output", "return"), text("tests/update-parity.test.ts", "import { update } from '../src/update.ts'\nimport { updateOptimized } from '../src/update-optimized.ts'\nconst input=[1,2,3]\nif(JSON.stringify(update(input))!==JSON.stringify(updateOptimized(input))) throw new Error('parity')\n", "update", "updateOptimized", "JSON.stringify", "throw new Error")],
    },
    "game-dev-2d-save-progression": {
        "inputs": {"project.godot": "[application]\nconfig/name=\"Save fixture\"\n"},
        "outputs": [text("src/save_store.gd", "const CURRENT_VERSION = 2\nfunc migrate(data):\n    if data.version > CURRENT_VERSION:\n        return {\"error\": \"future-version\"}\n    var migrated = data.duplicate(true)\n    if migrated.version == 1:\n        migrated.version = 2\n    return migrated\nfunc atomic_write(temp_path, final_path, payload):\n    var file = FileAccess.open(temp_path, FileAccess.WRITE)\n    file.store_string(payload)\n    file.flush()\n    file.close()\n    return DirAccess.rename_absolute(temp_path, final_path)\nfunc load_with_backup(primary, backup):\n    return primary if primary != null else backup\n", "CURRENT_VERSION", "migrate", "future-version", "duplicate", "atomic", "temp", "flush", "rename_absolute", "backup"), text("tests/save_store.test.gd", "assert(migrate({\"version\":1,\"coins\":7}) == {\"version\":2,\"coins\":7})\nassert(migrate({\"version\":3}).error == \"future-version\")\nassert(load_with_backup(null, {\"version\":2}).version == 2)\nassert(atomic_write(\"save.tmp\", \"save.json\", \"{}\") == OK)\n", "coins", "future-version", "null", "backup", "save.tmp", "save.json")],
    },
    "game-dev-2d-testing": {
        "inputs": {"src/attack-window.mjs": "export class AttackWindow {\n  constructor(){ this.seen=new Set(); this.paused=false }\n  attack(id){ if(this.paused || this.seen.has(id)) return false; this.seen.add(id); return true }\n  setPaused(value){ this.paused=value }\n  restart(){ this.seen.clear(); this.paused=false }\n}\n"},
        "outputs": [text("tests/attack-window.test.mjs", "import { AttackWindow } from '../src/attack-window.mjs'\nconst window = new AttackWindow()\nif(window.attack('target') !== true) throw new Error('first hit')\nif(window.attack('target') !== false) throw new Error('repeat hit')\nwindow.setPaused(true)\nif(window.attack('other') !== false) throw new Error('paused hit')\nwindow.restart()\nif(window.attack('target') !== true) throw new Error('restart hit')\n", "AttackWindow", "attack('target')", "setPaused(true)", "restart()", "throw new Error", forbids=("expect(true)", "assert(true)")), json_file("behavior/attack-results.json", '{"valid_target_hits":1,"repeat_target_hits":0,"paused_hits":0,"after_scene_restart_hits":1}\n', "valid_target_hits", "repeat_target_hits", "paused_hits", "after_scene_restart_hits")],
    },
    "game-dev-2d-ui-accessibility": {
        "inputs": {"package.json": '{"dependencies":{"phaser":"3.90.0"}}\n'},
        "outputs": [text("src/pause-menu.ts", "export const pauseMenu={ items:['resume','settings','quit'], initialFocus:'resume', accessibleName:'Pause menu', restoreFocus:true, touchTarget:44, layout:{maxWidthPercent:100,wrap:true,overflow:'auto'}, reducedMotionPreservesState:true }\n", "items", "initialFocus", "accessibleName", "restoreFocus", "touchTarget", "maxWidthPercent", "wrap", "overflow", "reducedMotionPreservesState"), text("tests/pause-menu.test.ts", "import { pauseMenu } from '../src/pause-menu.ts'\nif(pauseMenu.items.join(',')!=='resume,settings,quit') throw new Error('order')\nif(pauseMenu.touchTarget<44||!pauseMenu.restoreFocus) throw new Error('a11y')\nif(!pauseMenu.layout.wrap||pauseMenu.layout.overflow!=='auto') throw new Error('reflow')\nif(!pauseMenu.reducedMotionPreservesState) throw new Error('reduced motion')\n", "order", "a11y", "reflow", "reduced motion", "throw new Error")],
    },
    "game-dev-2d-gameplay": {
        "inputs": {"package.json": '{"dependencies":{"phaser":"3.90.0"}}\n'},
        "outputs": [text("src/dash.ts", "export class Dash { cooldown=250; active=false; remaining=0; start(){ if(this.remaining>0) return false; this.active=true; this.remaining=this.cooldown; return true } collide(){this.active=false} pause(elapsed:number){return Math.max(0,this.remaining-elapsed)} restart(){this.active=false;this.remaining=0} }\n", "Dash", "cooldown", "start", "remaining", "collide", "pause", "restart"), text("tests/dash.test.ts", "import { Dash } from '../src/dash.ts'\nconst dash=new Dash(); if(!dash.start()||dash.start()) throw new Error('cooldown')\ndash.collide(); if(dash.active) throw new Error('collision')\nif(dash.pause(100)!==150) throw new Error('pause')\ndash.restart(); if(dash.active||dash.remaining!==0) throw new Error('restart')\n", "cooldown", "collision", "pause", "restart", "throw new Error")],
    },
    "cloud-ops": {
        "inputs": {"context.json": '{"account":"fixture@example.invalid","project":"synthetic-project","region":"europe-west1","allow_remote_mutation":false}\n'},
        "outputs": [json_file("operation-plan.json", '{"account":"fixture@example.invalid","project":"synthetic-project","region":"europe-west1","command":["gcloud","run","services","describe","fixture","--account","fixture@example.invalid","--project","synthetic-project","--region","europe-west1"],"read_only":true}\n', "account", "project", "region", "command", "read_only")],
    },
    "ci-go": {
        "inputs": {"go.mod": "module example.invalid/fixture\n\ngo 1.24\n"},
        "outputs": [text(".github/workflows/go.yml", "name: Go CI\non: [push, pull_request]\njobs:\n  verify:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-go@v5\n        with: {go-version: '1.24'}\n      - run: gofmt -w . && git diff --exit-code\n      - run: go vet ./...\n      - run: go test -race ./...\n      - run: go build ./...\n", "runs-on", "checkout@v4", "setup-go@v5", "gofmt", "go vet", "go test", "-race", "go build", forbids=("publish",))],
    },
    "ai-eng-agent-design": {
        "inputs": {"requirements.txt": "langgraph==0.0.0-fixture\n"},
        "outputs": [text("src/graph.py", "from typing import TypedDict\nfrom langgraph.graph import StateGraph, START, END\nfrom langgraph.checkpoint.memory import MemorySaver\nfrom langgraph.types import interrupt\nclass State(TypedDict):\n    approved: bool\ndef collect(state: State): return state\ndef approval(state: State): return {**state, 'approved': bool(interrupt({'question':'Approve write?'}))}\ndef write(state: State): return state\ndef route(state: State): return 'write' if state['approved'] else END\nbuilder = StateGraph(State)\nbuilder.add_node('collect', collect)\nbuilder.add_node('approval', approval)\nbuilder.add_node('write', write)\nbuilder.add_edge(START, 'collect')\nbuilder.add_edge('collect', 'approval')\nbuilder.add_conditional_edges('approval', route, {'write':'write', END:END})\nbuilder.add_edge('write', END)\ngraph = builder.compile(checkpointer=MemorySaver())\n", "StateGraph", "TypedDict", "interrupt", "add_node", "add_conditional_edges", "checkpointer"), json_file("behavior/graph-results.json", '{"initial":"collect","nodes":["collect","approval","write"],"route_unapproved":"END","route_approved":"write","checkpoint":"memory","resume_node":"approval","interrupt_before_write":true}\n', "initial", "nodes", "route_unapproved", "route_approved", "checkpoint", "resume_node", "interrupt_before_write")],
    },
    "ai-eng-llm-integration": {
        "inputs": {"src/endpoint.ts": "export async function ask(input:string){ return fetch('https://example.invalid',{method:'POST',body:input}) }\n"},
        "outputs": [text("llm-review.md", "P1 src/endpoint.ts:1 — private input crosses a provider boundary.\nRetry: bound retries and timeout.\nAuthority: tools require explicit scope.\nPatch: see remediation.diff; it redacts input and surfaces provider failures.\n", "src/endpoint.ts:1", "private", "Retry", "Authority", "remediation.diff"), text("remediation.diff", "--- a/src/endpoint.ts\n+++ b/src/endpoint.ts\n@@ -1 +1 @@\n-export async function ask(input:string){ return fetch('https://example.invalid',{method:'POST',body:input}) }\n+export async function ask(input:string){ const redacted='[redacted]'; return fetch('https://example.invalid',{method:'POST',body:redacted}) }\n", "--- a/src/endpoint.ts", "+++ b/src/endpoint.ts", "@@ -1 +1 @@", "redacted")],
    },
    "web-state-zustand": {
        "inputs": {"package.json": '{"dependencies":{"zustand":"5.0.0"}}\n'},
        "outputs": [text("src/cart-store.ts", "import { create } from 'zustand'\nimport { persist } from 'zustand/middleware'\ntype Item={price:number}; type CartState={items:Item[];add:(item:Item)=>void;reset:()=>void}\nexport const useCartStore=create<CartState>()(persist((set)=>({items:[],add:(item)=>set(s=>({items:[...s.items,item]})),reset:()=>set({items:[]})}),{name:'cart-v1',partialize:s=>({items:s.items})}))\nexport const selectTotal=(s:CartState)=>s.items.reduce((sum,item)=>sum+item.price,0)\n", "zustand", "create", "persist", "partialize", "selectTotal", "reset"), text("tests/cart-store.test.ts", "import { selectTotal, useCartStore } from '../src/cart-store'\nif(selectTotal({items:[],add(){},reset(){}})!==0) throw new Error('initial total')\nuseCartStore.getState().add({price:12})\nif(selectTotal(useCartStore.getState())!==12) throw new Error('derived total')\nuseCartStore.getState().reset()\nif(useCartStore.getState().items.length!==0) throw new Error('reset')\n", "selectTotal", "getState", "add", "reset", "throw new Error")],
    },
    "web-state-xstate": {
        "inputs": {"package.json": '{"dependencies":{"xstate":"5.0.0"}}\n'},
        "outputs": [text("src/checkout-machine.ts", "import { createMachine } from 'xstate'\ntype Event={type:'START'}|{type:'RETRY'}|{type:'CANCEL'}\nexport const checkoutMachine=createMachine({types:{} as {events:Event},initial:'idle',states:{idle:{on:{START:'submitting'}},submitting:{on:{RETRY:'submitting',CANCEL:'cancelled'}},cancelled:{}}})\n", "xstate", "createMachine", "events:Event", "initial", "RETRY", "CANCEL"), text("tests/checkout-machine.test.ts", "import { createActor } from 'xstate'\nimport { checkoutMachine } from '../src/checkout-machine'\nconst invalid=createActor(checkoutMachine).start(); invalid.send({type:'RETRY'}); if(invalid.getSnapshot().value!=='idle') throw new Error('invalid event')\nconst actor=createActor(checkoutMachine).start()\nactor.send({type:'START'}); if(actor.getSnapshot().value!=='submitting') throw new Error('start')\nactor.send({type:'RETRY'}); actor.send({type:'CANCEL'}); if(actor.getSnapshot().value!=='cancelled') throw new Error('cancel')\n", "createActor", "invalid event", "idle", "send", "getSnapshot", "submitting", "cancelled", "throw new Error")],
    },
    "writing-academic-edit": {
        "inputs": {"manuscript.md": "---\ntitle: Synthetic paper\nauthor: Fixture Author\n---\n# Synthetic paper\n\nClaim without evidence.\n"},
        "mutable_inputs": ["manuscript.md"],
        "outputs": [text("manuscript.md", "---\ntitle: Synthetic paper\nauthor: Fixture Author\n---\n# Synthetic paper\n\nThe draft makes a claim without supporting evidence.\n", "title: Synthetic paper", "author: Fixture Author", "# Synthetic paper", "claim", "supporting evidence", forbids=("Claim without evidence.",))],
    },
    "database-postgresql": {
        "inputs": {"schema.sql": "create table visits(id bigint primary key, clinic_id bigint not null, occurred_at timestamptz not null);\n", "query.sql": "select * from visits where clinic_id = 7 order by occurred_at desc;\n"},
        "outputs": [text("review.sql", "EXPLAIN (ANALYZE, BUFFERS) SELECT id, occurred_at FROM visits WHERE clinic_id = 7 ORDER BY occurred_at DESC;\nCREATE INDEX CONCURRENTLY IF NOT EXISTS visits_clinic_occurred_idx ON visits (clinic_id, occurred_at DESC);\n", "EXPLAIN", "BUFFERS", "clinic_id", "INDEX CONCURRENTLY"), text("postgres-review.md", "Lock risk: use CONCURRENTLY outside a transaction.\nRollback: DROP INDEX CONCURRENTLY visits_clinic_occurred_idx.\nValidate on production-like statistics before execution.\n", "Lock", "Rollback", "statistics", "before execution")],
    },
    "game-dev-2d-procedural-generation": {
        "inputs": {"project.godot": "[application]\nconfig/name=\"Procgen fixture\"\n"},
        "outputs": [text("src/room_generator.gd", "func generate(seed_value):\n    var state = seed_value\n    var rooms = []\n    for index in range(6):\n        state = (state * 1664525 + 1013904223) % 4294967296\n        rooms.append({\"id\": index, \"kind\": state % 4})\n    var edges = []\n    for index in range(1, rooms.size()):\n        edges.append([index - 1, index])\n    var spawns = []\n    for index in range(min(3, rooms.size())):\n        spawns.append(rooms[index].id)\n    return {\"rooms\": rooms, \"edges\": edges, \"spawns\": spawns}\n", "seed_value", "1664525", "1013904223", "4294967296", "state % 4", "rooms.append", "edges", "index - 1", "spawns.append", "min(3"), json_file("behavior/generator-model.json", '{"algorithm":"lcg","multiplier":1664525,"increment":1013904223,"modulus":4294967296,"room_count":6,"backbone":"previous-to-current","spawn_count":3}\n', "algorithm", "multiplier", "increment", "modulus", "room_count", "backbone", "spawn_count")],
    },
    "ci-python": {
        "inputs": {"pyproject.toml": "[project]\nname='fixture'\nversion='0.0.0'\n"},
        "outputs": [text(".github/workflows/python.yml", "name: Python CI\non: [push, pull_request]\njobs:\n  verify:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: astral-sh/setup-uv@v6\n      - run: uv sync --frozen\n      - run: uv run ruff check .\n      - run: uv run pyright\n      - run: uv run pytest\n      - run: uv build\n", "runs-on", "checkout@v4", "setup-uv@v6", "uv sync --frozen", "ruff", "pyright", "pytest", "uv build", forbids=("publish", "upload"))],
    },
    "ci-rust": {
        "inputs": {"Cargo.toml": "[package]\nname='fixture'\nversion='0.0.0'\nedition='2024'\n"},
        "outputs": [text(".github/workflows/rust.yml", "name: Rust CI\non: [push, pull_request]\njobs:\n  verify:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: dtolnay/rust-toolchain@1.88.0\n      - uses: EmbarkStudios/cargo-deny-action@v2\n      - run: cargo fmt --check\n      - run: cargo clippy -- -D warnings\n      - run: cargo test\n      - run: cargo build --release\n", "runs-on", "checkout@v4", "rust-toolchain@1.88.0", "cargo-deny-action@v2", "cargo fmt", "cargo clippy", "-D warnings", "cargo test", "cargo build", forbids=("publish", "upload"))],
    },
    "release-rust": {
        "inputs": {"Cargo.toml": "[package]\nname='fixture'\nversion='1.2.3'\nedition='2024'\n"},
        "outputs": [text("dist/fixture", "synthetic rust artifact\n", "synthetic rust artifact"), json_file("dist/manifest.json", '{"version":"1.2.3","artifacts":["fixture"],"sha256":"02ff43841729efa5831b91d950d4224015fae05d1087169c28544e2d1198bdd9","published":false}\n', "version", "artifacts", "sha256", "published"), json_file("dist/SBOM.spdx.json", '{"spdxVersion":"SPDX-2.3","name":"fixture-1.2.3","packages":[{"name":"fixture","versionInfo":"1.2.3"}]}\n', "spdxVersion", "name", "packages"), text("RELEASE_EVIDENCE.md", "Local build only.\nChecksum: verified against dist/fixture.\nSBOM: dist/SBOM.spdx.json.\nTag: withheld.\nPush: withheld.\nUpload/publish: withheld.\n", "Local", "Checksum", "SBOM", "Tag", "Push", "publish")],
    },
    "research-case-study-design": {
        "inputs": {"evidence/interviews.csv": "participant,observation\nP1,synthetic observation\n", "evidence/repository.log": "synthetic commit evidence\n"},
        "outputs": [text("case-study-protocol.md", "Case: synthetic software team.\nUnit of analysis: change review.\nTriangulation: interview and repository log.\n\n| Source location | Claim | Finding |\n| --- | --- | --- |\n| evidence/interviews.csv:2 | P1 observed a synthetic review | interview observation |\n| evidence/repository.log:1 | repository contains synthetic commit evidence | repository corroboration |\n\nChain of evidence: source location -> claim -> finding.\nEthics: synthetic data only.\nThreats: single-case transferability.\n", "Case", "Unit of analysis", "Triangulation", "Source location", "evidence/interviews.csv:2", "evidence/repository.log:1", "Chain of evidence", "Ethics", "Threats")],
    },
    "research-paper-authoring": {
        "inputs": {"sources.bib": "@article{fixture,author={A},title={T},journal={J},year={2026}}\n"},
        "outputs": [text("paper/main.tex", "\\documentclass{article}\n\\begin{document}\n\\section{Introduction}\nSynthetic claim \\cite{fixture}.\n\\section{Method}\nReproducible method.\n\\bibliography{../sources}\n\\end{document}\n", "documentclass", "Introduction", "Method", "cite{fixture}", "bibliography"), json_file("bibliography-report.json", '{"orphaned":[],"unused":[],"malformed":[],"validated":true}\n', "orphaned", "unused", "malformed", "validated")],
    },
    "ci-game-dev-2d": {
        "inputs": {"project.txt": "engine=phaser\npackage-manager=pnpm\n"},
        "outputs": [text(".github/workflows/game.yml", "name: Game CI\non: [push, pull_request]\njobs:\n  verify:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: pnpm install --frozen-lockfile\n      - run: pnpm test\n      - run: pnpm build\n", "Game CI", "pull_request", "ubuntu-latest", "--frozen-lockfile", "pnpm test", "pnpm build", forbids=("deploy", "publish"))],
    },
    "ci-terraform": {
        "inputs": {"main.tf": "terraform { required_version = \">= 1.8\" }\n"},
        "outputs": [text(".github/workflows/terraform.yml", "name: Terraform CI\non: [push, pull_request]\npermissions: read-all\njobs:\n  verify:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: terraform fmt -check\n      - run: terraform validate\n      - run: terraform plan -out=fixture.tfplan\n", "Terraform CI", "permissions: read-all", "terraform fmt -check", "terraform validate", "terraform plan", forbids=("terraform apply", "-auto-approve"))],
    },
    "release-android": {
        "inputs": {"release-context.txt": "platform=android\nversion=1.2.3\n"},
        "outputs": [text("RELEASE_PLAN.md", "Android release candidate 1.2.3\nArtifact: app-release.aab\nChecksum: required\nSigning: external approved boundary\nUpload: withheld\nPublish: withheld\n", "Android", "app-release.aab", "Checksum", "Signing", "Upload: withheld", "Publish: withheld")],
    },
    "release-ai-eng": {
        "inputs": {"release-context.json": '{"version":"1.2.3","prompts":"v3","model_router":"v2","tool_schema":"v2","eval_fingerprint":"fixture-eval-7"}\n'},
        "outputs": [
            text("RELEASE_EVIDENCE.md", "AI release candidate 1.2.3\nPrompts: v3\nModel router: v2\nTool schema: v2\nEvaluation: complete fixture-eval-7\nRollback: restore v1.2.2 configuration and disable traffic\nProvider mutation: withheld\nRollout: withheld\nDeployment: withheld\n", "AI release candidate", "Prompts", "Model router", "Tool schema", "Evaluation: complete", "Rollback", "Provider mutation: withheld", "Rollout: withheld", "Deployment: withheld"),
            json_file("AI_RELEASE_MANIFEST.json", '{"version":"1.2.3","prompts":"v3","model_router":"v2","tool_schema":"v2","eval_fingerprint":"fixture-eval-7","published":false,"provider_mutation":false,"rollout_executed":false}\n', "version", "prompts", "model_router", "tool_schema", "eval_fingerprint", "published", "provider_mutation", "rollout_executed"),
        ],
    },
    "release-go": {
        "inputs": {"release-context.txt": "language=go\nversion=1.2.3\n"},
        "outputs": [text("RELEASE_PLAN.md", "Go release candidate 1.2.3\nArtifacts: linux, macOS, windows\nChecksum: required\nSBOM: required\nTag: withheld\nPublish: withheld\n", "Go", "Artifacts", "Checksum", "SBOM", "Tag: withheld", "Publish: withheld")],
    },
    "release-python": {
        "inputs": {"release-context.txt": "language=python\nversion=1.2.3\n"},
        "outputs": [text("RELEASE_PLAN.md", "Python release candidate 1.2.3\nArtifacts: wheel and sdist\nTwine check: required\nChecksum: required\nUpload: withheld\nPublish: withheld\n", "Python", "wheel", "sdist", "Twine check", "Checksum", "Upload: withheld", "Publish: withheld")],
    },
    "release-terraform": {
        "inputs": {"release-context.txt": "technology=terraform\nversion=1.2.3\n"},
        "outputs": [text("RELEASE_PLAN.md", "Terraform module release candidate 1.2.3\nValidation: fmt, validate, examples\nCompatibility: documented\nTag: withheld\nRegistry publication: withheld\n", "Terraform", "fmt", "validate", "Compatibility", "Tag: withheld", "Registry publication: withheld")],
    },
    "release-typescript": {
        "inputs": {"release-context.txt": "language=typescript\nversion=1.2.3\n"},
        "outputs": [text("RELEASE_PLAN.md", "TypeScript package release candidate 1.2.3\nArtifact: npm pack tarball\nProvenance: required\nChecksum: required\nTag: withheld\nPublish: withheld\n", "TypeScript", "npm pack", "Provenance", "Checksum", "Tag: withheld", "Publish: withheld")],
    },
    "writing-blog-post": {
        "inputs": {"BRIEF.md": "Audience: software engineers. Topic: evidence before automation. Format: Markdown draft.\n"},
        "outputs": [text("blog-post.md", "# Evidence before automation\n\nAutomation is useful only when its result can be checked.\n\n## Start with the observable outcome\n\nDefine the reader, boundary, expected evidence, and failure mode before selecting tooling.\n\n## A practical checklist\n\n- State what changed.\n- Show the smallest relevant check.\n- Separate local evidence from publication authority.\n\n## Limits\n\nThis draft does not claim universal results and is not published.\n", "# Evidence before automation", "observable outcome", "practical checklist", "Limits", "not published")],
    },
    "sdd-specification": {
        "inputs": {"REQUEST.md": "Approved behavior: audit records are retained for 30 days, then deleted. Deletion failures must be retried without extending visibility to ordinary users. No implementation, release, or production mutation is authorized.\n"},
        "outputs": [
            text("SPEC.md", "---\nid: SPEC-RETENTION\ntitle: Audit record retention\nsummary: Retain audit records for 30 days and recover deletion failures\nstatus: approved\nscope: [audit-records]\nauthority:\n  granted: [specification]\n  withheld: [implementation, release, production]\n---\n\n# Intent\n\nAudit records remain available for 30 days, then become unavailable to ordinary users and enter deletion.\n\n## Acceptance criteria\n\n- **RET-001** Given an audit record, it remains available to ordinary users through day 30.\n- **RET-002** After day 30, the record is unavailable to ordinary users and deletion failures are retried.\n\n## Invariant\n\nA deletion retry never restores ordinary-user visibility.\n\n## Explicit exclusions\n\nImplementation, release, and production mutation are outside scope.\n", "id: SPEC-RETENTION", "status: approved", "RET-001", "RET-002", "Invariant", "Explicit exclusions", "withheld"),
            text("behavior-matrix.md", "# Behavior/oracle matrix\n\n| Criterion | Scenario | Invariant | Observable oracle | Oracle provenance | Planned verification | Evidence |\n| --- | --- | --- | --- | --- | --- | --- |\n| RET-001 | day 30 | available through day 30 | ordinary user can read at day 30 | spec-derived | boundary test | pending |\n| RET-002 | deletion retry | retry never restores visibility | read is denied while retry remains scheduled | spec-derived | failure-path integration test | pending |\n", "RET-001", "RET-002", "Observable oracle", "Oracle provenance", "spec-derived", "Planned verification", "pending"),
        ],
    },
    "cloud-supabase": {
        "inputs": {"supabase/migrations/0001_schema.sql": "create table notes(id bigint primary key, clinic_id bigint not null);\n"},
        "outputs": [text("supabase/migrations/0002_notes_rls.sql", "alter table notes enable row level security;\ncreate policy notes_tenant on notes for all to authenticated using (clinic_id = current_setting('app.clinic_id')::bigint) with check (clinic_id = current_setting('app.clinic_id')::bigint);\n", "enable row level security", "policy", "authenticated", "clinic_id", "with check"), text("tests/notes_rls.sql", "begin;\ninsert into notes(id,clinic_id) values (1,7),(2,8);\ngrant select, insert on notes to authenticated;\nset local role authenticated;\nset local app.clinic_id = '7';\ndo $$ begin\n  if (select array_agg(id order by id) from notes) <> array[1] then raise exception 'cross-tenant visibility'; end if;\n  begin insert into notes(id,clinic_id) values (3,8); raise exception 'cross-tenant write allowed'; exception when insufficient_privilege then null; end;\nend $$;\nrollback;\n", "begin", "values (1,7),(2,8)", "grant select, insert", "role authenticated", "set local", "array[1]", "raise exception", "insufficient_privilege", "rollback")],
    },
    "infra-terraform": {
        "inputs": {"main.tf": "terraform { required_version = \">= 1.8\" }\nvariable \"project_id\" { type = string }\n"},
        "outputs": [text("change.tf", "resource \"google_storage_bucket\" \"fixture\" {\n  name     = \"synthetic-fixture-bucket\"\n  project  = var.project_id\n  location = \"EU\"\n}\n", "resource", "project_id", "location"), json_file("plan-summary.json", '{"workspace":"synthetic","add":1,"change":0,"destroy":0,"apply_executed":false}\n', "workspace", "add", "change", "destroy", "apply_executed")],
    },
    "writing-technical-edit": {
        "inputs": {"article.md": "# Reliable agents\n\nAgents always solve every task perfectly.\n"},
        "outputs": [text("article-review.md", "P1 article.md:3 — absolute claim lacks evidence.\nSuggested edit: bounded evaluation evidence does not establish universal reliability.\nSource caveat: verify against primary sources.\nPreservation: article.md remains unchanged.\n", "article.md:3", "evidence", "Suggested edit", "primary sources", "unchanged")],
    },
    "ci-typescript": {
        "inputs": {"package.json": '{"packageManager":"pnpm@11","scripts":{"typecheck":"tsc --noEmit","test":"vitest","build":"vite build"}}\n', "pnpm-lock.yaml": "lockfileVersion: '9.0'\n"},
        "outputs": [text(".github/workflows/typescript.yml", "name: TypeScript CI\non: [push, pull_request]\njobs:\n  verify:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-node@v4\n        with: {node-version: '22', cache: pnpm}\n      - run: corepack enable\n      - run: pnpm install --frozen-lockfile\n      - run: pnpm run typecheck\n      - run: pnpm run lint\n      - run: pnpm run test\n      - run: pnpm run build\n", "runs-on", "checkout@v4", "setup-node@v4", "corepack", "pnpm install --frozen-lockfile", "typecheck", "lint", "test", "build", forbids=("publish", "npm ci"))],
    },
    "web-validation-zod": {
        "inputs": {"src/api.ts": "export function acceptPayload(input: unknown){ return input }\n"},
        "outputs": [text("src/payload-schema.ts", "import { z } from 'zod'\nexport const PayloadSchema=z.object({id:z.string().uuid(),count:z.number().int().nonnegative()})\nexport type Payload=z.infer<typeof PayloadSchema>\nexport const parsePayload=(input:unknown)=>PayloadSchema.safeParse(input)\n", "z.object", "safeParse", "z.infer", "unknown"), text("tests/payload-schema.test.ts", "import { parsePayload } from '../src/payload-schema'\nif(!parsePayload({id:'123e4567-e89b-12d3-a456-426614174000',count:1}).success) throw new Error('valid')\nif(parsePayload({id:'bad',count:1}).success) throw new Error('uuid')\nif(parsePayload({id:'123e4567-e89b-12d3-a456-426614174000',count:-1}).success) throw new Error('count')\n", "parsePayload", "count:-1", "id:'bad'", "throw new Error")],
    },
    "product-ui-ux-design": {
        "inputs": {"product-evidence.json": PRODUCT_UI_UX_EVIDENCE},
        "outputs": [text(
            "product-ux-audit.md",
            PRODUCT_UI_UX_SAMPLE,
            "Verified fixture evidence",
            "Runtime verification: not performed",
            "Prioritized findings",
            "Complete state model",
            "SaaS onboarding",
            "E-commerce checkout",
            "CMS editorial flow",
            "CRM mobile capture",
            "ERP purchase approval",
            "Accessibility and human verification",
            "Experience performance boundary",
            "Profiling is required before assigning a technical root cause",
            "Acceptance:",
            forbids=("WCAG compliant", "runtime verification: passed", "implemented the product"),
        )],
    },
    "product-performance-engineering": {
        "inputs": {"performance-evidence.json": PRODUCT_PERFORMANCE_EVIDENCE},
        "outputs": [text(
            "performance-analysis.md",
            PRODUCT_PERFORMANCE_SAMPLE,
            "Baseline: repeated samples",
            "median and p95",
            "Field improvement: not claimed",
            "Physical-device verification: unavailable",
            "Production load: not executed",
            "Budget unchanged: 2500 ms",
            "Skeleton is not an optimization",
            "Functional equivalence: failed; candidate rejected",
            "Root cause: unsupported without profile",
            "web-lcp-critical-path",
            "web-long-task-input",
            "web-layout-instability",
            "android-startup",
            "android-jank-anr",
            "ios-launch-hang-hitch",
            "mobile-memory-lifecycle",
            "cross-platform-react-native",
            "missing-measurement",
            forbids=(
                "best run only",
                "Field improvement: verified",
                "Root cause: database verified",
                "Budget relaxed: 3500 ms",
                "Skeleton hides the delay",
                "Simulator proves physical performance",
                "production load executed",
            ),
        )],
    },
}

JSON_EQUALS = {
    ("ci-ai-eng", "eval-plan.json"): {"execute": False, "upper_bound_calls": 0, "credentials_required": False, "incomplete_is_green": False},
    ("release-game-dev-2d", "artifacts/manifest.json"): {"deployed": False},
    ("cloud-ops", "operation-plan.json"): {"read_only": True, "project": "synthetic-project"},
    ("release-rust", "dist/manifest.json"): {"published": False},
    ("release-ai-eng", "AI_RELEASE_MANIFEST.json"): {"published": False, "provider_mutation": False, "rollout_executed": False},
    ("research-paper-authoring", "bibliography-report.json"): {"validated": True, "orphaned": [], "malformed": []},
    ("infra-terraform", "plan-summary.json"): {"destroy": 0, "apply_executed": False},
}
for (skill_name, output_path), expected_values in JSON_EQUALS.items():
    output = next(item for item in ORACLES[skill_name]["outputs"] if item["path"] == output_path)
    output["equals"] = expected_values
