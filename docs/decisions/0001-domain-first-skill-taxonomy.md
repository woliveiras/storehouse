# Adopt domain-first skill identifiers

- Status: accepted
- Date: 2026-08-09
- Decision makers: @woliveiras
- Consulted: Codex
- Informed: Storehouse users
- Supersedes: none

## Context and Problem Statement

Storehouse skill identifiers mixed technology-first names, action-first names,
and domain-first names. The inconsistency made alphabetical discovery noisy and
embedded volatile implementation choices such as ChromaDB, LangGraph, and
Google Cloud in otherwise durable capabilities. CI and release responsibilities
were also combined for games but separated for Rust.

Skill identifiers are public installation contracts. The repository therefore
needs one coordinated taxonomy migration rather than incremental aliases or
permanent duplicate directories.

## Decision Drivers

- Skills remain standalone directories directly under `skills/`.
- Alphabetical listing should group related capabilities without nested folders.
- Volatile frameworks and providers should use progressively disclosed references
  when they share a stable workflow and safety boundary.
- CI validation and release production have different triggers, authority, and
  outputs even when both execute on the same automation platform.
- Frozen Geremmyas provenance must survive renamed Storehouse identifiers.

## Considered Options

- Keep the mixed identifiers and rely on collections.
- Create nested domain directories.
- Adopt flat, domain-first identifiers with conditional references.

## Decision Outcome

Chosen option: **flat, domain-first identifiers with conditional references**,
because it improves discovery while preserving the portable `skills/<name>/`
distribution boundary.

The distributed inventory contains 42 skills under these namespaces:
`ai-eng`, `ci`, `cloud`, `database`, `game-dev`, `infra`, `release`,
`research`, `sdd`, `web`, and `writing`.

CI and release use symmetric technology suffixes for AI engineering, Android,
game development 2D, Go, Python, Rust, Terraform, and TypeScript. CI verifies
changes; release versions, packages, signs, or prepares distribution.
Publishing, uploading, tagging, pushing, deploying, provider configuration, or
mutating a remote registry still requires the authority of the consuming
repository.

ChromaDB and pgvector are references inside `ai-eng-rag-pipeline`; LangGraph
and CrewAI are references inside `ai-eng-agent-design`; Google Cloud and AWS are
references inside `cloud-ops`. PostgreSQL guidance is organized by modeling,
query review, performance, and migrations/operations.

`migrate-react-router` and `skill-authoring` are retired. Storehouse relies on
the host client's skill-creation capability instead of distributing its own
authoring skill.

### Consequences

- Good: related skills group predictably in clients and installation listings.
- Good: framework/provider additions do not require new public identifiers when
  the governing workflow remains stable.
- Good: CI and release authority boundaries become explicit and testable.
- Bad: all previous identifiers are breaking changes for installed copies and
  documentation.
- Bad: routing, behavior, composition, security, fixtures, catalog provenance,
  and clean-room installation evidence must migrate together.
- Neutral: collections remain declarative documentation and may overlap.

## Pros and Cons of the Options

### Keep the mixed identifiers

- Good: no migration cost.
- Bad: collections do not organize the client's alphabetical skill listing.
- Bad: technology changes continue to produce inconsistent public names.

### Create nested domain directories

- Good: filesystem hierarchy would be visually explicit.
- Bad: it violates the repository's direct `skills/<name>/` product boundary
  and risks incompatible discovery across clients.

### Adopt flat, domain-first identifiers

- Good: it preserves standalone distribution and improves alphabetical discovery.
- Good: references hide provider-specific translation behind stable workflows.
- Bad: it requires a coordinated breaking migration.

## Confirmation

The decision is confirmed when deterministic tests observe exactly 42 valid
skills, CI/release suffix parity, conditional references, renamed provenance,
complete routing/behavior/composition/security inventories, official validation,
and clean-room installation. Provider/model evaluation remains separately
authorized and is not required for the local taxonomy migration.

## More Information

- `AGENTS.md`
- `docs/architecture.md`
- `docs/catalog.md`
- `docs/validation-and-evaluations.md`
