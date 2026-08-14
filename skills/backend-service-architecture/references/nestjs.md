# NestJS translation

Use these rules only after inspecting the installed NestJS version, module
graph, HTTP adapter, persistence libraries, tests, and application bootstrap.

## Boundaries and composition

- Treat feature modules as explicit composition and visibility boundaries.
  Keep `imports`, `providers`, `controllers`, and `exports` small; export a
  capability-facing provider rather than internal repositories and helpers.
- Keep controllers thin transport adapters. Parse the request, invoke one
  application operation, and translate its result or failure; do not coordinate
  repositories, payment clients, queues, and domain policy in controllers.
- Use providers for explicit application services, policies, and adapters.
  Prefer constructor injection and stable tokens where an infrastructure
  implementation crosses a capability boundary.
- Use dynamic modules for genuinely configurable infrastructure composition,
  not to conceal mutable global state or business branching.
- Treat route/module grouping as a candidate boundary, then verify it against
  business invariants, data ownership, callers, and change history.

## Request and cross-cutting flow

- Use pipes for transport parsing and validation; do not confuse validated DTOs
  with behavior-rich domain objects.
- Use guards for authentication and authorization decisions that belong before
  handler execution. Keep resource-sensitive policy explicit and testable.
- Use interceptors for bounded request/response concerns such as timing,
  tracing, or deliberate mapping. Do not hide business workflows or commits in
  interceptors.
- Use exception filters to translate known failures consistently. Preserve the
  original failure for internal diagnostics without exposing sensitive details.
- Use middleware only for protocol-level work that truly precedes route policy.
  Account for ordering across middleware, guards, interceptors, pipes, handlers,
  and filters.

## Dependency and lifecycle risks

- Treat circular modules, `forwardRef`, broad global modules, service locators,
  and large shared modules as coupling signals. Remove the underlying ownership
  ambiguity instead of normalizing the workaround.
- Choose singleton, request, or transient provider scope from state and lifetime
  requirements. Do not introduce request scope without measuring its propagation
  and runtime cost.
- Keep ORM entities and query builders out of transport contracts. Define the
  transaction around the application operation and make post-commit events,
  retries, and idempotency visible.
- Keep framework decorators and Nest-specific exceptions at the transport or
  integration edge when the domain must remain reusable.

## Verification

Test domain policy without the Nest container where practical, application
operations with controlled ports, module wiring with the Nest testing utilities,
and representative HTTP behavior end to end. Include authorization denial,
validation failure, transaction rollback, adapter failure, retry/idempotency,
and error translation. A compiled module alone does not prove correct runtime
ownership or request behavior.

## Primary references

- [NestJS modules](https://docs.nestjs.com/modules)
- [NestJS providers](https://docs.nestjs.com/providers)
- [NestJS request lifecycle](https://docs.nestjs.com/faq/request-lifecycle)
