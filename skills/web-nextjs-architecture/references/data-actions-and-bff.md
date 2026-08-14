# Data access, actions, and BFF boundaries

Choose an entrypoint from its callers, protocol, caching needs, authorization,
and deployment behavior rather than from a universal preference.

## Select the narrowest appropriate surface

- Read directly in a Server Component or server-side application operation when
  only the rendered Next.js tree consumes the data. Do not call the app's own
  Route Handler from a Server Component; the extra HTTP round trip adds a
  failure and latency boundary without creating reuse.
- Use a Server Action primarily for a mutation initiated by the application UI.
  Treat it as a public-facing mutation entrypoint, validate input, recheck
  authorization, define the transaction and idempotency behavior, and coordinate
  cache invalidation with the mutation result.
- Use a Route Handler for a public HTTP endpoint, webhook, non-UI response,
  external or mobile client, protocol-level cache contract, or integration that
  cannot call a Server Action. Keep protocol translation at the edge.
- Fetch in a Client Component when the requirement depends on browser-only APIs,
  frequent polling, or a client cache whose lifecycle is intentional. Avoid
  moving server-capable reads into the browser merely for familiarity.
- Use a separate backend when the required protocol, background execution,
  durable connection, independent scaling, operational ownership, or client set
  exceeds the verified Next.js deployment contract.

Next.js backend features are not a full backend replacement. Serverless Route
Handlers may lack shared memory, writable
filesystem, long execution, or durable WebSocket connections. Verify the real
adapter and host before accepting those obligations.

## Compose with backend architecture

This reference translates entrypoints into Next.js. Use the optional
`backend-service-architecture` skill when the material problem is a business
capability boundary, transaction, idempotency policy, ports and adapters,
modular monolith, or backend decomposition. Keep the Next.js entrypoint as a
transport or UI adapter over that operation instead of duplicating business
policy in a Server Action and Route Handler.

## Primary sources

- [Backend for Frontend guide](https://nextjs.org/docs/app/guides/backend-for-frontend)
- [Fetching data](https://nextjs.org/docs/app/getting-started/fetching-data)
- [Updating data with Server Functions](https://nextjs.org/docs/app/getting-started/updating-data)
- [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route)
