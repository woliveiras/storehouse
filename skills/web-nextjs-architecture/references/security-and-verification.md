# Security and verification

Treat every server-side entrypoint as reachable through an untrusted request.
Client rendering, a hidden button, layout redirect, or optimistic Proxy check is
not secure authorization.

## Protect each boundary

- Authenticate and authorize again inside each sensitive Server Action, Route
  Handler, and server-side data access operation. Treat Actions and Handlers as
  public-facing entrypoints even when only application UI currently calls them.
- Keep secure authorization near the data or operation. A Data Access Layer can
  centralize session verification and a DTO can limit returned fields; neither
  substitutes for domain-specific permission checks.
- Use Proxy for bounded request preprocessing and optimistic redirect decisions,
  not as the only guard for nested routes, Server Actions, or direct data access.
- Validate untrusted input, content type, body size, identifiers, redirects,
  uploads, webhook authenticity, and error disclosure at the applicable edge.
- Keep secrets out of Client Components, serialized props, logs, URLs, generated
  artifacts, and `NEXT_PUBLIC_*`. Inspect the production client bundle when a
  module-boundary change could expose server code.
- Define idempotency, rate controls, audit behavior, transaction ownership, and
  post-commit work for sensitive mutations; compose backend or security skills
  when those concerns exceed Next.js translation.

## Verify architecture claims

Use the smallest checks that can reject a plausible wrong implementation:

- dependency or import checks for server/client and capability boundaries;
- unit tests for policy and data mapping outside framework adapters;
- integration tests for Server Actions, Route Handlers, caching, invalidation,
  runtime-specific resources, and error translation;
- a production build plus browser tests for direct URLs, hydration, navigation,
  forms, loading, error, not-found, recovery, and authorization denial;
- representative deployed checks for adapter limits, shared cache, proxy/CDN,
  streaming, rolling releases, and multiple instances.

Do not claim security, production readiness, runtime portability, or user-visible
correctness from TypeScript, lint, a production build, automated browser checks,
or a local server alone. Report what each check establishes and what remains
unverified.

## Primary sources

- [Authentication and authorization](https://nextjs.org/docs/app/guides/authentication)
- [Data security](https://nextjs.org/docs/app/guides/data-security)
- [Production checklist](https://nextjs.org/docs/app/guides/production-checklist)
- [Proxy](https://nextjs.org/docs/app/api-reference/file-conventions/proxy)
