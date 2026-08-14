# Pages Router coexistence and migration

Load this reference only when the application still uses `pages`, legacy data
APIs, API Routes, or an incremental App Router migration. Inspect the installed
version's migration guides before translating any API.

## Preserve behavior while crossing routers

Inventory `getServerSideProps`, `getStaticProps`, `getStaticPaths`, API Routes,
custom `_app`, custom `_document`, routing hooks, head and metadata behavior,
fallback modes, rewrites, middleware or Proxy, client data libraries, and tests.
Record URL, status, headers, cookies, cache behavior, rendered content,
authorization, loading, error, and not-found contracts for each migrated path.

- Keep Pages Router and App Router coexistence as a reversible migration seam.
- Move one complete route or coherent vertical slice rather than creating a
  permanent half-migration across every layer.
- Translate shared UI into layouts deliberately; `_app` and `_document` do not
  map one-to-one to an App Router layout.
- Replace `getServerSideProps` or `getStaticProps` from the required rendering
  and freshness behavior, not through a mechanical API substitution.
- Keep an API Route until callers have migrated and the chosen Server Action,
  Route Handler, or external backend preserves its public contract.
- Account for navigation and state differences when Pages Router and App Router
  links cross between routing systems.

Add fail-first characterization checks before moving the route. Verify direct
load, soft navigation, refresh, back/forward, metadata, cookies, cache,
authorization, loading, errors, and production build output. Maintain rollback
to the previous router path until the new path passes in the representative
deployment.

## Primary sources

- [Migrating from Pages Router to App Router](https://nextjs.org/docs/app/guides/migrating/app-router-migration)
- [Pages Router documentation](https://nextjs.org/docs/pages)
- [App Router documentation](https://nextjs.org/docs/app)
