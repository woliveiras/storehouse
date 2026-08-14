# Add full-stack Next.js architecture as a web capability

- Status: accepted
- Date: 2026-08-14
- Decision makers: @woliveiras
- Consulted: Codex
- Informed: Storehouse users
- Supersedes: none

## Context and Problem Statement

Storehouse needs a standalone capability for designing, reviewing, and
incrementally evolving full-stack Next.js applications. The existing
`backend-service-architecture` skill owns framework-neutral service boundaries
and NestJS, FastAPI, and Fiber translations, but deliberately excludes the
rendering, Server Component, cache, navigation, and client/server decisions
that make comprehensive Next.js architecture distinct.

Adding another public skill identity, collection, and evaluation row changes
the current inventory and establishes an enduring ownership boundary between
full-stack framework architecture and general backend service architecture.

## Decision Drivers

- Preserve flat domain-first `skills/<name>/` distribution and independent installation.
- Inspect the installed Next.js and React versions, router, cache model, runtime, and deployment adapter before giving version-sensitive guidance.
- Own App Router topology, Server and Client Component graphs, data entrypoint selection, rendering, streaming, cache and invalidation, runtime, deployment, and Pages Router migration.
- Keep business capability design, application/domain separation, transactions, idempotency, ports and adapters, and backend decomposition with `backend-service-architecture` when that capability is installed.
- Keep database, state, validation, UI/UX, performance, CI, and release work with their existing specialized owners.
- Extend deterministic routing, behavior, composition, security, catalog, and installation evidence without provider execution.

## Decision Outcome

Add `web-nextjs-architecture` in the flat `web` namespace and add the
declarative `nextjs` collection. The skill owns full-stack Next.js composition
and translates general service obligations into Route Handlers, Server Actions,
Server Components, cache APIs, runtimes, and deployment shapes.

`backend-service-architecture` remains the optional owner for deeper service
boundaries. Neither skill depends on the other. A Next.js application can use
the new skill alone, while a BFF with material domain, transaction, or
decomposition decisions may compose both.

The distributed inventory ratchet advances from 45 to 46 skills. Current
architecture, catalog, README, deterministic tests, evaluation inventory, and
provider-call budgets advance with it.

## Stable Criteria and Behavior/Oracle Matrix

| ID | Expected behavior | Oracle | Provenance |
| --- | --- | --- | --- |
| WNA-001 | The skill identity and minimal OpenAI interface metadata validate and install independently. | Official validators, metadata assertions, and clean-room official CLI smoke. | external |
| WNA-002 | The concise core links directly to exactly eight conditional first-level references. | Exact file inventory, direct-link, conditional-loading, and line-budget assertions. | spec-derived |
| WNA-003 | The workflow inspects exact versions, router, cache model, runtime, adapter, route tree, module graphs, data, security, and evidence limits before designing. | Core-contract assertions. | spec-derived |
| WNA-004 | App Router guidance separates URL, rendering, and business structures and covers route groups, layouts, parallel routes, and intercepting routes. | Reference contract and official-source assertions. | external |
| WNA-005 | Server/client guidance treats `use client` as a module graph boundary and protects serialization, secrets, and hydration behavior. | Reference contract and official-source assertions. | external |
| WNA-006 | Data guidance selects direct server reads, Server Actions, Route Handlers, client reads, or an external backend from callers and operational needs. | Reference contract, BFF boundary assertions, and behavior oracle. | independent |
| WNA-007 | Rendering guidance covers initial load, navigation, Suspense, streaming, waterfalls, loading, error, not-found, and recovery. | Reference contract and official-source assertions. | external |
| WNA-008 | Cache guidance distinguishes Cache Components from the previous model and defines freshness, invalidation, personalization, and multi-instance consistency. | Reference contract and behavior oracle. | independent |
| WNA-009 | Runtime guidance covers Node.js, Edge, static export, serverless, self-hosting, adapters, and production topology without provider lock-in. | Reference contract and official-source assertions. | external |
| WNA-010 | Security and migration guidance protects public entrypoints, server/client secrets, authorization, production verification, and reversible Pages/App migration. | Reference contract, behavior oracle, and security trajectory policy. | independent |
| WNA-011 | Backend architecture remains optional and owns deeper business capability, transaction, idempotency, ports, and decomposition decisions without duplication. | Core boundary assertions and composition variants. | independent |
| WNA-012 | Catalog, README, architecture, taxonomy, and ADR expose exactly 46 skills and the new collection consistently. | Repository renderer and exact inventory assertions. | independent |
| WNA-013 | Positive routing and backend-only, React-only, and database-only negatives are represented. | `RT-046` and routing assertions. | implementation-aware |
| WNA-014 | A deterministic Next.js fixture rejects route-as-domain, excessive client boundaries, internal handler round trips, missing authorization, unsafe shared cache, and unsupported deployment claims. | `BH-046`, executable oracle, protected hashes, and no-op rejection. | independent |
| WNA-015 | Standalone use, optional backend composition, and optional Baseline review preserve Next.js as focal owner. | `CP-046` variants. | independent |
| WNA-016 | Untrusted project instructions cannot expose secrets, read protected files, deploy, mutate production, or expand authority. | `SEC-046`, canary, sentinel, and trajectory policy. | independent |
| WNA-017 | Required validators, syntax checks, dry-run budgets, diff checks, and clean-room installation pass without provider execution. | Recorded local command results and provider gates. | external |

## Consequences

- Good: Next.js architecture gains a coherent full-stack workflow instead of disconnected framework tips.
- Good: backend architecture remains reusable across frameworks and optional for Next.js BFF depth.
- Good: version, cache model, runtime, and deployment differences become explicit evidence requirements.
- Bad: inventory-sensitive assertions, evaluation fixtures, and provider budgets must advance for a new public row.
- Neutral: official Next.js guidance informs framework behavior but does not prove a product's runtime, security, performance, or production readiness.

## Confirmation

The decision is confirmed when WNA-001 through WNA-017 pass without provider
execution, a clean-room install exposes exactly the requested skill, and the
final worktree contains only task-owned changes.
