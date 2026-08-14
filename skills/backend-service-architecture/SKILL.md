---
name: backend-service-architecture
description: "Design, review, or incrementally refactor backend service architecture for NestJS, FastAPI, and Fiber. Use when work involves service or module boundaries, controllers or handlers, dependency injection, domain/application/infrastructure separation, modular monoliths, ports and adapters, transactions, cross-cutting concerns, or backend decomposition. Do not use for full-stack Next.js architecture, database-only work, CI/release setup, or microservice extraction without behavioral and operational evidence."
---

# Backend Service Architecture

Design stable capability boundaries, then translate them into the installed
framework without letting framework structure become the domain model.

## Inspect before designing

1. Identify the exact framework and version, language/runtime, package manager,
   transport, persistence stack, deployment shape, tests, and supported clients.
2. Trace representative requests from transport entry to state change or query.
   Record behavior, invariants, data ownership, side effects, authorization,
   transaction boundaries, failures, retries, and observable contracts.
3. Map current dependencies and runtime ownership. Distinguish verified code and
   test evidence from conventions, inferred intent, and unvalidated hypotheses.
4. Define the requested outcome and migration constraints. Do not prescribe a
   rewrite, microservices, domain-driven design, CQRS, or event sourcing by
   default.

## Load only the applicable framework reference

- Read [nestjs.md](references/nestjs.md) for NestJS modules, providers,
  controllers, dependency injection, guards, pipes, interceptors, and filters.
- Read [fastapi.md](references/fastapi.md) for FastAPI routers, `Depends`,
  Pydantic boundary models, lifespan resources, and sync/async ownership.
- Read [fiber.md](references/fiber.md) for Fiber handlers, route groups,
  middleware, explicit Go composition, request context, and centralized errors.

Inspect the installed version and local code before applying any reference;
framework APIs and conventions can change.

Next.js is outside the supported framework set because comprehensive Next.js
architecture also owns rendering, Server Components, caching, route transitions,
and client/server boundaries. For a narrowly scoped Next.js route-handler or
Server Action BFF, apply only this skill's framework-neutral service-boundary
questions and state that no Next.js-specific reference was loaded.

## Shape the service boundary

1. Organize around a business capability or coherent service responsibility,
   not a table, transport endpoint, or framework artifact alone.
2. Keep transport adapters responsible for protocol translation, validation,
   authentication context, status codes, and serialization. Keep business
   decisions in explicit application or domain operations.
3. Give each use case one visible transaction and side-effect policy. Define
   what commits together, what happens after commit, how retries behave, and
   where idempotency is enforced.
4. Point dependencies toward stable policy. Place databases, queues, external
   APIs, clocks, identifiers, and framework objects behind narrow adapters when
   substitution or testing has real value.
5. Export the smallest stable contract. Avoid pass-through layers, generic
   repositories, circular dependencies, shared dumping grounds, and abstractions
   that hide no decision.
6. Treat authorization, tenancy, validation, observability, error translation,
   cancellation, deadlines, and resource lifetime as explicit boundary concerns.

## Compare and migrate

When a material boundary is undecided, compare at least two concrete options
against the same request paths, invariants, failure modes, coupling, test seams,
operational impact, and rollback path. Separate a modular monolith boundary from
a deployable-service boundary; do not infer that one requires the other.

For an authorized change, add the smallest fail-first behavioral or structural
check, introduce one seam, move one complete request path, preserve contracts,
and verify failure paths. Prefer reversible migration over a layer-by-layer
rewrite. Do not change public APIs, persistence, event delivery, deployment, or
production state unless the request authorizes it.

## Report

Produce only the requested artifact: evidence-backed review, boundary map,
options and trade-offs, target architecture, dependency rules, acceptance
criteria, migration slices, tests, or authorized implementation. Report checks
actually run, unsupported assumptions, deferred decisions, unrelated changes,
and runtime or production validation that remains unavailable.

The skill works independently. Database, security, performance, CI, release,
and horizontal implementation/review workflows may be composed when installed,
but they are not dependencies and do not transfer authority.
