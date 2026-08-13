# Add product performance engineering as an independent product capability

- Status: accepted
- Date: 2026-08-13
- Decision makers: @woliveiras
- Consulted: Codex
- Informed: Storehouse users
- Supersedes: none

## Context and Problem Statement

Storehouse needs a standalone capability that drives measurable web and mobile
performance symptoms through reproduction, profiling, causal optimization, and
verification. `product-ui-ux-design` already owns the observable experience
under latency, but intentionally does not own technical root cause or runtime
optimization. Game and PostgreSQL performance have narrower specialized owners.

Adding another public skill identity, collection, and evaluation row changes the
current Storehouse inventory and formalizes an important ownership boundary. ADR
0001 records the historical taxonomy migration and ADR 0002 records the first
`product` capability; neither historical decision should be edited retroactively.

## Decision Drivers

- Preserve flat domain-first `skills/<name>/` distribution and independent installation.
- Require a baseline, repeatable measurement, profile-supported causal path, and functional equivalence before claiming improvement.
- Cover web, Android, Apple platforms, and actual cross-platform mobile runtimes through conditional first-level references.
- Keep UI/UX experience states, game performance, PostgreSQL tuning, CI/release, and observability-only work with their existing owners.
- Prevent false claims from one score, one run, best-run selection, simulator-only evidence, missing field data, or budget relaxation.
- Extend deterministic routing, behavior, composition, security, catalog, and installation evidence without provider execution.

## Decision Outcome

Add `product-performance-engineering` as the second skill in the flat `product`
namespace and add the declarative `product-performance` collection. The skill
owns performance measurement, profiling, technical root cause, causal
optimization, technical budgets, benchmarks, and regression tests for web and
mobile products.

`product-ui-ux-design` continues to own feedback, loading/offline/error/recovery
states, user control, task continuity, microcopy, and experience acceptance
criteria. Composition is optional when both concerns are in scope. Neither skill
depends on the other. Baseline remains an optional external horizontal workflow.

The distributed inventory ratchet advances from 43 to 44 skills. The current
architecture, catalog, README, deterministic tests, evaluation inventory, and
exact provider-call budgets advance with it.

## Stable Criteria and Behavior/Oracle Matrix

| ID | Expected behavior | Oracle | Provenance |
| --- | --- | --- | --- |
| PPE-001 | The skill identity and minimal OpenAI interface metadata validate and install independently. | Official validators, exact metadata assertions, and clean-room official CLI smoke. | external |
| PPE-002 | The concise core links directly to exactly eight conditional first-level references. | Exact file inventory, direct-link, conditional-loading, and line-budget assertions. | spec-derived |
| PPE-003 | The workflow inspects the real system and defines environment, path, baseline, distribution, and impact before optimization. | Core-contract assertions. | spec-derived |
| PPE-004 | Foundations distinguish evidence classes, profiling, causality, variance, percentiles, equivalence, and prioritization. | Reference contract and primary-source assertions. | independent |
| PPE-005 | Web guidance covers Core Web Vitals without treating Lighthouse or laboratory evidence as certification or field proof. | Web reference contract and source assertions. | external |
| PPE-006 | Android guidance separates startup states and TTID/TTFD and covers frames, ANRs, Compose/Views, resources, benchmarks, and physical devices. | Android reference contract and source assertions. | external |
| PPE-007 | Apple guidance separates launch, usable state, hangs, hitches, rendering, resources, MetricKit, and physical devices. | Apple reference contract and source assertions. | external |
| PPE-008 | Cross-platform guidance attributes shared, interop, and native costs and validates Android and iOS separately. | Cross-platform reference contract and source assertions. | independent |
| PPE-009 | Performance tests use repeated distributions, preserve correctness, reject no-op/mutants, and never weaken budgets to pass. | Testing-reference contract and executable behavior mutants. | independent |
| PPE-010 | Field observability preserves segmentation, sampling, privacy, release comparison, and correlation limits. | Field-reference contract and security assertions. | independent |
| PPE-011 | UI/UX, integrity, cache, concurrency, background, and authority boundaries remain explicit and independent. | Boundary contract and composition variants. | independent |
| PPE-012 | Catalog, README, architecture, taxonomy, and ADR expose exactly 44 skills and the new collection consistently. | Repository renderer and exact inventory assertions. | independent |
| PPE-013 | Positive routing plus UI/UX-only, game, PostgreSQL-only, and CI/release-only negatives are represented. | `RT-044` expansion and routing assertions. | implementation-aware |
| PPE-014 | A deterministic multi-platform fixture rejects missing baselines, best-run proof, false field/root-cause claims, changed behavior, relaxed budgets, latency masking, and simulator-only proof. | `BH-044`, executable oracle, calibrated sample, no-op, and targeted mutants. | independent |
| PPE-015 | Standalone, optional UI/UX composition, optional Baseline review, and adversarial trace/log boundaries are covered. | `CP-044`, `SEC-044`, protected hashes, sentinel, canary, and trajectory policy. | independent |
| PPE-016 | Required validators, syntax checks, dry-run budgets, diff checks, and clean-room installation pass without provider execution. | Recorded local command results and provider gates. | external |

## Consequences

- Good: web and mobile performance work gains a causal measurement-to-verification workflow rather than generic tips.
- Good: product experience and technical optimization keep clear independent owners while allowing optional composition.
- Good: platform-specific detail remains progressive and the installed skill has no tool or companion dependency.
- Bad: inventory-sensitive assertions and provider budgets must advance for a new public row.
- Neutral: official platform guidance informs investigation but does not establish product-specific requirements or empirical improvement.

## Confirmation

The decision is confirmed when PPE-001 through PPE-016 pass with no provider
execution and the final worktree contains only task-owned changes.
