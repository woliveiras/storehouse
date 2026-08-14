---
name: web-nextjs-architecture
description: "Design, review, or incrementally evolve full-stack Next.js architecture across App Router or Pages Router, Server Components and Client Components, Server Actions, Route Handlers, caching, rendering, streaming, runtimes, and deployment. Use when work involves route and layout topology, server/client boundaries, data-access placement, BFF design, Cache Components, migration, or deployment-shape decisions. Do not use for backend service architecture unrelated to Next.js, React-only component design, database-only work, UI/UX design, speculative performance optimization, CI, or release automation."
---

# Next.js Architecture

Design from the installed Next.js execution model and product behavior rather
than from a preferred folder template or deployment provider.

## Inspect the actual application

1. Identify the exact Next.js and React version, package manager, App Router,
   Pages Router, or hybrid state, enabled flags such as `cacheComponents`,
   `next.config` behavior, TypeScript configuration, tests, and build commands.
2. Identify Node.js and Edge usage, static export, serverless, self-hosted, or
   managed deployment, the deployment adapter, instance topology, filesystem
   and connection constraints, regions, and supported clients.
3. Map the route tree, layouts, public entrypoints, Server and Client Component
   module graphs, data sources, mutations, caches, external integrations,
   authentication and authorization, secrets, and observable contracts.
4. Trace representative initial requests and route transitions through render,
   data access, mutation, invalidation, streaming, hydration, and failure. Keep
   verified evidence, inferred intent, hypotheses, and unavailable runtime or
   production evidence distinct.

## Load only relevant references

- Read [app-router-and-project-structure.md](references/app-router-and-project-structure.md) for App Router files, route groups, private folders, layouts, and route topology.
- Read [server-client-boundaries.md](references/server-client-boundaries.md) for Server and Client Component module graphs, serialization, secrets, hydration, and third-party boundaries.
- Read [data-actions-and-bff.md](references/data-actions-and-bff.md) when choosing among direct server reads, Server Actions, Route Handlers, client fetching, and an external backend.
- Read [rendering-streaming-and-navigation.md](references/rendering-streaming-and-navigation.md) for rendering, Suspense, streaming, loading and error boundaries, prefetching, and route transitions.
- Read [caching-and-revalidation.md](references/caching-and-revalidation.md) when caching, Cache Components, freshness, invalidation, personalization, or multiple instances matter.
- Read [runtimes-and-deployment.md](references/runtimes-and-deployment.md) for Node.js, Edge, static export, serverless, self-hosting, adapters, and runtime configuration.
- Read [security-and-verification.md](references/security-and-verification.md) when the application has protected data or actions, public endpoints, implementation work, or an architecture review.
- Read [pages-router-migration.md](references/pages-router-migration.md) only for Pages Router architecture, coexistence, or migration to App Router.

Inspect the installed version and its official documentation before applying a
version-sensitive API or convention. Do not transfer behavior between routers,
cache models, runtimes, or deployment adapters without verification.

## Shape the Next.js boundary

1. Keep route files and framework entrypoints focused on routing, rendering,
   protocol translation, and composition. A route group, layout, Route Handler,
   or Server Action is not automatically a business capability boundary.
2. Default to Server Components and introduce a Client Component boundary only
   where interactivity, client state, lifecycle, custom hooks, or browser APIs
   require it. Keep secrets and server-only dependencies outside the client
   module graph and make crossed values serializable.
3. Fetch internal read data directly from the server-side operation that needs
   it. Use Server Actions primarily for UI-originated mutations and Route
   Handlers for public HTTP contracts, webhooks, or external clients. Do not add
   an internal HTTP round trip merely to reuse a Route Handler.
4. Design static, cached, and request-time work together with Suspense,
   meaningful loading states, error recovery, navigation, and invalidation.
   Prevent accidental waterfalls and caches without explicit ownership,
   freshness, consistency, and multi-instance behavior.
5. Treat Server Actions and Route Handlers as public-facing entrypoints for
   authentication, authorization, validation, rate and size controls, error
   disclosure, idempotency, and audit needs. Do not rely on hidden UI or Proxy
   alone for secure authorization.
6. Make runtime and deployment assumptions explicit. Do not claim portability,
   persistence, shared cache behavior, WebSocket support, or production
   readiness from a local development server or successful build alone.

## Preserve the backend ownership boundary

This skill owns full-stack Next.js composition and the translation of service
concerns into Next.js mechanisms. `backend-service-architecture` may optionally
own deeper business capability boundaries, application and domain separation,
transactions, idempotency, ports and adapters, or backend decomposition. It is
not a dependency: this skill must remain useful when installed alone. Do not
duplicate a general backend architecture, prescribe a microservice, or move
business policy into framework entrypoints merely because Next.js can execute
server-side code.

## Compare, change, and verify

For a material decision, compare at least two viable options against the same
routes, users, invariants, data freshness, failure paths, client JavaScript,
runtime constraints, operational topology, test seams, rollback, and migration.

For an authorized implementation, add the smallest fail-first behavioral or
structural check, move one complete route or request path, preserve public URLs
and contracts, and verify a production build plus representative initial load,
client navigation, mutation, invalidation, authorization denial, loading, error,
and recovery behavior. Keep Pages/App coexistence or deployment rollback
available until the migrated path is proven.

Produce only the requested artifact: evidence-backed review, route and boundary
map, options, target architecture, acceptance criteria, migration slices, tests,
or authorized implementation. Report actual checks, unsupported assumptions,
unrelated changes, and unavailable browser, runtime, deployment, or production
evidence. The skill works independently; database, UI/UX, performance, backend,
security, CI, release, and horizontal workflows remain optional composition.
