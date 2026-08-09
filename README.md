# Storehouse

A curated set of skills for Phaser, Godot, Android Native, TypeScript, Python, Golang, Rust, Terraform, Data Modeling, Cloud Infrastructure and AI Engineering

## Storehouse and Baseline

[Baseline](https://github.com/woliveiras/baseline) is the recommended global Codex
plugin for horizontal engineering workflows such as proportional measurement,
TDD, review, documentation, architecture, decisions, security, and session
continuity. Baseline provides the foundation. Storehouse provides optional depth
through specialized skills and owns the optional SDD methodology through the
standalone `sdd-specification` skill and `sdd` collection. Either product works independently;
when both are present, approved SDD artifacts may feed installed TDD and review
capabilities without a physical or runtime dependency.

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
npx skills add woliveiras/storehouse --skill game-dev-2d-gameplay
```

Choose target agents or copy mode with the official CLI flags when the default
discovery is not appropriate. Review the CLI prompt before accepting writes.

## Collections

The following commands document the groups declared in
`catalog/collections.json` and are checked by the repository test suite.

<!-- collections:start -->
### `game-core`

Core 2D gameplay programming and deterministic game testing.

```bash
npx skills add woliveiras/storehouse \
  --skill game-dev-2d-gameplay \
  --skill game-dev-2d-testing
```

### `game-ui`

Accessible 2D game interfaces and moment-to-moment feel.

```bash
npx skills add woliveiras/storehouse \
  --skill game-dev-2d-ui-accessibility \
  --skill game-dev-2d-feel
```

### `game-systems`

AI, procedural generation, saves, and progression for Phaser and Godot 2D.

```bash
npx skills add woliveiras/storehouse \
  --skill game-dev-2d-ai \
  --skill game-dev-2d-procedural-generation \
  --skill game-dev-2d-save-progression
```

### `game-performance`

Measured 2D game performance work.

```bash
npx skills add woliveiras/storehouse \
  --skill game-dev-2d-performance
```

### `game-audio`

2D game audio systems and lifecycle.

```bash
npx skills add woliveiras/storehouse \
  --skill game-dev-2d-audio
```

### `game-art`

2D runtime art production, processing, and integration.

```bash
npx skills add woliveiras/storehouse \
  --skill game-dev-2d-art
```

### `game-ci`

Continuous integration for Phaser and Godot 2D projects.

```bash
npx skills add woliveiras/storehouse \
  --skill ci-game-dev-2d
```

### `game-release`

Versioned Phaser and Godot 2D release artifacts and evidence.

```bash
npx skills add woliveiras/storehouse \
  --skill release-game-dev-2d
```

### `game-dev`

Complete aggregate of the focused Phaser and Godot 2D collections.

```bash
npx skills add woliveiras/storehouse \
  --skill game-dev-2d-gameplay \
  --skill game-dev-2d-testing \
  --skill game-dev-2d-ui-accessibility \
  --skill game-dev-2d-feel \
  --skill game-dev-2d-ai \
  --skill game-dev-2d-procedural-generation \
  --skill game-dev-2d-save-progression \
  --skill game-dev-2d-performance \
  --skill game-dev-2d-audio \
  --skill game-dev-2d-art \
  --skill ci-game-dev-2d \
  --skill release-game-dev-2d
```

### `ci`

Continuous integration for AI engineering, Android, game development 2D, Go, Python, Rust, Terraform, and TypeScript.

```bash
npx skills add woliveiras/storehouse \
  --skill ci-ai-eng \
  --skill ci-android \
  --skill ci-game-dev-2d \
  --skill ci-go \
  --skill ci-python \
  --skill ci-rust \
  --skill ci-terraform \
  --skill ci-typescript
```

### `release`

Release engineering for AI engineering, Android, game development 2D, Go, Python, Rust, Terraform, and TypeScript.

```bash
npx skills add woliveiras/storehouse \
  --skill release-ai-eng \
  --skill release-android \
  --skill release-game-dev-2d \
  --skill release-go \
  --skill release-python \
  --skill release-rust \
  --skill release-terraform \
  --skill release-typescript
```

### `android`

Android CI and release engineering.

```bash
npx skills add woliveiras/storehouse \
  --skill ci-android \
  --skill release-android
```

### `go`

Go CI and release engineering.

```bash
npx skills add woliveiras/storehouse \
  --skill ci-go \
  --skill release-go
```

### `python`

Python CI and release engineering.

```bash
npx skills add woliveiras/storehouse \
  --skill ci-python \
  --skill release-python
```

### `rust`

Rust CI and release engineering.

```bash
npx skills add woliveiras/storehouse \
  --skill ci-rust \
  --skill release-rust
```

### `terraform`

Terraform infrastructure, CI, and release engineering.

```bash
npx skills add woliveiras/storehouse \
  --skill infra-terraform \
  --skill ci-terraform \
  --skill release-terraform
```

### `typescript`

TypeScript CI, release, and boundary validation.

```bash
npx skills add woliveiras/storehouse \
  --skill ci-typescript \
  --skill release-typescript \
  --skill web-validation-zod
```

### `web`

Zustand, XState, and Zod recipes for web applications.

```bash
npx skills add woliveiras/storehouse \
  --skill web-state-zustand \
  --skill web-state-xstate \
  --skill web-validation-zod
```

### `data`

PostgreSQL, RAG storage, and Supabase workflows.

```bash
npx skills add woliveiras/storehouse \
  --skill database-postgresql \
  --skill ai-eng-rag-pipeline \
  --skill cloud-supabase
```

### `infrastructure`

Cloud operations, Supabase, and Terraform infrastructure.

```bash
npx skills add woliveiras/storehouse \
  --skill cloud-ops \
  --skill cloud-supabase \
  --skill infra-terraform
```

### `ai-engineering`

Agent, LLM service, RAG pipeline, CI, and release engineering.

```bash
npx skills add woliveiras/storehouse \
  --skill ai-eng-agent-design \
  --skill ai-eng-llm-integration \
  --skill ai-eng-rag-pipeline \
  --skill ci-ai-eng \
  --skill release-ai-eng
```

### `scientific-research`

Scientific papers, empirical case studies, and academic draft editing.

```bash
npx skills add woliveiras/storehouse \
  --skill research-paper-authoring \
  --skill research-case-study-design \
  --skill writing-academic-edit
```

### `writing`

Technical blog authoring and evidence-preserving editing.

```bash
npx skills add woliveiras/storehouse \
  --skill writing-blog-post \
  --skill writing-technical-edit \
  --skill writing-academic-edit
```

### `sdd`

Optional Specification-Driven Development with durable specifications, oracle matrices, reconciliation, and formal review.

```bash
npx skills add woliveiras/storehouse \
  --skill sdd-specification
```
<!-- collections:end -->

## Update and remove

Check for updates across installed skills, or update a named skill:

```bash
npx skills check
npx skills update
npx skills update game-dev-2d-gameplay
```

Remove a skill from the current project:

```bash
npx skills remove game-dev-2d-gameplay
```

Removing a collection means removing its individual skill names; collections
have no installed identity.

## Compatibility and privacy

The 42 directories validate against the Agent Skills contract. A clean-room
official CLI installation smoke is required when distribution, collections, or
skill layout changes. Twelve game skills retain deliberate Codex
`agents/openai.yaml` metadata. `game-dev-2d-art` can use Codex image generation
when available, but documents a non-generation fallback. Support claims do not
extend beyond fresh recorded checks.

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
Evaluation dependencies use UV and PNPM. Nothing under `tests/` or `evals/` is
needed by an installed skill.

## License

MIT. See [`LICENSE`](LICENSE).
