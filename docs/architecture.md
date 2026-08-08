# Architecture

The repository product is the set of independent directories under `skills/`.
Each directory owns its `SKILL.md` and optional `agents/`, `references/`,
`scripts/`, and `assets/` resources. Installed skills do not import repository
code or depend on Tuxedo, Geremmyas, another skill, Python, or Node maintenance
dependencies.

`catalog/collections.json` is a declarative documentation source. Includes are
expanded in declared order, reject cycles and duplicates, and never execute an
install. `catalog/skills.json` records source provenance and migration
dispositions. `maintenance/`, `tests/`, and `evals/` are maintainer-only
boundaries.

Tuxedo remains the separate global horizontal workflow. Composition is by an
agent selecting independently installed skills; there is no sync layer,
dependency resolver, client generator, or duplicated Tuxedo skill here.
