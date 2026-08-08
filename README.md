# Storehouse

Storehouse is William Oliveira's curated source of specialized,
project-installable [Agent Skills](https://agentskills.io/specification) for
Phaser and Godot 2D, Android, languages and frameworks, data and cloud
infrastructure, AI/RAG, scientific research, and technical writing. Each folder
under `skills/` is an independent capability that coding agents can use without
any runtime from this repository.

## Storehouse and Tuxedo

[Tuxedo](https://github.com/woliveiras/tuxedo) is the recommended global Codex
plugin for horizontal engineering workflows such as specification, TDD,
verification, documentation, architecture, decisions, security, and session
continuity. This repository supplies vertical capabilities selected per
project. Either product works independently; when both are present, their
workflows may compose without a physical or runtime dependency.

Collections below are documented groups of ordinary `--skill` arguments. They
are not packs, a package manager, dependency declarations, or executable
runtime metadata. `catalog/collections.json` is declarative and installs
nothing.

## Install by project

The examples use the official [`skills` CLI](https://github.com/vercel-labs/skills/blob/main/README.md),
locked as a development dependency for repository validation. Project scope is
the CLI default. Run commands from the project that should receive the skill.

List the skills in this repository:

```bash
npx skills add woliveiras/storehouse --list
```

Install one skill:

```bash
npx skills add woliveiras/storehouse --skill gameplay-programming-2d
```

Choose target agents or copy mode with the official CLI flags when the default
discovery is not appropriate. Review the CLI prompt before accepting writes.

## Collections

The following block is rendered deterministically from
`catalog/collections.json` and checked by the repository test suite.

<!-- collections:start -->
### `game-core`

Core 2D gameplay programming and deterministic game testing.

```bash
npx skills add woliveiras/storehouse \
  --skill gameplay-programming-2d \
  --skill game-testing-2d
```

### `game-ui`

Accessible 2D game interfaces and moment-to-moment feel.

```bash
npx skills add woliveiras/storehouse \
  --skill game-ui-accessibility \
  --skill game-feel-2d
```

### `game-systems`

AI, procedural generation, saves, and progression for Phaser and Godot 2D.

```bash
npx skills add woliveiras/storehouse \
  --skill game-ai-2d \
  --skill procedural-generation-2d \
  --skill game-save-n-progress
```

### `game-performance`

Measured 2D game performance work.

```bash
npx skills add woliveiras/storehouse \
  --skill game-performance-2d
```

### `game-audio`

2D game audio systems and lifecycle.

```bash
npx skills add woliveiras/storehouse \
  --skill game-audio-2d
```

### `game-art`

2D runtime art production, processing, and integration.

```bash
npx skills add woliveiras/storehouse \
  --skill game-art-2d
```

### `game-delivery`

Reproducible Phaser and Godot build and release evidence.

```bash
npx skills add woliveiras/storehouse \
  --skill game-build-and-release
```

### `game-dev`

Complete aggregate of the seven focused Phaser and Godot 2D collections.

```bash
npx skills add woliveiras/storehouse \
  --skill gameplay-programming-2d \
  --skill game-testing-2d \
  --skill game-ui-accessibility \
  --skill game-feel-2d \
  --skill game-ai-2d \
  --skill procedural-generation-2d \
  --skill game-save-n-progress \
  --skill game-performance-2d \
  --skill game-audio-2d \
  --skill game-art-2d \
  --skill game-build-and-release
```

### `android`

Android CI and delivery checks.

```bash
npx skills add woliveiras/storehouse \
  --skill android-ci-setup
```

### `go`

Go CI and supply-chain checks.

```bash
npx skills add woliveiras/storehouse \
  --skill go-ci-setup
```

### `python`

Python CI, validation, and publishing preparation.

```bash
npx skills add woliveiras/storehouse \
  --skill python-ci-setup
```

### `rust`

Rust CI and release engineering.

```bash
npx skills add woliveiras/storehouse \
  --skill rust-ci-setup \
  --skill rust-release
```

### `typescript`

TypeScript CI and boundary validation.

```bash
npx skills add woliveiras/storehouse \
  --skill typescript-ci-setup \
  --skill validate-with-zod
```

### `web`

React Router migration plus Zustand, XState, and Zod recipes.

```bash
npx skills add woliveiras/storehouse \
  --skill migrate-react-router \
  --skill manage-state-with-zustand \
  --skill model-state-with-xstate \
  --skill validate-with-zod
```

### `data`

PostgreSQL, ChromaDB/RAG, and Supabase workflows.

```bash
npx skills add woliveiras/storehouse \
  --skill postgres-query-review \
  --skill chromadb-rag-workflow \
  --skill supabase-workflow
```

### `infrastructure`

Google Cloud and Terraform operations.

```bash
npx skills add woliveiras/storehouse \
  --skill gcloud-operation \
  --skill terraform-change
```

### `ai`

LangGraph, LLM service, and RAG design and review.

```bash
npx skills add woliveiras/storehouse \
  --skill langgraph-agent-design \
  --skill llm-integration-review \
  --skill chromadb-rag-workflow
```

### `scientific-research`

Scientific papers, empirical case studies, and academic draft review.

```bash
npx skills add woliveiras/storehouse \
  --skill scientific-paper \
  --skill scientific-case-study-research \
  --skill paper-review
```

### `writing`

Evidence-preserving technical blog review.

```bash
npx skills add woliveiras/storehouse \
  --skill text-review
```

### `skill-maintenance`

Portable Agent Skill authoring and review.

```bash
npx skills add woliveiras/storehouse \
  --skill skill-authoring
```
<!-- collections:end -->

## Update and remove

Check for updates across installed skills, or update a named skill:

```bash
npx skills check
npx skills update
npx skills update gameplay-programming-2d
```

Remove a skill from the current project:

```bash
npx skills remove gameplay-programming-2d
```

Removing a collection means removing its individual skill names; collections
have no installed identity.

## Compatibility and privacy

The 33 directories validate against the Agent Skills contract. Clean-room
installer checks cover repository listing plus representative individual and
multi-skill discovery; exact tested agents are recorded in
[`docs/compatibility.md`](docs/compatibility.md). Eleven game skills retain
deliberate Codex `agents/openai.yaml` metadata. `game-art-2d` can use Codex
image generation when available, but documents a non-generation fallback.
Support claims do not extend beyond those checks.

The external `skills` CLI reports anonymous aggregate telemetry by default.
Its documentation says to disable it with either environment variable:

```bash
DISABLE_TELEMETRY=1 npx skills add woliveiras/storehouse --list
DO_NOT_TRACK=1 npx skills add woliveiras/storehouse --list
```

## Development

See [`docs/architecture.md`](docs/architecture.md),
[`docs/catalog.md`](docs/catalog.md), and
[`docs/validation-and-evaluations.md`](docs/validation-and-evaluations.md).
Development dependency provenance is recorded in
[`docs/development-dependencies.md`](docs/development-dependencies.md).
Python maintenance uses UV; Node maintenance uses PNPM. Nothing under
`maintenance/`, `tests/`, or `evals/` is needed by an installed skill.

## License

MIT. See [`LICENSE`](LICENSE) and the frozen per-file provenance inventory in
[`catalog/skills.json`](catalog/skills.json).
