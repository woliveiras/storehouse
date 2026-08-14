# ADR 0006: Add Product Testing Engineering

- Status: Accepted
- Date: 2026-08-14

## Context

Storehouse has focused skills for CI workflow construction, one-behavior TDD
through optional Baseline, product performance, product security and privacy,
product UI/UX, data systems, and Phaser/Godot 2D game testing. It does not have
an independent capability for risk-based product test strategy and architecture
across web, mobile, API, persistence, offline, concurrency, migration,
accessibility, and device boundaries.

The repository has 47 skills before this addition. Existing work occupies ADR
0005 and criterion IDs through RT/BH/CP/SEC-047, so this addition uses ADR 0006
and RT/BH/CP/SEC-048.

## Decision

Add the standalone `product-testing-engineering` skill and declarative
`product-testing` collection. The skill owns risk prioritization, public test
seams, independent oracles, deterministic fixtures and harnesses, synthetic
data, isolation, flakiness diagnosis, behavioral coverage, test-level
allocation, and evidence limits for web and mobile product systems.

Ownership remains separated:

- Baseline TDD owns implementation of one approved behavior through a
  fail-first check;
- `ci-*` skills own workflow syntax, jobs, matrices, caches, permissions, and CI
  execution;
- `product-performance-engineering` owns metrics, profiling, benchmarks,
  budgets, and technical performance causality;
- `product-security-privacy-engineering` owns threats, trust boundaries,
  authorization policy, abuse cases, and technical privacy decisions;
- `product-ui-ux-design` owns experience and accessibility decisions; and
- `game-dev-2d-testing` owns Phaser and Godot 2D game testing.

Each capability remains independently installable. Optional composition may
translate an approved specialized risk into a reliable test without moving its
governing decision into this skill.

The installed package contains one concise entrypoint, deterministic Codex
metadata, two reusable templates, and nine directly linked references. It has no
runtime, dependency, script, README, companion skill, or consumer-side policy.

## Deterministic acceptance criteria

- **PTE-001:** exact skill identity, routing description, and Codex interface
  metadata validate and install independently.
- **PTE-002:** the entrypoint directly and conditionally links exactly nine
  first-level references and two reusable assets within its line budget.
- **PTE-003:** the workflow begins with governing behavior, product risks,
  journeys, invariants, states, boundaries, and consequences before test levels.
- **PTE-004:** every selected check maps risk to the cheapest suitable public
  seam and an independent oracle that rejects a plausibly wrong implementation.
- **PTE-005:** unit, component, integration, contract, and end-to-end coverage is
  allocated without a universal pyramid or duplicated confidence claims.
- **PTE-006:** fixtures control clock, IDs, randomness, network, concurrency, and
  data and remain minimal, readable, isolated, synthetic, and recoverable.
- **PTE-007:** authorized changes use fail-first evidence; strategy-only and
  diagnosis-only requests do not mutate product behavior.
- **PTE-008:** flakiness is diagnosed causally without weakened assertions,
  arbitrary sleeps, indiscriminate retries, threshold relaxation, or test
  deletion.
- **PTE-009:** web, mobile, API, persistence, tenancy, migration, offline,
  retry, duplicate, accessibility, simulator, physical-device, and human
  evidence boundaries are explicit.
- **PTE-010:** coverage, snapshots, automation, browser runs, simulators, and
  passing checks are bounded evidence rather than proof.
- **PTE-011:** production data, real customer data, external end-to-end,
  production, and device-farm execution require explicit authority and safety
  controls.
- **PTE-012:** taxonomy, architecture, collection, and rendered README expose an
  exact inventory of 48 standalone skills.
- **PTE-013:** RT-048 covers explicit and implicit routing plus negatives for
  Baseline TDD, CI workflow work, performance benchmarking, security threat
  modeling, and game testing.
- **PTE-014:** BH-048 uses a synthetic web/mobile/API/persistence/tenancy fixture
  and an executable oracle that rejects no-op, coverage proof, weakened
  assertions, unauthorized execution claims, and tenant crossing.
- **PTE-015:** CP-048 compares control, focal, specialized composition, and
  minimal Baseline variants while preserving ownership.
- **PTE-016:** SEC-048 requires trajectory evidence against canary access, test
  deletion, threshold lowering, real-data use, production execution, and
  protected-file mutation while still requiring a legitimate strategy.
- **PTE-017:** deterministic, official, dry-run, syntax, diff, and clean-room
  installation checks pass without provider/model evaluation execution.

## Consequences

The exact inventory becomes 48 skills and gains one declarative collection.
Repository-only tests and evaluations grow, including a bounded mechanism for a
routing negative against frozen external Baseline TDD. No consumer runtime,
implicit dependency, provider call, production operation, or universal test
shape is introduced. Test evidence remains proportional to the seam,
environment, fixture, oracle, and execution actually observed.
