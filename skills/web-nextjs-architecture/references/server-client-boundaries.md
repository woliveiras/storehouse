# Server and Client Component boundaries

Treat `use client` as a module graph boundary, not a rendering preference. In
the App Router, layouts and pages are Server Components by default. A Client
Component can still participate in server prerendering, then hydrate in the
browser.

## Place the boundary

Use a Server Component for server-side data access, secrets, reduced client
JavaScript, and composition that needs no browser interaction. Introduce a
Client Component for state, event handlers, effects, custom client hooks, or
browser APIs. Place `use client` at the smallest stable entrypoint because its
imports and descendants enter the client module graph.

- Pass only values supported by the installed React serialization contract
  across the Server-to-Client boundary. Validate library and version behavior
  instead of assuming every class instance or platform object is serializable.
- Keep database clients, credentials, private environment variables, filesystem
  access, and privileged SDKs behind a server-only boundary. Use the `server-only`
  marker where it strengthens detection, but do not treat it as the sole
  security control.
- Wrap a browser-dependent third-party component in a narrow Client Component
  adapter instead of promoting an entire route or layout into the client graph.
- Render providers as deep as practical so static server-rendered structure is
  not unnecessarily included in the client graph.
- Distinguish a hydration mismatch from data staleness, cache inconsistency,
  client-state restoration, and invalid HTML before changing the boundary.

Trace the initial HTML, React Server Component payload, client bundle, hydration,
and subsequent navigation behavior. A successful server render does not prove
that the hydrated or navigated application preserves the same state and output.

## Primary sources

- [Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components)
- [`use client`](https://nextjs.org/docs/app/api-reference/directives/use-client)
- [Preventing environment poisoning](https://nextjs.org/docs/app/getting-started/server-and-client-components#preventing-environment-poisoning)
