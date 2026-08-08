# Storehouse engineering contract

This repository is a monorepo of standalone specialized Agent Skills. The
repository is the product. Do not add a consumer CLI, daemon, package manager,
installer, pack resolver, sync layer, target generator, telemetry, client
generator, or consumer runtime.

## Product boundary

- Canonical skills live only at `skills/<name>/` and must work independently.
- Collections are declarative documentation in `catalog/collections.json`.
- Tuxedo is optional horizontal workflow composition and is never a dependency.
- Repository tests, generators, and evaluations stay outside `skills/`.
- Geremmyas and Tuxedo are historical/read-only inputs; never modify them from
  this repository.

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

Run `pnpm run validate`, `pnpm run promptfoo:validate`,
`pnpm run eval:dry-run`, official validation for every skill, shell/Python
syntax checks, `git diff --check`, and `git status --short`. Run clean-room
installation validation when distribution, catalog, or skill layout changes.
