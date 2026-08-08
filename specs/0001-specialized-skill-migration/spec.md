---
id: SPEC-0001
title: Migrate specialized Geremmyas skills into a standalone monorepo
summary: Establish agent-skills as the canonical, project-installable home for the specialized Geremmyas skills that Tuxedo does not supersede.
status: ready
scope:
  - skills
  - catalog
  - documentation
  - deterministic validation
  - repository evaluations
risk: large/high-risk
risk_domains:
  - compatibility
  - supply-chain
  - credentials
  - destructive-actions
  - external-services
reversibility: local Git commits can be reverted; the source repositories remain unchanged
change_surfaces:
  - skills/
  - catalog/
  - docs/
  - tests/
  - evals/
  - repository development configuration
contracts:
  - Agent Skills specification
  - skills CLI 1.5.22 documentation
  - Geremmyas source inventory at the recorded commit
  - Tuxedo successor inventory at the recorded commit
review_policy: independent spec, test, and code contexts when available
test_provenance:
  - spec-derived
  - independent
  - external
  - implementation-aware
  - diagnostic-probe
navigation:
  - behavior-matrix.md
  - plan.md
  - tasks.md
  - evidence.md
documentation: required
authority:
  granted:
    - read Geremmyas and Tuxedo
    - persist product and evidence files only in agent-skills
    - create and remove narrowly scoped disposable validation scratch directories outside all three checkouts
    - create the dedicated evaluation home only through an explicit login command
    - run deterministic checks and evaluation dry-runs
    - create atomic local Conventional Commits
  withheld:
    - push
    - release
    - publish
    - pull-request
    - remote mutation
    - model or provider calls without a separately approved budget
    - writes to Geremmyas, Tuxedo, personal Codex/Promptfoo state, or unrelated paths
dependencies:
  - Node and Python dependencies may be development-only
  - consumers require no repository runtime
---

# Intent

Create a self-contained Agent Skills monorepo whose canonical product surface is
`skills/<name>/`. Migrate every specialized Geremmyas skill not superseded by
Tuxedo, preserve the useful skill-local resources and provenance, remove
Geremmyas CLI assumptions, and publish only documentation and declarative
collections for installation through the official `skills` CLI.

The repository must not recreate Geremmyas distribution behavior. Tuxedo stays
the global horizontal engineering workflow; these specialized skills are
project-scoped and independently useful with or without Tuxedo.

### Write boundary

Persistent repository/product changes are authorized only under
`agent-skills`. The user's explicit clean-room installation and isolated-eval
requirements narrowly authorize operational scratch created with a freshly
allocated temporary directory outside all three checkouts, provided its exact
resolved path is recorded, it contains only synthetic fixtures/tool state, and
it is removed after the check. No temporary path may resolve through a symlink
to a checkout or personal configuration.

The one allowed persistent out-of-checkout state is the dedicated evaluation
home selected by `AGENT_SKILLS_EVAL_CODEX_HOME` (default
`$HOME/.codex-agent-skills-evals`). Only the explicit `eval:login` command may
create it; deterministic checks, dry-runs, config validation, and auth status do
not create it. It may retain Codex-managed authentication and the minimal
operational state enumerated under AS-023. The harness never deletes it
automatically. Removing it is a separately deliberate repository action. This
exception does not authorize any write to the personal `CODEX_HOME`,
`$HOME/.codex`, Geremmyas, Tuxedo, or unrelated paths.

## Frozen source baseline

- Geremmyas repository: `783ac878213b61acb914b9151c779c6de0b84286`
- Geremmyas `content/skills` Git-tree listing SHA-256:
  `7de30d71108e8c4e73641a70aaa2d9541ce97f6b826cca528f6eeed0bb73e20d`
- Tuxedo repository: `168922a54b695fd2446295c58157981079d2d5d6`
- Tuxedo `plugins/tuxedo/skills` Git-tree listing SHA-256:
  `3ed55c2bcd4614cd7074a6ff4ff01199a81b4dd9f31d9912fa25f191c85a967f`
- Geremmyas skill directories found: 49.
- Tuxedo-successor exclusions present in Geremmyas: 16.
- Specialized migration set: 33.
- Initial `git status --porcelain=v1 --untracked-files=all`: empty in all three
  repositories before destination artifacts were written. The destination had
  an unborn `main`; Geremmyas and Tuxedo had the HEADs recorded above.

The tree-listing digest algorithm is byte-exact: set `LC_ALL=C`, run
`git -C <repository> ls-tree -r --full-tree <commit> <path>` with its ordinary
newline-delimited stdout (which is Git-sorted and includes mode, object type,
blob object ID, and path), and SHA-256 the stdout bytes without transformation.

### Normative migrated set (33)

`android-ci-setup`, `chromadb-rag-workflow`, `game-ai-2d`, `game-art-2d`,
`game-audio-2d`, `game-build-and-release`, `game-feel-2d`,
`game-performance-2d`, `game-save-n-progress`, `game-testing-2d`,
`game-ui-accessibility`, `gameplay-programming-2d`, `gcloud-operation`,
`go-ci-setup`, `langgraph-agent-design`, `llm-integration-review`,
`manage-state-with-zustand`, `migrate-react-router`,
`model-state-with-xstate`, `paper-review`, `postgres-query-review`,
`procedural-generation-2d`, `python-ci-setup`, `rust-ci-setup`, `rust-release`,
`scientific-case-study-research`, `scientific-paper`, `skill-authoring`,
`supabase-workflow`, `terraform-change`, `text-review`, `typescript-ci-setup`,
and `validate-with-zod`.

### Normative excluded set (16)

`brainstorming`, `bugfix`, `ci-workflow`, `decision-framework`,
`design-deep-modules`, `docs`, `git-commit`, `improve-architecture`,
`premortem`, `refine`, `session-bridge`, `shape-domain`, `spec`, `tdd`,
`technical-research`, and `verify`.

### Normative collection set (20)

`game-core`, `game-ui`, `game-systems`, `game-performance`, `game-audio`,
`game-art`, `game-delivery`, `game-dev`, `android`, `go`, `python`, `rust`,
`typescript`, `web`, `data`, `infrastructure`, `ai`, `scientific-research`,
`writing`, and `skill-maintenance`.

### Normative security classification

All behavior evals use protected hashes and an outside sentinel. The additional
adversarial security contract applies to these 21 skills because their primary
workflow adds a sensitive surface beyond ordinary scoped file editing:

| Skill | Required security domains |
| --- | --- |
| `android-ci-setup` | CI authority, supply chain, signing/release credentials |
| `chromadb-rag-workflow` | database persistence, tenancy, destructive collection operations |
| `game-art-2d` | bundled filesystem-writing scripts, image-generation tooling |
| `game-build-and-release` | artifact integrity, secrets, release/deploy authority |
| `game-save-n-progress` | persistence, corruption, overwrite/data loss |
| `gcloud-operation` | cloud identity, IAM, billing, remote mutation |
| `go-ci-setup` | CI authority, dependency execution, release/container supply chain |
| `langgraph-agent-design` | tool side effects, resumability, external systems |
| `llm-integration-review` | external model services, private data, privileged tools |
| `migrate-react-router` | dependency mutation, broad filesystem rewrite |
| `paper-review` | explicit in-place overwrite of user-authored files |
| `postgres-query-review` | database writes, locks, migrations, data loss |
| `python-ci-setup` | CI authority, dependency execution, package publication |
| `rust-ci-setup` | CI authority, dependency execution, release supply chain |
| `rust-release` | tagging, pushing, signing, publishing, upload authority |
| `scientific-case-study-research` | participant/private research data and external systems |
| `scientific-paper` | bundled filesystem-reading script and authored research artifacts |
| `supabase-workflow` | database/Auth/Storage/RLS and remote platform mutation |
| `terraform-change` | infrastructure/state mutation, secrets, destructive scope |
| `text-review` | explicit in-place overwrite of user-authored files |
| `typescript-ci-setup` | CI authority, dependency execution, release supply chain |

The remaining 12 skills are classified non-sensitive for the additional
security suite because their primary contract stays within ordinary scoped code,
analysis, or local design: `game-ai-2d`, `game-audio-2d`, `game-feel-2d`,
`game-performance-2d`, `game-testing-2d`, `game-ui-accessibility`,
`gameplay-programming-2d`, `manage-state-with-zustand`,
`model-state-with-xstate`, `procedural-generation-2d`, `skill-authoring`, and
`validate-with-zod`. This does not waive their AS-019 protected-path and
outside-sentinel controls.

Implementation must stop with an explicit inventory error if a fresh source
inspection does not reproduce this baseline. The committed repository must not
depend on either absolute checkout path; the paths above are evidence from this
repository migration task, not consumer configuration.

A later source-repository commit that leaves the complete governed skill tree
byte-identical does not change the frozen provenance baseline. Such checkout
drift must be recorded, compared against the frozen tree, and never silently
substituted as the source commit.

## Behavior and invariants

1. `skills/<name>/` is the only canonical copy of each migrated skill.
2. Each skill is independently valid and contains every necessary owned
   resource recursively.
3. No excluded horizontal Tuxedo successor exists under `skills/`.
4. No skill requires Geremmyas, Tuxedo, a repository development dependency, or
   another skill at runtime. Optional composition may be documented.
5. Collections are declarative, deterministic sets of existing skill names.
   They install, execute, and resolve nothing by themselves.
6. The README installation commands are checked against the same collection
   catalog they document.
7. Repository evaluation tooling stays outside every skill and fails closed on
   unsafe homes, ambiguous authentication, provider use without explicit
   execution, contaminated state, and unsanitized evidence.
8. Geremmyas and Tuxedo remain byte-for-byte untouched by this task.

## Acceptance criteria

- **AS-001 — Source reconciliation:** A fresh read-only inventory proves
  equality with the two normative name sets and `49 total = 33 migrated + 16
  excluded`, with disjoint sets and every excluded name present in both the
  Geremmyas inventory and the Tuxedo successor tree.
- **AS-002 — Frozen inputs:** Validation proves the recorded source commits
  still exist and compares expected inventories and complete governed-tree
  hashes against them. A clean later checkout HEAD is acceptable only when its
  governed tree is byte-identical; it is recorded and never replaces the
  provenance commit.
- **AS-003 — Exact destination inventory:** `skills/` contains exactly the 33
  expected directories, each with one top-level `SKILL.md`, and none of the 16
  excluded names.
- **AS-004 — Recursive ownership:** Every expected source file for a migrated
  skill has a destination disposition (`preserved`, `adapted`, or intentionally
  excluded with rationale); no cache, local result, client materialization, CLI
  manifest, or Geremmyas runtime file enters a skill.
- **AS-005 — Valid skill contract:** Every `SKILL.md` has valid YAML, a unique
  lowercase kebab-case `name` matching its directory, a non-empty actionable
  routing `description`, and valid Agent Skills metadata.
- **AS-006 — Resource integrity:** All local Markdown links and explicit
  skill-local resource/script references resolve, and shipped scripts pass
  syntax checks plus representative execution tests.
- **AS-007 — Portable standalone behavior:** Accidental Geremmyas CLI paths,
  commands, packs, manifests, targets, hooks, instruction materializations,
  personal absolute paths, and mandatory Tuxedo references are absent. Every
  discovered reference to those surfaces has an explicit migration disposition.
  Deliberate Codex metadata and tools are documented as client-specific
  compatibility, not universal support.
- **AS-008 — Game scope:** Game skills remain limited by default to Phaser and
  Godot 2D, with Pixel Art where applicable; Unity, PixiJS, and 3D are not added
  as default scope.
- **AS-009 — Provenance and license:** The repository records source commits,
  per-skill source paths and content hashes, adapted-file dispositions, MIT
  provenance, and preserves applicable credits or notices. The frozen
  Geremmyas `LICENSE` is inspected from Git, must have SHA-256
  `24923e703cfafa4e2c5098f4d5b0442ab43f9405dbdbb9fd961707c32e5e4702`,
  and its scope plus any skill-local notice exception is recorded rather than
  inferred from authorship.
- **AS-010 — Catalog schema:** `catalog/collections.json` has a documented,
  versioned schema and contains only unique names, descriptions, direct skills,
  and/or collection includes allowed by that schema.
- **AS-011 — Collection validity:** All required focused collections exist,
  exactly matching the normative collection set,
  reference only real skills, contain no duplicate direct or expanded entries,
  reject include cycles, and expand deterministically. `game-dev` expands the
  seven focused game collections in declared order.
- **AS-012 — Catalog coverage:** Every migrated skill appears in the skill
  inventory and at least one collection or declared category.
- **AS-013 — README contract:** The README explains agent-skills, Tuxedo,
  standalone composition, project scope, collections as documentation only,
  listing, individual installation, every collection command, update, removal,
  compatibility evidence, and external CLI telemetry controls.
- **AS-014 — Command drift protection:** Every skill identifier in README
  `skills` commands exists, every required collection command is derived from
  the catalog, and the checked block matches deterministic rendered output.
- **AS-015 — Official CLI contract:** Commands match current primary `skills`
  CLI documentation and a pinned observed version; a clean temporary local
  repository install lists, installs, and discovers a representative single
  skill and multi-skill collection without touching personal configuration.
- **AS-016 — Official skill validation:** Every one of the 33 skill directories
  passes the official Agent Skills validator used by repository validation.
- **AS-017 — Deterministic validation:** One explicit command validates the
  inventory, frontmatter, descriptions, links, resources, portability scans,
  catalogs, README commands, eval coverage, isolation policy, forbidden files,
  official skill validation, and known source baseline without model calls.
- **AS-018 — Routing eval coverage:** All 33 skills have an explicit positive,
  an applicable implicit positive, and a justified negative or collision case;
  related-skill collisions, legitimate multi-skill composition, and focal skill
  selection with Tuxedo present are represented without Cartesian expansion.
  Applicability of implicit invocation is recorded per skill; an explicit-only
  skill has a documented exception instead of a synthetic implicit trigger.
- **AS-019 — Behavior eval coverage:** All 33 skills have at least one
  criterion-linked significant scenario, controlled fixture, observable output,
  independent or spec-derived oracle, no-op rejection, fresh workspace, hashes
  of protected paths, and an outside-workspace sentinel for every write-capable
  trial.
- **AS-020 — Composition eval coverage:** The catalog evaluates the focal skill
  through proportionate `baseline` (without focal), `focal` (only focal),
  `composed-specialized` (legitimate companions), `tuxedo-minimal` (focal plus
  the smallest relevant Tuxedo subset), `tuxedo-full-plugin` (the complete
  external plugin when technically viable), and `current`/`proposed` variants
  for future revisions. The catalog records applicability or a concrete
  technical non-viability reason for every optional variant. Each variant has
  its own oracle. No Tuxedo skill is copied into agent-skills and absence of
  Tuxedo remains supported.
- **AS-021 — Security eval coverage:** Every skill classified as sensitive for
  cloud, infrastructure, database, release, destructive command, filesystem,
  persistence, or external-service behavior has a concrete adversarial
  stimulus, mandatory legitimate change, protected hashes, outside sentinel,
  canary, and `needs-review` fallback when trajectory evidence is unavailable.
  The inventory classifies all 33 skills with a sensitivity boolean, zero or
  more domains, and rationale. Validation derives the security-case set from
  that classification and rejects an unclassified skill or a sensitive skill
  without its required case.
- **AS-022 — Verdict integrity:** Deterministic failure outranks semantic
  review; `pass`, `fail`, and `needs-review` remain distinct; empty refusal or a
  completion claim without the required artifact cannot pass.
- **AS-023 — Evaluation isolation:** Provider runs use a dedicated absolute
  home outside the checkout and personal Codex homes, resolve symlinks, never
  read/copy/print/link personal `auth.json`, accept only `Logged in using
  ChatGPT`, and remove API-key variables. They reject personal or unknown
  skills, plugins, memories, rules, MCPs, hooks, instruction files, policy,
  profiles, model/provider settings, and unknown configuration keys. Allowed
  operational entries and the curated Codex-managed plugin cache must be real
  files/directories rather than symlinks and are validated fail-closed.
  Promptfoo Cloud sharing is explicitly disabled. Each case declares whether
  network is required; network is disabled for all others. Runs use disposable
  Promptfoo state and fresh Git workspaces and never use real credentials or
  projects in fixtures.
- **AS-024 — Evidence privacy:** Only append-only sanitized verdict reports may
  persist. Prompts, raw responses, traces, secrets, credentials, and canaries do
  not enter durable output; completed shard checkpoints survive peer failure.
- **AS-025 — Explicit evaluation commands:** Separate commands exist for
  deterministic validation, Promptfoo configuration validation, dry-run,
  dedicated auth status/login, smoke, routing, behavior, composition, security,
  compare, and full evaluation. Install, commit, push, and ordinary CI never
  invoke a model/provider.
- **AS-026 — Budget gate:** Every provider-reaching command first computes exact
  target trials, secondary judgments, shard ranges, and concurrency. Execution
  additionally requires an explicit flag and a human-approved budget token; no
  provider call occurs in this task.
- **AS-027 — Development dependency boundary and project identity:** Python/Node
  dependencies, Promptfoo, and `@openai/codex-sdk` are outside all skills, use
  UV/PNPM conventions, and are unnecessary for installed skill use. Top-level
  Node and Python manifests identify the repository as `agent-skills`; internal
  tooling labels do not replace the canonical product name.
- **AS-028 — Documentation and reviews:** Architecture, catalog, compatibility,
  migration, evaluation, and evidence docs are reconciled. Spec, tests, and
  code receive separately reconstructed reviews, with final findings under
  `Spec`, `Standards`, and `Risk`.
- **AS-029 — Source integrity and Git:** Final evidence proves Geremmyas retains
  its baseline commit and clean status; Tuxedo retains a clean status and the
  frozen governed skill tree even if unrelated commits move its checkout HEAD;
  agent-skills has only task-owned commits/changes, `git diff --check` passes,
  and no push, release, publication, PR, remote mutation, or unauthorized model
  call occurred.

## Explicit exclusions

- A custom installation CLI, package manager, daemon, pack resolver, sync
  layer, target generator, client generator, telemetry, or consumer runtime.
- Copies of the 16 Tuxedo successor skills or of Tuxedo plugin content.
- Bidirectional synchronization with Geremmyas or Tuxedo.
- Automatic technology detection or automatic collection installation.
- Unity, PixiJS, or 3D as default game-development scope.
- Real provider evaluation, release, publication, push, PR, or remote mutation.

## Edge and failure scenarios

- A governed source inventory or tree differs from the frozen baseline: stop
  and report drift; do not silently recalculate expected output. A clean later
  checkout commit with a byte-identical governed tree is recorded and may be
  used only as a live validation checkout; provenance does not move.
- A source-relative link escapes its skill: either internalize the owned
  resource or replace the reference with portable prose and record adaptation.
- An external command or tool is client-specific: retain only when deliberate,
  state the verified client boundary, and provide a useful fallback when one
  exists.
- A collection includes another collection: expand depth-first in declared
  order, reject cycles, and reject repeated final skills.
- Dedicated authentication is absent: auth status and provider suites fail
  before fixture/workspace creation; dry-run remains available.
- Structured trajectory is unavailable for a security case: return
  `needs-review`, never infer safety from prose alone.
- Tuxedo full-plugin composition is unavailable in the isolated harness:
  record the exact technical blocker and still run the standalone and minimal
  composition variants; do not replace plugin evidence with copied skills.

## Open decisions and assumptions

- The frozen Geremmyas repository-level MIT license is the candidate source
  license. Its committed text, scope, and every skill-local notice or credit
  must be inspected before redistribution; same authorship is not license
  evidence.
- The repository uses the external `skills` CLI only for clean-room maintenance
  validation and user commands. It does not vendor or wrap that CLI.
- The provider harness may pin the currently reviewed Tuxedo development
  versions of Promptfoo and the Codex SDK, subject to lockfile and audit checks.

## Evidence and review

- Behavior matrix: `behavior-matrix.md`
- Fail-first evidence: `evidence.md`
- Documentation decision: required; see `docs/`
- Spec review: `reviews/spec-review.md`
- Test review: `reviews/test-review.md`
- Code review: `reviews/code-review.md`
