# Runtimes and deployment

Treat deployment shape as part of the Next.js architecture. Record the adapter,
runtime per entrypoint, region, instance count, scaling model, connection and
execution limits, writable filesystem, cache sharing, streaming support,
reverse proxy or CDN, environment injection, and rollback mechanism.

## Choose from verified constraints

- Prefer the default Node.js runtime when the application needs ordinary Node
  APIs or dependencies. Select Edge Runtime only for a demonstrated requirement
  and verify every dependency; Edge supports a smaller API surface and does not
  support every Next.js capability such as ISR.
- Use static export only when every required route works without a Next.js
  runtime server. Server Actions and request-time server features cannot be
  assumed available in exported output.
- In serverless deployments, do not assume memory shared across requests,
  writable persistent filesystem, unbounded execution, background completion,
  or durable WebSocket connections. Verify host and adapter limits.
- For self-hosting, place an appropriate reverse proxy in front of the Next.js
  server, assess streaming and buffering, and configure cache and invalidation
  behavior across multiple instances. `output: 'standalone'` can reduce a
  container artifact but does not provide the surrounding operational controls.
- Separate build-time public configuration from server-side runtime secrets.
  A value included through `NEXT_PUBLIC_*` is eligible for the client bundle and
  must not contain a secret.

Test the production build and artifact in the target topology. A local
`next dev`, single process, or successful build does not validate horizontal
cache coherence, rolling deployment, connection lifetime, proxy buffering,
regional behavior, or recovery.

## Primary sources

- [Edge Runtime](https://nextjs.org/docs/pages/api-reference/edge)
- [Static exports](https://nextjs.org/docs/app/guides/static-exports)
- [Self-hosting](https://nextjs.org/docs/app/guides/self-hosting)
- [Environment variables](https://nextjs.org/docs/app/guides/environment-variables)
