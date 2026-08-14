# FastAPI translation

Use these rules only after inspecting the installed FastAPI, Starlette, Pydantic,
Python, server, persistence, concurrency, and test versions.

## Boundaries and composition

- Use `APIRouter` to organize and compose transport endpoints, but verify real
  capability boundaries through invariants, state ownership, callers, and
  change history. A router prefix is not a domain boundary by itself.
- Keep path-operation functions thin: translate HTTP input, call one application
  operation, and map the result. Do not open transactions, implement policy, and
  coordinate several integrations directly in the router.
- Use `Depends` for explicit request-scoped collaborators such as identity,
  authorization context, sessions, and use-case construction. Avoid dependency
  graphs that hide business sequencing or make ownership impossible to trace.
- Use Pydantic models as validated boundary contracts. Map them deliberately to
  domain values when domain invariants or behavior exceed transport validation.

## Resources, concurrency, and failures

- Own shared clients, pools, and model resources through the application
  `lifespan`; make startup failure, shutdown, and test replacement observable.
- Keep `async` end to end only for non-blocking work supported by the selected
  libraries. Isolate blocking calls deliberately; do not add `async def` as a
  performance claim.
- Define a visible transaction boundary per application operation. Make commit,
  rollback, post-commit side effects, retries, and idempotency explicit.
- Pass cancellation, deadlines, identity, and trace data intentionally. Do not
  pass `Request`, database sessions, or ORM models into behavior that should be
  independent of HTTP and persistence.
- Translate known application failures with centralized exception handlers and
  stable public error contracts. Do not leak tracebacks, SQL, credentials, or
  private payloads.

## Verification

Test domain policy as ordinary Python, application operations with controlled
ports, dependency overrides and lifespan behavior at the integration boundary,
and representative HTTP behavior with the project's supported client. Cover
authorization denial, Pydantic validation, sync/async adapter failure,
transaction rollback, retry/idempotency, startup/shutdown, and error mapping.
Do not assume an in-process test proves production server, worker, or event-loop
behavior.

## Primary references

- [FastAPI bigger applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [FastAPI lifespan events](https://fastapi.tiangolo.com/advanced/events/)
