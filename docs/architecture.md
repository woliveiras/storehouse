# Architecture

The repository product is the set of independent directories under `skills/`.
Each directory owns its `SKILL.md` and optional `agents/`, `references/`,
`scripts/`, and `assets/` resources. Installed skills do not import repository
code or depend on Baseline, another skill, or repository test and evaluation
dependencies.

The current flat domain-first inventory contains 48 skills. The `backend`
namespace owns framework-neutral service-boundary design with conditional
NestJS, FastAPI, and Fiber translations. `web-nextjs-architecture` owns
full-stack Next.js route, render, server/client, data-entrypoint, cache, runtime,
and deployment decisions while optionally composing with the backend capability
for deeper service boundaries. The `product`
namespace owns independent cross-platform product UI/UX design, product
performance engineering, product security and privacy, and product testing
capabilities.
`product-ui-ux-design` owns observable experience under latency;
`product-performance-engineering` owns measurement, profiling, technical root
cause, optimization, budgets, and causal regression tests; and
`product-security-privacy-engineering` owns product threat models, trust
boundaries, authorization and tenancy, sensitive-data lifecycles, adversarial
verification, and incident containment; and `product-testing-engineering` owns
risk-based test strategy and architecture, public seams, deterministic fixtures,
independent oracles, behavioral coverage, test levels, and flakiness diagnosis
across web and mobile product boundaries. Each can be installed alone, and game
interfaces, performance, and testing remain in the separate `game-dev-2d`
namespace.

`catalog/collections.json` is a declarative documentation source. Includes are
expanded in declared order, reject cycles and duplicates, and never execute an
install. `tests/` validates deterministic repository contracts. `evals/` owns
the behavioral case inventory, fixtures, oracles, Promptfoo configuration, and
isolated provider runner. Neither boundary is distributed with a skill.

Baseline remains the separate global horizontal workflow. Composition is by an
agent selecting independently installed capabilities; there is no sync layer,
dependency resolver, or client generator. Storehouse owns the optional
`sdd-specification` skill and `sdd` collection; Baseline does not distribute
them. SDD may hand
approved behavior to TDD and review capabilities when installed, but neither
repository imports or copies the other's workflow implementation.
