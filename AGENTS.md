# Storehouse engineering contract

This repository is a monorepo of standalone specialized Agent Skills. The
repository is the product. Do not add a consumer CLI, daemon, package manager,
installer, pack resolver, sync layer, target generator, telemetry, client
generator, or consumer runtime.

## Product boundary

- Canonical skills live only at `skills/<name>/` and must work independently.
- Collections are declarative documentation in `catalog/collections.json`.
- Baseline is optional horizontal workflow composition and is never a dependency.
- SDD is an optional Storehouse capability under `skills/sdd-specification`; installing any
  other skill or collection does not install or require it.
- Repository tests and evaluations stay outside `skills/`. `evals/catalog.json`
  is the canonical evaluation-case inventory; checked-in fixtures and oracles
  change with it.
- Baseline is an optional composition source. Treat its checkout as read-only
  while working here.
- Git is the default archive. Remove reconstructible documents that no longer
  guide a current decision, operation, contract, risk, or behavior; do not keep
  archive directories or completed task bundles in the current tree.

## Change workflow

For material behavior, preserve
`spec -> behavior/oracle matrix -> fail-first test -> implementation -> evidence -> spec/test/code review`.
Give criteria stable IDs and classify each oracle as `spec-derived`,
`independent`, `implementation-aware`, `external`, or `diagnostic-probe`.
Preserve unrelated work and stop if a source baseline changes.

## Toolchain and authority

- Use UV for Python and PNPM for Node. Development dependencies must never be
  required by an installed skill.
- Model/provider evals require an exact budget, explicit `--execute`, and a
  matching human approval token. They never run from install, ordinary CI,
  commit, or push.
- Push, release, publication, PR creation, remote mutation, destructive cleanup,
  and model calls require separate human authority.
- Commit coherent task-owned slices locally with Conventional Commits.

## Required checks

Run `pnpm run validate`, `pnpm run validate:official`,
`pnpm run promptfoo:validate`, `pnpm run eval:dry-run`, shell/Python syntax
checks, `git diff --check`, and `git status --short`. Run a clean-room official
CLI installation smoke when distribution, collections, or skill layout changes.
