# Fiber translation

Use these rules only after inspecting the installed Fiber major version, Go
version, HTTP/runtime compatibility requirements, persistence, process model,
middleware, and tests. Do not transfer APIs between Fiber major versions.

## Boundaries and composition

- Keep handlers as transport adapters over `fiber.Ctx`: parse and validate the
  request, invoke one application operation, then serialize the result or map an
  error. Do not pass `fiber.Ctx` into domain policy or persistence.
- Treat route groups as transport organization, not proof of a capability
  boundary. Align packages with cohesive behavior, invariants, state ownership,
  and change patterns.
- Compose dependencies explicitly in `main` or a focused bootstrap package.
  Use constructors and small interfaces defined near their consumers; avoid
  package globals, mutable singletons, service locators, and interfaces created
  only to imitate another framework's dependency injection.
- Keep application and domain packages independent of Fiber. Let adapters own
  databases, queues, external clients, clocks, and identifiers.

## Request lifecycle and failures

- Derive the supported cancellation, deadline, identity, and trace information
  from the request boundary into `context.Context` using the installed Fiber
  version's API. Never retain `fiber.Ctx` or references to request-backed data
  beyond the handler lifetime.
- Make middleware order explicit. Keep authentication, authorization, recovery,
  request IDs, observability, body limits, and security headers narrow; do not
  hide business transactions or retries in middleware.
- Configure a centralized error handler that maps typed application failures to
  stable HTTP responses while preserving internal diagnostic context and
  withholding sensitive details.
- Define one visible transaction boundary per application operation. Make
  rollback, post-commit work, retry, idempotency, and partial failure explicit.
- Preserve ordinary Go error wrapping and inspection. Do not convert every
  internal error into a Fiber error before the transport edge.

## Verification

Test domain and application packages without Fiber, handlers with controlled
ports, middleware order and short-circuit behavior, and representative HTTP
requests. Cover malformed input, authorization denial, cancellation, adapter
failure, transaction rollback, retry/idempotency, panic recovery, and the error
handler. Run the race detector when shared state or concurrent adapters are in
scope; a handler unit test alone does not prove lifecycle or concurrency safety.

## Primary references

- [Fiber documentation and version selector](https://docs.gofiber.io/)

Select the installed major version before opening its routing, middleware,
context, and error-handling pages.
